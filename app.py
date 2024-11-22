##########################################################
#
#
#
#
##########################################################
import matplotlib.pyplot as plt 
import numpy as np 
import pandas as pd 
from IPython.display import display, HTML

import shutil
import sys
import os.path

from pyomo.environ import *
from constraints import create_constraints


H = 10

Network = {
    # time grid
    'TIME':  range(0, H+1),
    
    # states
    'STATES': {
        'RM'   : {'capacity': 500, 'initial': 200, 'price':  0},
        'P'    : {'capacity': 500, 'initial':   0, 'price': 10},
    },

    'STATES_SHIPMENT': {
        ('P', 15) : {'shipment': 15.0},
    },
    
    # state-to-task arcs indexed by (state, task)
    'ST_ARCS': {
        ('RM', 'T1') : {'rho': 1.0},
    },
    
    # task-to-state arcs indexed by (task, state)
    'TS_ARCS': {
        ('T1', 'P') : {'dur': 1, 'rho': 1.0},
    },
    
    # state-to-task arcs indexed by (state, task)
    'ST_ARCS_EXTENDED': {
        ('RM', 'T1', 'T1-SD') : {'rho': 0},
        ('RM', 'T1', 'T1-SU') : {'rho': 0.2},
        ('RM', 'T1', 'T1-SB') : {'rho': 1.0},
    },
    
    # task-to-state arcs indexed by (task, state)
    'TS_ARCS_EXTENDED': {
        ('T1', 'P', 'T1-SD') : {'dur': 1, 'rho': 0},
        ('T1', 'P', 'T1-SU') : {'dur': 1, 'rho': 0.2},
        ('T1', 'P', 'T1-SB') : {'dur': 1, 'rho': 1.0},
    },
    
    # unit data indexed by (unit, task)
    'UNIT_TASKS': {
        ('U1', 'T1') : {'tau_min': 2, 'tau_max': 7, 'Bmin': 10, 'Bmax': 10, 'Cost': 0, 'vCost': 0, 'isContinuos': True, 'hasSS': True, 'isDirect': False},
    },

    'UNIT_TASK_SUBTASKS': {
        #('U1', 'T1', 'T1-ST') : {'tau': 2, 'Bmin': 1, 'Bmax': 2, 'Cost': 0, 'vCost': 3.5, 'subtask': "direct_transition"},
        ('U1', 'T1', 'T1-SD') : {'tau': 2, 'Bmin': 2, 'Bmax': 2, 'Cost': 0, 'vCost': 3.5, 'subtask': "shutdown"},
        ('U1', 'T1', 'T1-SU') : {'tau': 2, 'Bmin': 2, 'Bmax': 2, 'Cost': 0, 'vCost': 3.5, 'subtask': "startup"},
        ('U1', 'T1', 'T1-SB') : {'tau': 1, 'Bmin': 1, 'Bmax': 3, 'Cost': 0, 'vCost': 5, 'subtask': "steady-state"},
    }
}

STN = Network

STATES = STN['STATES']
ST_ARCS = STN['ST_ARCS']
TS_ARCS = STN['TS_ARCS']
UNIT_TASKS = STN['UNIT_TASKS']
UNIT_TASK_SUBTASKS = STN['UNIT_TASK_SUBTASKS']
TIME = STN['TIME']
ST_ARCS_EXTENDED = STN['ST_ARCS_EXTENDED']
TS_ARCS_EXTENDED = STN['TS_ARCS_EXTENDED']

##############################################################################################
#                                       TASKS                                                #
##############################################################################################

# Set of tasks.
S_TASKS = set([i for (j,i) in UNIT_TASKS])

# Set of all tasks and subtasks.
S_SUBTASKS = set([iprime for (j,i,iprime) in UNIT_TASK_SUBTASKS]) 

# S_K_MINUS[i] set of materials consumed by task i.
S_K_MINUS = {i: set() for i in S_TASKS} 
for (k,i) in ST_ARCS:
    S_K_MINUS[i].add(k)

# S_K_PLUS[i] set of materials consumed by task i.
S_K_PLUS = {i: set() for i in S_TASKS} 
for (i,k) in TS_ARCS:
    S_K_PLUS[i].add(k)

# S_J[i] is the set of units j able to execute task i.
S_J = {i: set() for i in S_TASKS}
for (j,i) in UNIT_TASKS:
    S_J[i].add(j)

# Set of al continuous tasks.
S_I_C = set([i for (j,i) in UNIT_TASKS if (UNIT_TASKS[(j,i)]['isContinuos'] == True)])

# S_I_CSS is the set of continuos tasks with startups and shutdowns.
S_I_CSS = set([i for (j,i) in UNIT_TASKS if (UNIT_TASKS[(j,i)]['isContinuos'] == True and UNIT_TASKS[(j,i)]['hasSS'] == True)])

# Set of all continuous tasks with direct transition.
S_I_CT = set([i for (j,i) in UNIT_TASKS if (UNIT_TASKS[(j,i)]['isContinuos'] == True and UNIT_TASKS[(j,i)]['hasSS'] == True and UNIT_TASKS[(j,i)]['isDirect'] == True)])

# Individual of all subtasks SU, SB, SD and ST for each continuos task.
S_I_SU = {i: set() for i in S_I_CSS}
for (j,i,i_SU) in UNIT_TASK_SUBTASKS:
    if UNIT_TASK_SUBTASKS[(j,i,i_SU)]['subtask'] == "startup":
        S_I_SU[i].add(i_SU)

S_I_SD = {i: set() for i in S_I_CSS}
for (j,i,i_SD) in UNIT_TASK_SUBTASKS:
    if UNIT_TASK_SUBTASKS[(j,i,i_SD)]['subtask'] == "shutdown":
        S_I_SD[i].add(i_SD)

S_I_ST = {i: set() for i in S_I_CSS}
for (j,i,i_ST) in UNIT_TASK_SUBTASKS:
    if UNIT_TASK_SUBTASKS[(j,i,i_ST)]['subtask'] == "direct_transition":
        S_I_ST[i].add(i_ST)

S_I_SB = {i: set() for i in S_I_CSS}
for (j,i,i_SB) in UNIT_TASK_SUBTASKS:
    if UNIT_TASK_SUBTASKS[(j,i,i_SB)]['subtask'] == "steady-state":
        S_I_SB[i].add(i_SB)

# Set of all subtasks SU, SB, SD and ST for each continuos task.
S_I_S = {i: set() for i in S_I_C}
for (j,i,i_SUB) in UNIT_TASK_SUBTASKS:
    S_I_S[i].add(i_SUB)

# Set of all transient subtasks SU, SD and ST for each continuos task.
S_I_TS = {i: set() for i in S_I_C}
for (j,i,i_TS) in UNIT_TASK_SUBTASKS:
    if ((UNIT_TASK_SUBTASKS[(j,i,i_TS)]['subtask'] == "startup") or
       (UNIT_TASK_SUBTASKS[(j,i,i_TS)]['subtask'] == "shutdown") or
       (UNIT_TASK_SUBTASKS[(j,i,i_TS)]['subtask'] == "direct_transition")):
        S_I_TS[i].add(i_TS)

# P_rho_MINUS[i,k] is the input fraction of material k consumed by task i.
#P_rho_MINUS = {(i,k): ST_ARCS[(k,i)]['rho'] for (k,i) in ST_ARCS}
P_rho_MINUS = {(i_SUB,k): ST_ARCS_EXTENDED[(k,i,i_SUB)]['rho'] for (k,i,i_SUB) in ST_ARCS_EXTENDED}

# P_rho_PLUS[i,k] is the output fraction of material k produced by task i.
P_rho_PLUS = {(i_SUB,k): TS_ARCS_EXTENDED[(i,k,i_SUB)]['rho'] for (i,k,i_SUB) in TS_ARCS_EXTENDED}

# P_P[i,k] is the processing time for task i to produce material k.
P_P = {(i,k): TS_ARCS[(i,k)]['dur'] for (i,k) in TS_ARCS}

# p[i] is the maximum completion time for task i.
p = {i: max([ P_P[i,k] for k in S_K_PLUS[i]]) for i in S_TASKS}

# Min and max lenghts of a run.
P_Tau_Min = {(i,j): UNIT_TASKS[(j,i)]['tau_min'] for (j,i) in UNIT_TASKS}
P_Tau_Max = {(i,j): UNIT_TASKS[(j,i)]['tau_max'] for (j,i) in UNIT_TASKS}

# Number of periods for transition, startup and shutdown
P_Tau = {(i_SUB,j): UNIT_TASK_SUBTASKS[(j,i,i_SUB)]['tau'] for (j,i,i_SUB) in UNIT_TASK_SUBTASKS}
#P_Tau_SB = {(i,j): UNIT_TASKS[(j,i)]['tau_SD'] for (j,i) in UNIT_TASKS if (UNIT_TASKS[(j,i)]['isContinuos'] == True and UNIT_TASKS[(j,i)]['hasStartupsShutdowns'] == True and UNIT_TASKS[(j,i)]['isDirect'] == False)}

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

# Min and max batch sizes of unit j for task i.
P_Bmax = {(i_SUB,j): UNIT_TASK_SUBTASKS[(j,i,i_SUB)]['Bmax'] for (j,i,i_SUB) in UNIT_TASK_SUBTASKS}
P_Bmin = {(i_SUB,j): UNIT_TASK_SUBTASKS[(j,i,i_SUB)]['Bmin'] for (j,i,i_SUB) in UNIT_TASK_SUBTASKS}

S_TIME = np.array(TIME)
S_MATERIALS = set([k for k in STATES.keys()])

#S_J_CSS is the set of units that can process continuos tasks involving startups and shutdowns.
S_J_SS = set([j for (j,i) in UNIT_TASKS if (UNIT_TASKS[(j,i)]['isContinuos'] == True and UNIT_TASKS[(j,i)]['hasSS'] == True)])
##############################################################################################
#                                       VARIABLES                                            #
##############################################################################################

model = ConcreteModel()

# V_X[i,j,n] = 1 if unit j processes (sub)task i at time point n.
model.V_X = Var(S_SUBTASKS, S_UNITS, S_TIME, domain = Boolean)

# V_Y_End[i,j,n] = 1 if a run of a continuous task in unit j ends at time point n.
model.V_Y_End = Var(S_TASKS, S_UNITS, S_TIME, domain = Boolean)

# V_Y_Start[i,j,n] = 1 if a run of a continuous task in unit j starts at time point n.
model.V_Y_Start = Var(S_TASKS, S_UNITS, S_TIME, domain = Boolean)

# V_B[i,j,n] is the batch size assigned to task i in unit j at time n.
model.V_B = Var(S_SUBTASKS, S_UNITS, S_TIME, domain = NonNegativeReals)

# V_S[s,n] is the inventory of material s in time n.
model.V_S = Var(S_MATERIALS, S_TIME, domain = NonNegativeReals)

# V_Q[j,n] is the inventory of unit j in time n.
model.V_Q = Var(S_UNITS, S_TIME, domain = NonNegativeReals)

# V_X_Hat[i,j,n] is 1 if unit j is in task mode i (ready to execute batch subtaks i_SB(i)) at time point n.
model.V_X_Hat = Var(S_TASKS, S_UNITS, S_TIME, domain = Boolean)

# V_X_Hat_Idle[j,n] is 1 if unit j is in idle mode at time point n.
model.V_X_Hat_Idle = Var(S_UNITS, S_TIME, domain = Boolean)

######################################
#               Constraint           #
######################################

def task_unit_assignment(model, j, n):
    return sum(model.V_X[i_SUB,j,n] for i in S_I[j] for i_SUB in S_I_S[i]) <= 1 
    
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
        return model.V_S[k,n+1] == STATES[k]['initial'] - sum(P_rho_MINUS[i_SUB,k]*model.V_B[i_SUB,j,n] for i in (S_I_MINUS[k] & S_I_C) for j in S_J[i] for i_SUB in S_I_S[i])
    elif (n >= 1 and n < H):
        return model.V_S[k,n+1] == (model.V_S[k,n] 
                                  + sum(P_rho_PLUS[i_SUB,k]*model.V_B[i_SUB,j,n-1] for i in (S_I_PLUS[k] & S_I_C) for j in S_J[i] for i_SUB in S_I_S[i]) 
                                  - sum(P_rho_MINUS[i_SUB,k]*model.V_B[i_SUB,j,n] for i in (S_I_MINUS[k] & S_I_C) for j in S_J[i] for i_SUB in S_I_S[i]))
    else:
        return Constraint.Skip

def track_startup_shutdown(model, i, j, n):
    if n >= 1 and j in S_J[i]:
        return model.V_X_Hat[i,j,n] == (model.V_X_Hat[i,j,n-1] 
                                      + sum(model.V_X[i_SB,j,n-1] for i_SB in S_I_SB[i])
                                      + sum(model.V_X[i_SU,j,n-1] for i_SU in S_I_SU[i])
                                      - sum(model.V_X[i_SB,j,n] for i_SU in S_I_SB[i]) 
                                      - sum(model.V_X[i_SD,j,n] for i_SD in S_I_SD[i]))
    else:
        return Constraint.Skip

def track_idle_unit(model, j, n):
    if j in S_J_SS and n >= 1:
        return model.V_X_Hat_Idle[j,n] == (model.V_X_Hat_Idle[j,n-1] 
                                         + sum(model.V_X[i_SD,j,n-1] for i in (S_I_CSS & S_I[j]) for i_SD in S_I_SD[i]) 
                                         - sum(model.V_X[i_SU,j,n] for i in (S_I_CSS & S_I[j]) for i_SU in S_I_SU[i])) 
                                         
    else:
        return Constraint.Skip

def track_start_end_batch_task_continuos_1(model, i, j, n):
    if n >= 1 and i in S_I_CSS and j in S_J[i]:
        return model.V_Y_Start[i,j,n] == (sum(model.V_X[i_SB,j,n] for i_SB in S_I_SB[i]) 
                                       - sum(model.V_X[i_SB,j,n-1] for i_SB in S_I_SB[i])
                                       + model.V_Y_End[i,j,n])
    else:
        return Constraint.Skip

def track_start_end_batch_task_continuos_2(model, i, j, n):
    if i in S_I_CSS and j in S_J[i]:
        return model.V_Y_Start[i,j,n] + model.V_Y_End[i,j,n] <= 1
    else:
        return Constraint.Skip

def min_lenght_run_continuos(model, i, j, n):
    if i in S_I_CSS and j in S_J[i]:
        return sum(model.V_X[i_SB,j,n] for i_SB in S_I_SB[i]) >= sum(model.V_Y_Start[i,j,nprime] for nprime in S_TIME if (nprime >= (n - P_Tau_Min[i,j] + 1) and nprime <= (n))) 
    else:
        return Constraint.Skip

def max_lenght_run_continuos(model, i, j, n):
    if i in S_I_CSS and j in S_J[i]:
        return sum(model.V_X[i_SB,j,nprime] for i_SB in S_I_SB[i] for nprime in S_TIME if (nprime >= (n - P_Tau_Max[i,j]) and nprime <= (n))) <= P_Tau_Max[i,j] 
    else:
        return Constraint.Skip

def unit_availability_with_startup_shutdown(model, j, n):
    if j in S_J_SS:
        return sum(model.V_X[iprime,j,nprime] for i in (S_I[j] & S_I_C) for iprime in S_I_S[i] for nprime in S_TIME if ( (nprime >= n - P_Tau[iprime,j] + 1) and (nprime <= n))) + sum(model.V_X_Hat[i,j,n] for i in (S_I[j] & S_I_CSS)) + model.V_X_Hat_Idle[j,n] == 1 
    else:
        return      

def unit_capacity_lb_continuos(model, i, j, n):
    return model.V_B[i_SUB,j,n] >= model.V_X[i_SUB,j,n]*P_Bmin[i_SUB,j]
    
def unit_capacity_ub_continuos(model, i, j, n):
    return model.V_B[i_SUB,j,n] <= model.V_X[i_SUB,j,n]*P_Bmax[i_SUB,j]
    
def objective(model):
    return (sum(STATES[s]['price']*model.V_S[s,H] for s in STATES) 
            - sum(UNIT_TASKS[(j,i)]['Cost']*model.V_X[i_SUB,j,n] + UNIT_TASK_SUBTASKS[(j,i,i_SUB)]['vCost']*model.V_B[i_SUB,j,n] for i in S_TASKS for i_SUB in S_I_S[i] for j in S_J[i] for n in S_TIME))

 

model.C_Task_Unit_Assignment = Constraint(S_UNITS, S_TIME, rule = task_unit_assignment)
#model.C_Track_Start_End_Batch_Task = Constraint(S_TASKS, S_UNITS, S_TIME, rule = track_start_end_batch_task)
#model.C_Unit_Capacity_LB = Constraint(S_TASKS, S_UNITS, S_TIME, rule = unit_capacity_lb)
#model.C_Unit_Capacity_UB = Constraint(S_TASKS, S_UNITS, S_TIME, rule = unit_capacity_ub)
model.C_Material_Storage_Limit = Constraint(S_MATERIALS, S_TIME, rule = material_capacity)
#model.C_Min_Lenght_Run = Constraint(S_TASKS, S_UNITS, S_TIME, rule = min_lenght_run)
#model.C_Max_Lenght_Run = Constraint(S_TASKS, S_UNITS, S_TIME, rule = max_lenght_run)
model.C_Material_Mass_Balance = Constraint(S_MATERIALS, S_TIME, rule = material_mass_balance)
model.C_Objective = Objective(expr = objective, sense = maximize)
model.C_Track_Startup_Shutdown = Constraint(S_I_CSS, S_UNITS, S_TIME, rule = track_startup_shutdown)
model.C_Track_Idle_Unit = Constraint(S_UNITS, S_TIME, rule = track_idle_unit)
model.C_Track_Start_End_Batch_Task_Continuos_1 = Constraint(S_I_CSS, S_UNITS, S_TIME, rule = track_start_end_batch_task_continuos_1)
model.C_Track_Start_End_Batch_Task_Continuos_2 = Constraint(S_I_CSS, S_UNITS, S_TIME, rule = track_start_end_batch_task_continuos_2)
model.C_Mix_Lenght_Run_Continuos = Constraint(S_I_CSS, S_UNITS, S_TIME, rule = min_lenght_run_continuos)
model.C_Max_Lenght_Run_Continuos = Constraint(S_I_CSS, S_UNITS, S_TIME, rule = max_lenght_run_continuos)
model.C_Unit_Availability_With_StartUp_ShutDown = Constraint(S_UNITS, S_TIME, rule = unit_availability_with_startup_shutdown)
model.C_Unit_Capacity_LB = Constraint(S_SUBTASKS, S_UNITS, S_TIME, rule = unit_capacity_lb_continuos)
model.C_Unit_Capacity_UB = Constraint(S_SUBTASKS, S_UNITS, S_TIME, rule = unit_capacity_ub_continuos)


SolverFactory('appsi_highs').solve(model).write() 
for con in model.component_map(Constraint).itervalues():
    con.pprint()

print(S_I)

# show all of V_X
model.V_X.display()
model.V_Y_Start.display()
model.V_Y_End.display()
model.V_B.display()
model.V_X_Hat.display()


print("Set of taks: ", S_TASKS)
print("Set of all subtasks:", S_SUBTASKS)
print("Set of units: ", S_UNITS)
print("Set of material: ", S_MATERIALS)
print("Set of time points: ", S_TIME)
print("------------------------------------")
print("Set of tasks in each unit: ", S_I)
print("Set of tasks productin raw materials: ", S_I_PLUS)
print("Set of tasks consuming raw material: ", S_I_MINUS)
print("Set of continuous tasks: ", S_I_C)
print("Set of continuos tasks with startup and shutdown: ", S_I_CSS)
print("Set of continuos tasks with direct transition: ", S_I_CT)
print("set of shutdown subtask of a continuos task: ", S_I_SD)
print("Set of startup subtask of continuos task: ", S_I_SU)
print("Set of transition subtask of a continuos task: ", S_I_ST)
print("Set of one period steady state subtask related to a continuos taks: ", S_I_SB)
print("Set of transition subtasks: ", S_I_TS)
print("Set of of all subasks related to a continuos task: ", S_I_S)
print("------------------------------------")
print("Set of units executing tasks: ", S_J)
print("Set of units executing each continuos task: ", S_J_SS)
print("------------------------------------")
print("Input fraction of material k consumed by task i: ", P_rho_MINUS) 
print("Output fraction of material k produced by task i:", P_rho_PLUS) 
print("Min lenght of a run: ", P_Tau_Min) 
print("Max lenght of a run", P_Tau_Max) 
print("Number of periods for direct_transition, startup and shutdown:", P_Tau)
print("Min batch size of task in unit:", P_Bmin)
print("Max batch size of task in unit:", P_Bmax)


