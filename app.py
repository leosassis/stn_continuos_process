import matplotlib.pyplot as plt 
import numpy as np 
import pandas as pd 
from IPython.display import display, HTML

import shutil
import sys
import os.path

from pyomo.environ import *


H = 23

Network = {
    # time grid
    'TIME':  range(0, H+1),
    
    # states
    'STATES': {
        'RM'   : {'capacity': 500, 'initial': 200, 'price':  0},
        'P'    : {'capacity': 500, 'initial':   0, 'price': 10},
    },
    
    # state-to-task arcs indexed by (state, task)
    'ST_ARCS': {
        ('RM', 'T1') : {'rho': 1.0},
    },
    
    # task-to-state arcs indexed by (task, state)
    'TS_ARCS': {
        ('T1', 'P') : {'dur': 1, 'rho': 1.0},
    },
    
    # unit data indexed by (unit, task)
    'UNIT_TASKS': {
        ('U1', 'T1') : {'tau_min': 3, 'tau_max': 5, 'Bmin': 10, 'Bmax': 10, 'Cost': 0, 'vCost': 0},
    },
}

STN = Network

STATES = STN['STATES']
ST_ARCS = STN['ST_ARCS']
TS_ARCS = STN['TS_ARCS']
UNIT_TASKS = STN['UNIT_TASKS']
TIME = STN['TIME']

##############################################################################################
#                                       TASKS                                                #
##############################################################################################

#Set of taks.
S_TASKS = set([i for (j,i) in UNIT_TASKS])

# S_K_MINUS[i] set of materials consumed by task i.
S_K_MINUS = {i: set() for i in S_TASKS} 
for (k,i) in ST_ARCS:
    S_K_MINUS[i].add(k)

# S_K_PLUS[i] set of materials consumed by task i.
S_K_PLUS = {i: set() for i in S_TASKS} 
for (i,k) in TS_ARCS:
    S_K_PLUS[i].add(k)

# P_rho_MINUS[i,k] is the input fraction of material k consumed by task i.
P_rho_MINUS = {(i,k): ST_ARCS[(k,i)]['rho'] for (k,i) in ST_ARCS}

# P_rho_PLUS[i,k] is the output fraction of material k produced by task i.
P_rho_PLUS = {(i,k): TS_ARCS[(i,k)]['rho'] for (i,k) in TS_ARCS}

# P_P[i,k] is the processing time for task i to produce material k.
P_P = {(i,k): TS_ARCS[(i,k)]['dur'] for (i,k) in TS_ARCS}

# p[i] is the maximum completion time for task i.
p = {i: max([ P_P[i,k] for k in S_K_PLUS[i]]) for i in S_TASKS}

# Min and maz=x lenghts of a run.
P_Tau_Min = {(i,j): UNIT_TASKS[(j,i)]['tau_min'] for (j,i) in UNIT_TASKS}
P_Tau_Max = {(i,j): UNIT_TASKS[(j,i)]['tau_max'] for (j,i) in UNIT_TASKS}

# S_J[i] is the set of units j able to execute task i.
S_J = {i: set() for i in S_TASKS}
for (j,i) in UNIT_TASKS:
    S_J[i].add(j)

##############################################################################################
#                                       STATES                                               #
##############################################################################################

# S_I_MINUS[k] is the set of tasks that consume material k.
S_I_MINUS = {k: set() for k in STATES}
for (k,i) in ST_ARCS:
    S_I_MINUS[k].add(i)

# S_I_PLUS[k] is the set of tasks that produce material k.
S_I_PLUS = {k: set() for k in STATES}
for (i,k) in TS_ARCS:
    S_I_PLUS[k].add(i)

# P_Chi[k] is the storage capacity of each material.
P_Chi = {k: STATES[k]['capacity'] for k in STATES}

##############################################################################################
#                                       UNITS                                                #
##############################################################################################

S_UNITS = set([j for (j,i) in UNIT_TASKS])

# S_I[j] is the set of tasks executed in each unit j.
S_I = {j: set() for j in S_UNITS}
for (j,i) in UNIT_TASKS:
    S_I[j].add(i)

# Min and max capacities of unit j for task i.
P_Bmax = {(i,j): UNIT_TASKS[(j,i)]['Bmax'] for (j,i) in UNIT_TASKS}
P_Bmin = {(i,j): UNIT_TASKS[(j,i)]['Bmin'] for (j,i) in UNIT_TASKS}

S_TIME = np.array(TIME)
S_MATERIALS = set([k for k in STATES.keys()])


##############################################################################################
#                                       UNITS                                                #
##############################################################################################

model = ConcreteModel()

# V_X[i,j,n] = 1 if unit j processes (sub)task i at time point n.
model.V_X = Var(S_TASKS, S_UNITS, S_TIME, domain = Boolean)

# V_Y_End[i,j,n] = 1 if a run of a continuous task in unit j ends at time point n.
model.V_Y_End = Var(S_TASKS, S_UNITS, S_TIME, domain = Boolean)

# V_Y_Start[i,j,n] = 1 if a run of a continuous task in unit j starts at time point n.
model.V_Y_Start = Var(S_TASKS, S_UNITS, S_TIME, domain = Boolean)

# V_B[i,j,n] is the batch size assigned to task i in unit j at time n.
model.V_B = Var(S_TASKS, S_UNITS, S_TIME, domain=NonNegativeReals)

# V_S[s,n] is the inventory of material s in time n.
model.V_S = Var(S_MATERIALS, S_TIME, domain=NonNegativeReals)

# Q[j,n] is the inventory of unit j in time n.
model.V_Q = Var(S_UNITS, S_TIME, domain=NonNegativeReals)

######################################
#               Constraint           #
######################################

def task_unit_assignment(model, j, n):
    return sum(model.V_X[i,j,n] for i in S_I[j]) <= 1 
    
def track_start_end_batch_task(model, i, j, n):
    if n >= 1:
        return model.V_Y_Start[i,j,n] == model.V_X[i,j,n] - model.V_X[i,j,n-1] + model.V_Y_End[i,j,n]
    else:
        return Constraint.Skip

def unit_capacity_lb(model, i, j, n):
    if (j,i) in UNIT_TASKS.keys():
        return model.V_B[i,j,n] >= model.V_X[i,j,n]*P_Bmin[i,j]
    else:
        return Constraint.Skip    

def unit_capacity_ub(model, i, j, n):
    if (j,i) in UNIT_TASKS.keys():
        return model.V_B[i,j,n] <= model.V_X[i,j,n]*P_Bmax[i,j]
    else:
        return Constraint.Skip

def material_capacity(model, k, n):
    return model.V_S[k,n] <= P_Chi[k]

def min_lenght_run(model, i, j, n):
    return model.V_X[i,j,n] >= sum(model.V_Y_Start[i,j,nprime] for nprime in S_TIME if (nprime >= n - P_Tau_Min[i,j] + 1 and nprime <= n))    

def max_lenght_run(model, i, j, n):
    return sum(model.V_X[i,j,nprime] for nprime in S_TIME if (nprime >= n - P_Tau_Max[i,j] and nprime <= n)) <= P_Tau_Max[i,j] 
    
def material_mass_balance(model, k, n):
    if n == 0:
        return model.V_S[k,n+1] == STATES[k]['initial'] - sum(P_rho_MINUS[i,k]*model.V_B[i,j,n] for i in S_I_MINUS[k] for j in S_J[i])
    elif (n >= 1 and n < H):
        return model.V_S[k,n+1] == model.V_S[k,n] + sum(P_rho_PLUS[i,k]*model.V_B[i,j,n-1] for i in S_I_PLUS[k] for j in S_J[i]) - sum(P_rho_MINUS[i,k]*model.V_B[i,j,n] for i in S_I_MINUS[k] for j in S_J[i])
    else:
        return Constraint.Skip
         
def objective(model):
    return (sum(STATES[s]['price']*model.V_S[s,H] for s in STATES) 
            - sum(UNIT_TASKS[(j,i)]['Cost']*model.V_X[i,j,n] + UNIT_TASKS[(j,i)]['vCost']*model.V_B[i,j,n] for i in S_TASKS for j in S_J[i] for n in S_TIME))

model.C_Task_Unit_Assignment = Constraint(S_UNITS, S_TIME, rule = task_unit_assignment)
model.C_Track_Start_End_Batch_Task = Constraint(S_TASKS, S_UNITS, S_TIME, rule = track_start_end_batch_task)
model.C_Unit_Capacity_LB = Constraint(S_TASKS, S_UNITS, S_TIME, rule = unit_capacity_lb)
model.C_Unit_Capacity_UB = Constraint(S_TASKS, S_UNITS, S_TIME, rule = unit_capacity_ub)
model.C_Material_Storage_Limit = Constraint(S_MATERIALS, S_TIME, rule = material_capacity)
model.C_Min_Lenght_Run = Constraint(S_TASKS, S_UNITS, S_TIME, rule = min_lenght_run)
model.C_Max_Lenght_Run = Constraint(S_TASKS, S_UNITS, S_TIME, rule = max_lenght_run)
model.C_Material_Mass_Balance = Constraint(S_MATERIALS, S_TIME, rule = material_mass_balance)
model.C_Objective = Objective(expr = objective, sense = maximize)


SolverFactory('appsi_highs').solve(model).write() 
for con in model.component_map(Constraint).itervalues():
    con.pprint()

print(S_I)

# show all of V_X
model.V_X.display()
model.V_Y_Start.display()
model.V_Y_End.display()
model.V_B.display()

# iterate through and show values
#print()
#for s in model.V_X:
#    if model.X[s].value == 1:
#        print(f'for index {s} X[{s}] is: {model.X[s].value}')

# dump into a dictionary.... an entry point for pandas!
#print()
#print(model.X.extract_values())

# make a pd.Series indexed by the index set(s)
#print()
#w_vals = pd.Series(model.X.extract_values(), name=model.X.name)
#print(w_vals)
#print(p)

UnitAssignment = pd.DataFrame({j:[None for n in S_TIME] for j in S_UNITS}, index=S_TIME)

for n in S_TIME:
    for j in S_UNITS:
        for i in S_I[j]:
            for s in S_K_PLUS[i]:
                if n-p[i] >= 0:
                    if model.V_X[i,j,max(S_TIME[S_TIME <= n-p[i]])]() > 0:
                        UnitAssignment.loc[n,j] = None               
        for i in S_I[j]:
            if model.V_X[i,j,n]() > 0:
                UnitAssignment.loc[n,j] = (i,model.V_B[i,j,n]())

print(UnitAssignment)