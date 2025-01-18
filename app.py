##########################################################
#The current model has no utility constraints.           # 
#It assumes no storage restrictions.                     #
#It assumes unlimited amount of raw materials            #
#It assume no delays: idis, idly, rmi_dly, rmi_n         #
#It assumes no batch units: j_b                          #
#There is no pre-defined tasks for n=0: i_ini            #
#It assumes a simplified objectie function               #
#Verify mass balance (should ir be cumulative) and Eq20  #
##########################################################

import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd 
from IPython.display import display, HTML
from pyomo.environ import *
from pyomo.opt import SolverFactory
from data import *
from optimization import set_solver_options
from sets import create_sets
from itertools import product

H = H_Network_test
STN = Network_test

STATES = STN['STATES']
STATES_SHIPMENT = STN['STATES_SHIPMENT']
ST_ARCS = STN['ST_ARCS']
TS_ARCS = STN['TS_ARCS']
UNIT_TASKS = STN['UNIT_TASKS']
TIME = STN['TIME']
TASKS_TRANSITION_TASKS = STN['TASKS_TRANSITION_TASKS']


##############################################################################################
#                                       MAIN SETS                                            #
##############################################################################################

#Set of tasks.
S_TASKS = set([i for (j,i) in UNIT_TASKS])

#Set of units.
S_UNITS = set([j for (j,i) in UNIT_TASKS])

#Set of periods.
S_TIME = np.array(TIME)

#Set of materials.
S_MATERIALS = set([k for k in STATES.keys()])

#Equivalent to ij.
P_TASK_UNIT = {(i,j): UNIT_TASKS[(j,i)]['direction'] for (j,i) in UNIT_TASKS} 

#Equivalent ipits.
P_TASKS_TRANSITIONS = {(i,ii): TASKS_TRANSITION_TASKS[(i,ii)]['direction'] for (i,ii) in TASKS_TRANSITION_TASKS} 

#Equivalent ik.
P_TASKS_CONSUMP = {(i,k): -1 for (k,i) in ST_ARCS} 
P_TASKS_PROD = {(i,k): 1 for (i,k) in TS_ARCS} 
P_TASKS_PROD_CONSUMP = P_TASKS_CONSUMP | P_TASKS_PROD 

#Equivalent to jii.
P_TASK_TRANSITIONS_UNIT = {(j,i,ii): P_TASKS_TRANSITIONS[i,ii] for (j,i) in UNIT_TASKS for (j,ii) in UNIT_TASKS if (i,j) in P_TASK_UNIT if (ii,j) in P_TASK_UNIT if (i,ii) in P_TASKS_TRANSITIONS}

#Equivalent to icts.
S_I_Continuos_Tasks = set([i for (j,i) in UNIT_TASKS]) 

#Equivalent to ip.
S_I_Production_Tasks = set([i for (j,i) in UNIT_TASKS if all ((ii,i) not in TASKS_TRANSITION_TASKS for ii in S_TASKS)]) 


S_I_Production_Tasks_With_Transition = set([i for (i,ii) in TASKS_TRANSITION_TASKS]) 


S_I_All_Transition_Tasks = set([ii for (i,ii) in TASKS_TRANSITION_TASKS]) 

#Equivalent to ictsnt.
S_I_Production_Tasks_Without_Transition = S_TASKS - S_I_Production_Tasks_With_Transition - S_I_All_Transition_Tasks 

#Equivalent to i_ts_d.
S_I_Direct_Transition_Tasks = set([i for (ii,i) in TASKS_TRANSITION_TASKS if (TASKS_TRANSITION_TASKS[(ii,i)]['isDirect'] == True)]) 

#Equivalent to i_ts_i.
S_I_Indirect_Transition_Tasks = set([i for (ii,i) in TASKS_TRANSITION_TASKS if (TASKS_TRANSITION_TASKS[(ii,i)]['isDirect'] == False)]) 

#Equivalent to i_ts_su.
S_I_Startup_Tasks = set([i for (ii,i) in TASKS_TRANSITION_TASKS if (TASKS_TRANSITION_TASKS[(ii,i)]['isDirect'] == False and TASKS_TRANSITION_TASKS[(ii,i)]['isSU'] == True) ]) 

#Equivalent to i_ts_su.
S_I_Shutdown_Tasks = set([i for (ii,i) in TASKS_TRANSITION_TASKS if (TASKS_TRANSITION_TASKS[(ii,i)]['isDirect'] == False and TASKS_TRANSITION_TASKS[(ii,i)]['isSD'] == True) ]) 

#Equivalent to ip_d.
S_I_Production_Tasks_With_Direct_Transition = set([i for (i,ii) in TASKS_TRANSITION_TASKS if (TASKS_TRANSITION_TASKS[(i,ii)]['isDirect'] == True)]) 

#Equivalent to ip_i.
S_I_Production_Tasks_With_Indirect_Transition = set([i for (i,ii) in TASKS_TRANSITION_TASKS if (TASKS_TRANSITION_TASKS[(i,ii)]['isDirect'] == False)]) 

# S_K_CONSUMED_BY_I[i] set of materials consumed by task i. Equivalent to i_minus.
S_K_CONSUMED_BY_I = {i: set() for i in S_TASKS} 
for (k,i) in ST_ARCS:
    S_K_CONSUMED_BY_I[i].add(k)

# S_K_PRODUCED_BY_I[i] set of materials produced by task i. Equivalent to i_plus.
S_K_PRODUCED_BY_I = {i: set() for i in S_TASKS} 
for (i,k) in TS_ARCS:
    S_K_PRODUCED_BY_I[i].add(k)

# S_I_CONSUMING_K[k] is the set of tasks consuming material k. Equivalent to i_minus.
S_I_CONSUMING_K = {k: set() for k in STATES}
for (k,i) in ST_ARCS:
    S_I_CONSUMING_K[k].add(i)

# S_I_PRODUCING_K[k] is the set of tasks producing material k. Equivalent to i_plus.
S_I_PRODUCING_K = {k: set() for k in STATES}
for (i,k) in TS_ARCS:
    S_I_PRODUCING_K[k].add(i)

# S_J_Executing_I[i] is the set of units j able to execute task i. Equivalent to ij_set.
S_J_Executing_I = {i: set() for i in S_TASKS}
for (j,i) in UNIT_TASKS:
    S_J_Executing_I[i].add(j)

# S_I_In_J[j] is the set of tasks executed in each unit j. Equivalent to ij_set.
S_I_In_J = {j: set() for j in S_UNITS}
for (j,i) in UNIT_TASKS:
    S_I_In_J[j].add(i)

#%%
#Equivalent to j_d.
S_J_Units_With_Direct_Transition_Tasks = set([j for (j,i) in UNIT_TASKS if i in S_I_Production_Tasks_With_Direct_Transition]) 

#Equivalent to j_i.
S_J_Units_With_Shutdown_Tasks = set([j for (j,i) in UNIT_TASKS if i in S_I_Indirect_Transition_Tasks]) 

#Equivalent to j_c.
S_J_Units_Without_Transition_Tasks = S_UNITS - S_J_Units_With_Direct_Transition_Tasks - S_J_Units_With_Shutdown_Tasks 

#Equivalent rmp.
S_K_Final_Products = set([k for k in STATES if STATES[k]['isProd'] == True])

#Equivalent rmi.
S_K_Intermediates = set([k for k in STATES if STATES[k]['isIntermed'] == True])

print("Set of tasks S_TASKS: ", S_TASKS)
print("Set of units S_UNITS: ", S_UNITS)
print("Set of material S_MATERIALS: ", S_MATERIALS)
print("Set of time points S_TIME: ", S_TIME)
print("Parameter TASK_UNIT assignment P_TASK_UNIT: ", P_TASK_UNIT)
print("Parameter with transitions related to each task P_TASKS_TRANSITIONS: ", P_TASKS_TRANSITIONS)
print("Parameter related to the consumption and production of each task P_TASKS_PROD_CONSUMP: ", P_TASKS_PROD_CONSUMP)
print("Parameter that connects transitions with production tasks and units P_TASK_TRANSITIONS_UNIT: ", P_TASK_TRANSITIONS_UNIT)
print("Set of all continuos tasks S_I_Continuos_Tasks: ", S_I_Continuos_Tasks)
print("Set of production tasks S_I_Production_Tasks: ", S_I_Production_Tasks)
print("Set of production tasks without S_I_Production_Tasks_Without_Transition: ", S_I_Production_Tasks_Without_Transition)
print("Set of production tasks with transition S_I_Production_Tasks_With_Transition: ", S_I_Production_Tasks_With_Transition)
print("Set of production tasks with direct transitions S_I_Production_Tasks_With_Direct_Transition: ", S_I_Production_Tasks_With_Direct_Transition)
print("Set of production tasks with indirect transitions S_I_Production_Tasks_With_Indirect_Transition: ", S_I_Production_Tasks_With_Indirect_Transition) 
print("Set of all transition tasks S_I_All_Transition_Tasks: ", S_I_All_Transition_Tasks)
print("Set of direct transition tasks S_I_Direct_Transition_Tasks: ", S_I_Direct_Transition_Tasks)
print("Set of indirect transition tasks S_I_Indirect_Transition_Tasks: ", S_I_Indirect_Transition_Tasks)
print("Set of indirect transition to production tasks (startup) S_I_Startup_Tasks: ", S_I_Startup_Tasks)
print("Set of indirect transition to idle (shutdown) S_I_Shutdown_Tasks: ", S_I_Shutdown_Tasks)
print("Set of materials consumed by task i S_K_CONSUMED_BY_I: ", S_K_CONSUMED_BY_I)
print("Set of materials produced by task i S_K_PRODUCED_BY_I: ", S_K_PRODUCED_BY_I)
print("Set of tasks consuming material k S_I_CONSUMING_K: ", S_I_CONSUMING_K)
print("Set of tasks producing material k S_I_PRODUCING_K: ", S_I_PRODUCING_K) 
print("Set of units j able to execute task i S_J_Executing_I: ", S_J_Executing_I)
print("Set of tasks executed in each unit j S_I_In_J: ", S_I_In_J)
print("Set of units without transitions S_J_Units_Without_Transition_Tasks: ", S_J_Units_Without_Transition_Tasks)
print("Set of units with direct transitions S_J_Units_With_Direct_Transition_Tasks: ", S_J_Units_With_Direct_Transition_Tasks) 
print("Set of units with idle (with shutdowns) S_J_Units_With_Shutdown_Tasks: ", S_J_Units_With_Shutdown_Tasks) 
print("Set of final products S_K_Final_Products: ", S_K_Final_Products) 
print("Set of intermediates S_K_Intermediates: ", S_K_Intermediates) 

# Lower and upper bounds for batch size of tasks.
P_Bmax = {(i,j): UNIT_TASKS[(j,i)]['Bmax'] for (j,i) in UNIT_TASKS}
P_Bmin = {(i,j): UNIT_TASKS[(j,i)]['Bmin'] for (j,i) in UNIT_TASKS}

# P_rho_MINUS[i,k] is the input fraction of material k consumed by task i.
P_rho_MINUS = {(i,k): ST_ARCS[(k,i)]['rho'] for (k,i) in ST_ARCS}

# P_rho_PLUS[i,k] is the output fraction of material k produced by task i.
P_rho_PLUS = {(i,k): TS_ARCS[(i,k)]['rho'] for (i,k) in TS_ARCS}

# Min and max lenghts of a run.
P_Tau_Min = {(i,j): UNIT_TASKS[(j,i)]['tau_min'] for (j,i) in UNIT_TASKS if i in S_I_Production_Tasks}
P_Tau_Max = {(i,j): UNIT_TASKS[(j,i)]['tau_max'] for (j,i) in UNIT_TASKS if i in S_I_Production_Tasks}

# P_Chi[k] is the storage capacity of each material.
P_Chi = {k: STATES[k]['capacity'] for k in STATES}

# Demand. Equivalent to xi.
P_K_Demand = {(k,n): STATES_SHIPMENT[(k,n)]['demand'] for (k,n) in STATES_SHIPMENT}

# Number of periods for transition, startup and shutdown.
P_Tau = {(i,j): UNIT_TASKS[(j,i)]['tau'] for (j,i) in UNIT_TASKS}

# Unit initialization.
P_Unit_Init = {(j): 1 for j in S_UNITS}

# Startup Cost
P_StarUp_Cost = {(j,i): UNIT_TASKS[(j,i)]['sCost'] for (j,i) in UNIT_TASKS}

print("Min batch size of task in unit P_Bmin: ", P_Bmin)
print("Max batch size of task in unit P_Bmax: ", P_Bmax) 
print("Conversion coefficient of consumed materials P_rho_MINUS: ", P_rho_MINUS)
print("Conversion coefficient of produced materials P_rho_PLUS: ", P_rho_PLUS)
print("Minimum lengh of a run P_Tau_Min: ", P_Tau_Min)
print("Maximum lengh of a run P_Tau_Max: ",P_Tau_Max)
print("Storage capacity of each material P_Chi: ", P_Chi)
print('Demand for material P_K_Demand: ', P_K_Demand)
print("Time for executing a task P_Tau: ", P_Tau)
print("Unit initialization P_Unit_Init: ", P_Unit_Init)
print("Startup Cost P_StarUp_Cost: ", P_StarUp_Cost)

##############################################################################################
#                                       VARIABLES                                            #
##############################################################################################

model = ConcreteModel()


# V_X[i,j,n] = 1 if unit j processes (sub)task i at time point n.
model.V_X = Var(S_TASKS, S_UNITS, S_TIME, bounds = (0, 1), domain = Boolean)

# V_Y_End[i,j,n] = 1 if a run of a continuous task in unit j ends at time point n.
model.V_Y_End = Var(S_TASKS, S_UNITS, S_TIME, bounds = (0, 1), domain = Boolean)

# V_Y_Start[i,j,n] = 1 if a run of a continuous task in unit j starts at time point n.
model.V_Y_Start = Var(S_TASKS, S_UNITS, S_TIME, bounds = (0, 1), domain = Boolean)

# V_B[i,j,n] is the batch size assigned to task i in unit j at time n.
model.V_B = Var(S_TASKS, S_UNITS, S_TIME, domain = NonNegativeReals)

# V_S[k,n] is the inventory of material k in time n.
model.V_S = Var(S_MATERIALS, S_TIME, domain = NonNegativeReals)

# V_X_Hat[i,j,n] is 1 if unit j is in task mode i (ready to execute batch subtaks i_SB(i)) at time point n.
model.V_X_Hat = Var(S_TASKS, S_UNITS, S_TIME, bounds = (0, 1), domain = Boolean)

# V_X_Hat_Idle[j,n] is 1 if unit j is in idle mode at time point n.
model.V_X_Hat_Idle = Var(S_UNITS, S_TIME, bounds = (0, 1), domain = Boolean)

model.V_N_Unit = Var(S_UNITS, domain = Integers)

def variables_initialization(model):
    [model.V_X_Hat[i,j,n].fix(0) for i in S_TASKS for j in S_UNITS for n in S_TIME if n < H]   # model.V_X_Hat seams to have effect on the model.
    [model.V_X[i,j,n].fix(0) for i in S_TASKS for j in S_UNITS for n in S_TIME if n == H] # On the last period it can be maximum Y_End = 0.
    



variables_initialization(model)
######################################
#               Parameters           #
######################################

def material_demand(model, k, n):
    if (k,n) in STATES_SHIPMENT:
        return STATES_SHIPMENT[(k,n)]['demand']
    else:
        return 0

model.P_Init_Inventory_Material = Param(S_MATERIALS, initialize = STATES[k]['initial'])
model.P_Material_Demand = Param(S_MATERIALS, S_TIME, initialize = material_demand)
######################################
#               Constraint           #
######################################

# Lower bound on the batch size of all tasks.
def unit_capacity_lb_eq2(model, i, j, n):
    if (i,j) in P_TASK_UNIT:
        return model.V_X[i,j,n]*P_Bmin[i,j] <= model.V_B[i,j,n] 
    else:
        return Constraint.Skip    

# Upper bound on the batch size of all tasks.
def unit_capacity_ub_eq2(model, i, j, n):
    if (i,j) in P_TASK_UNIT:
        return model.V_B[i,j,n] <= model.V_X[i,j,n]*P_Bmax[i,j]
    else:
        return Constraint.Skip

def material_mass_balance_eq3(model, k, n):
    if STATES[k]['isRM'] == False:    
        return model.V_S[k,n] == ((model.V_S[k,n-1] if n >= 1 else 0) + (model.P_Init_Inventory_Material[k] if n == 0 else 0)
                                            + sum(
                                                P_rho_MINUS[i,k]*model.V_B[i,j,n] 
                                                for i in S_I_CONSUMING_K[k]
                                                for j in S_J_Executing_I[i] 
                                                #for (i,j) in P_TASK_UNIT 
                                                #if i in S_I_CONSUMING_K[k]
                                            )    
                                                                                        
                                            + sum(
                                                P_rho_PLUS[i,k]*model.V_B[i,j,n - P_Tau[i,j]] 
                                                for i in S_I_PRODUCING_K[k]
                                                for j in S_J_Executing_I[i] 
                                                #for (i,j) in P_TASK_UNIT
                                                #if i in S_I_PRODUCING_K[k] 
                                                #if t >= n - P_Tau[i,j] + 1 and t <= n
                                                if n - P_Tau[i,j] >= 0
                                            )
                                            - model.P_Material_Demand[k,n]
        )
    else:
        return Constraint.Skip

def track_idle_unit_eq13(model, j, n):
    if j in S_J_Units_With_Shutdown_Tasks:
        return model.V_X_Hat_Idle[j,n] == ((model.V_X_Hat_Idle[j,n-1] if n >= 1 else 0)
                                         + (P_Unit_Init[j] if n == 0 else 0)  
                                         + sum(
                                            model.V_X[i,j,n-P_Tau[i,j]] 
                                            for i in S_I_Indirect_Transition_Tasks
                                            #if (i,j) in P_TASK_UNIT 
                                            if P_TASK_UNIT.get((i,j)) == -1
                                            if n-P_Tau[i,j] >= 0
                                         ) 
                                         - sum(
                                            model.V_X[i,j,n] 
                                            for i in S_I_Indirect_Transition_Tasks
                                            #if (i,j) in P_TASK_UNIT 
                                            if P_TASK_UNIT.get((i,j)) == 1                                            
                                         )
        )                                         
    else:
        return Constraint.Skip

def track_transitions_unit_eq12(model, i, j, n):
    if i in S_I_Production_Tasks and j in S_J_Executing_I[i]:
        return model.V_X_Hat[i,j,n] == (
                                          (model.V_X_Hat[i,j,n-1] if n >= 1 else 0) 
                                        + (model.V_X[i,j,n-1] if n >= 1 else 0)
                                        
                                        + sum(model.V_X[ii,j,n-P_Tau[ii,j]] 
                                            for ii in S_I_Startup_Tasks
                                            if (j,i,ii) in P_TASK_TRANSITIONS_UNIT 
                                            #if P_TASK_TRANSITIONS_UNIT.get((j,i,ii)) == 1
                                            #if ii in S_I_Startup_Tasks
                                            if n - P_Tau[ii,j] >= 0
                                        )
                                        - model.V_X[i,j,n]
                                        - sum(
                                            model.V_X[ii,j,n] 
                                            for ii in S_I_Shutdown_Tasks
                                            if (j,i,ii) in P_TASK_TRANSITIONS_UNIT 
                                            #if P_TASK_TRANSITIONS_UNIT.get((j,i,ii)) == -1
                                            #if ii in S_I_Indirect_Transition_Tasks    
                                            #if ii not in S_I_Startup_Tasks
                                        )
        )                                         
    else:
        return Constraint.Skip


def track_transitions_unit_eq15(model, i, j, n):
    if j in (S_J_Units_With_Direct_Transition_Tasks or S_J_Units_With_Shutdown_Tasks) and (i,j) in P_TASK_UNIT and i in S_I_Production_Tasks:
        return model.V_X_Hat[i,j,n] == ((model.V_X_Hat[i,j,n-1] if n >= 1 else 0)
                                         + (model.V_X[i,j,n-1] if n >= 1 else 0)
                                         - model.V_X[i,j,n]
                                         + sum(
                                            model.V_X[ii,j,n-P_Tau[ii,j]] 
                                            for ii in S_I_Direct_Transition_Tasks
                                            #if (j,i,ii) in P_TASK_TRANSITIONS_UNIT 
                                            if P_TASK_TRANSITIONS_UNIT.get((j,i,ii)) == 1
                                            #if ii in S_I_Direct_Transition_Tasks
                                            if n >= P_Tau[ii,j]
                                         ) 
                                         - sum(
                                            model.V_X[ii,j,n] 
                                            for ii in S_I_Direct_Transition_Tasks
                                            #if (j,i,ii) in P_TASK_TRANSITIONS_UNIT 
                                            if P_TASK_TRANSITIONS_UNIT.get((j,i,ii)) == -1
                                            if ii in S_I_Direct_Transition_Tasks
                                         )
                                         + sum(
                                            model.V_X[ii,j,n-P_Tau[ii,j]] 
                                            for ii in S_I_Startup_Tasks
                                            #if (j,i,ii) in P_TASK_TRANSITIONS_UNIT 
                                            if P_TASK_TRANSITIONS_UNIT.get((j,i,ii)) == 1
                                            #if ii in S_I_Startup_Tasks
                                            if n >= P_Tau[ii,j]
                                         )
                                         - sum(
                                            model.V_X[ii,j,n] 
                                            for ii in S_I_Shutdown_Tasks
                                            #if (j,i,ii) in P_TASK_TRANSITIONS_UNIT 
                                            if P_TASK_TRANSITIONS_UNIT.get((j,i,ii)) == -1
                                            #if ii in S_I_Indirect_Transition_Tasks    
                                            #if ii not in S_I_Startup_Tasks
                                         )
        )                                         
    else:
        return Constraint.Skip

# Tracks the start and end of all production tasks.    
def track_start_end_production_task_eq16(model, i, j, n):
    #if (i,j) in P_TASK_UNIT and i in S_I_Production_Tasks and j in S_J_Executing_I[i]:
    if i in S_I_Production_Tasks and j in S_J_Executing_I[i]:
        return model.V_Y_Start[i,j,n] == model.V_X[i,j,n] - (model.V_X[i,j,n-1] if n >= 1 else 0) + model.V_Y_End[i,j,n]
    else:
        return Constraint.Skip

def track_start_end_batch_task_eq17(model, i, j, n):
    #if (i,j) in P_TASK_UNIT and i in S_I_Production_Tasks and j in S_J_Executing_I[i]:
    if i in S_I_Production_Tasks and j in S_J_Executing_I[i]:
        return model.V_Y_Start[i,j,n] + model.V_Y_End[i,j,n] <= 1
    else:
        return Constraint.Skip

def min_lenght_run_eq18(model, i, j, n):
    if (i,j) in P_TASK_UNIT and i in S_I_Production_Tasks:
        return model.V_X[i,j,n] >= sum(
                                        model.V_Y_Start[i,j,nprime] 
                                        for nprime in S_TIME 
                                        if (nprime >= n - P_Tau_Min[i,j] + 1 and nprime <= n)
                                      )    
    else:
        return Constraint.Skip

def max_lenght_run_eq19(model, i, j, n):
    if (i,j) in P_TASK_UNIT and i in S_I_Production_Tasks:
        return sum(
                    model.V_X[i,j,nprime] 
                    for nprime in S_TIME 
                    if (nprime >= n - P_Tau_Max[i,j] and nprime <= n)
                  ) <= P_Tau_Max[i,j] 
    else:
        return Constraint.Skip

def max_lenght_run_eq19_reformulation(model, i, j, n):
    if (i,j) in P_TASK_UNIT and i in S_I_Production_Tasks:
        return model.V_X[i,j,n] <= sum(model.V_Y_End[i,j,nprime] for nprime in S_TIME if ( (nprime >= n + 1) and (nprime <= n + P_Tau_Max[i,j]) )) 
    else:
        return Constraint.Skip

def track_start_production_task_after_transition_eq20(model, i, j, n):
    #if (i,j) in P_TASK_UNIT and i in S_I_Production_Tasks_With_Transition:
    if i in S_I_Production_Tasks_With_Transition and j in S_J_Executing_I[i]:
        return (
            model.V_X[i,j,n] 
            >= 
            sum(
                model.V_X[ii,j,nprime-P_Tau[ii,j]] 
                for ii in S_I_All_Transition_Tasks
                #if (i,ii) in P_TASKS_TRANSITIONS 
                if P_TASKS_TRANSITIONS.get((i,ii)) == 1
                for nprime in S_TIME
                if ((nprime >= n - P_Tau_Min[i,j] + 1) and (nprime <= n))  
                if nprime-P_Tau[ii,j] >= 0              
            )
        )
    else:
        return Constraint.Skip

def unit_availability_eq21(model, j, n):
    return (
        sum(
            model.V_X[i,j,nprime] 
            for i in S_TASKS
            if (i,j) in P_TASK_UNIT 
            for nprime in S_TIME 
            if ((nprime >= n - P_Tau[i,j] + 1) and (nprime <= n))
      ) 
      + sum(
            model.V_X_Hat[i,j,n] 
            for i in (S_I_Production_Tasks_With_Transition)
            if i in S_I_In_J[j]
      )
      + (model.V_X_Hat_Idle[j,n] if j in S_J_Units_With_Shutdown_Tasks else 0)

    ) <= 1

def material_capacity(model, k, n):
    return model.V_S[k,n] <= P_Chi[k]

def unit_activity_track(model, j):
    
    return model.V_N_Unit[j] == sum(model.V_X[i,j,n] for i in S_I_Production_Tasks if (i,j) in P_TASK_UNIT for n in S_TIME)
    
def unit_activity_bound(model, j):
    
    return model.V_N_Unit[j] <= floor(H/(min(P_Tau[i,j] for i in S_I_Production_Tasks if (i,j) in P_TASK_UNIT)))

def y_end_upper_bound(model, k):
    if STATES[k]['isProd'] == True:
        return sum(model.V_Y_End[i,j,n]*P_Bmin[i,j]*P_Tau_Min[i,j] for i in (S_I_PRODUCING_K[k] & S_I_Production_Tasks) for j in S_J_Executing_I[i] for n in S_TIME if n <= P_Largest_Demand_Point if (i,j) in P_TASK_UNIT) <= sum(P_K_Demand[k,n] for n in S_TIME if (k,n) in STATES_SHIPMENT)  
    else:
        return Constraint.Skip

def y_start_upper_bound(model, k):
    if STATES[k]['isProd'] == True:
        return sum(model.V_Y_Start[i,j,n]*P_Bmin[i,j]*P_Tau_Min[i,j] for i in (S_I_PRODUCING_K[k] & S_I_Production_Tasks) for j in S_J_Executing_I[i] for n in S_TIME if n <= P_Largest_Demand_Point if (i,j) in P_TASK_UNIT) <= sum(P_K_Demand[k,n] for n in S_TIME if (k,n) in STATES_SHIPMENT)  
    else:
        return Constraint.Skip

def x_production_upper_bound(model, k):
    if STATES[k]['isProd'] == True:
        return sum(model.V_X[i,j,n]*P_Bmin[i,j] for i in (S_I_PRODUCING_K[k] & S_I_Production_Tasks) for j in S_J_Executing_I[i] for n in S_TIME if n <= P_Largest_Demand_Point if (i,j) in P_TASK_UNIT) <= sum(P_K_Demand[k,n] for n in S_TIME if (k,n) in STATES_SHIPMENT)  
    else:
        return Constraint.Skip

def y_start_lower_bound(model, k):
    if STATES[k]['isProd'] == True:
        return sum(model.V_Y_Start[i,j,n]*P_Bmax[i,j]*P_Tau_Max[i,j] for i in (S_I_PRODUCING_K[k] & S_I_Production_Tasks) for j in S_J_Executing_I[i] for n in S_TIME if n <= P_Largest_Demand_Point if (i,j) in P_TASK_UNIT) >= sum(P_K_Demand[k,n] for n in S_TIME if (k,n) in STATES_SHIPMENT)  
    else:
        return Constraint.Skip

def y_end_lower_bound(model, k):
    if STATES[k]['isProd'] == True:
        return sum(model.V_Y_End[i,j,n]*P_Bmax[i,j]*P_Tau_Max[i,j] for i in (S_I_PRODUCING_K[k] & S_I_Production_Tasks) for j in S_J_Executing_I[i] for n in S_TIME if n <= P_Largest_Demand_Point if (i,j) in P_TASK_UNIT) >= sum(P_K_Demand[k,n] for n in S_TIME if (k,n) in STATES_SHIPMENT)  
    else:
        return Constraint.Skip
   
def x_production_lower_bound(model, k):
    if STATES[k]['isProd'] == True:
        return sum(model.V_X[i,j,n]*P_Bmax[i,j] for i in (S_I_PRODUCING_K[k] & S_I_Production_Tasks) for j in S_J_Executing_I[i] for n in S_TIME if n <= P_Largest_Demand_Point if (i,j) in P_TASK_UNIT) >= sum(P_K_Demand[k,n] for n in S_TIME if (k,n) in STATES_SHIPMENT)  
    else:
        return Constraint.Skip
    
def if_start_end(model, i, j, n):
    if (i in S_I_Production_Tasks) and (i,j) in P_TASK_UNIT and (n <= H - P_Tau_Max[i,j]):
        return sum(model.V_Y_End[i,j,nprime] for nprime in S_TIME if nprime >= n + P_Tau_Min[i,j] and nprime <= n + P_Tau_Max[i,j]) >= model.V_Y_Start[i,j,n]
    else:
        return Constraint.Skip

def forward_propagation_inequality(model, i):
    if (i in S_I_Production_Tasks): 
        return sum(model.V_B[i,j,n] for n in S_TIME for j in S_J_Executing_I[i] if (i,j) in P_TASK_UNIT) <= model.mu_adjusted[i]        
    else:
        return Constraint.Skip

def objective(model):
   
   fix_operational_cost = sum(UNIT_TASKS[(j,i)]['Cost']*model.V_X[i,j,n] for (i,j) in P_TASK_UNIT for n in S_TIME)
   variable_operational_cost = sum(UNIT_TASKS[(j,i)]['vCost']*model.V_B[i,j,n] for (i,j) in P_TASK_UNIT for n in S_TIME)
   startup_cost = sum(model.V_Y_Start[i,j,n]*P_StarUp_Cost[j,i] for (i,j) in P_TASK_UNIT for n in S_TIME)
   shutdown_cost = sum(model.V_Y_End[i,j,n]*P_StarUp_Cost[j,i] for (i,j) in P_TASK_UNIT for n in S_TIME)
   total_cost = fix_operational_cost + variable_operational_cost + startup_cost + shutdown_cost
   production_revenue = sum(STATES[k]['price']*model.V_S[k,n] for n in S_TIME for k in S_MATERIALS if STATES[k]['isProd'] == True)
   makespan = sum(n*model.V_X[i,j,n] for (i,j) in P_TASK_UNIT for n in S_TIME)
   
   return (production_revenue)

#######################################################
#                  Basic Model                        #
#######################################################

model.C_Unit_Capacity_LB_Eq2 = Constraint(S_TASKS, S_UNITS, S_TIME, rule = unit_capacity_lb_eq2)
model.C_Unit_Capacity_UB_Eq2 = Constraint(S_TASKS, S_UNITS, S_TIME, rule = unit_capacity_ub_eq2)
model.C_Material_Mass_Balance_Eq3 = Constraint(S_MATERIALS, S_TIME, rule = material_mass_balance_eq3)
#model.C_Track_Startup_Shutdown_Eq12 = Constraint(S_TASKS, S_UNITS, S_TIME, rule = track_transitions_unit_eq12)
model.C_Track_Idle_Unit_Eq13 = Constraint(S_UNITS, S_TIME, rule = track_idle_unit_eq13)
model.C_Track_Transitions_units_Eq15 = Constraint(S_TASKS, S_UNITS, S_TIME, rule = track_transitions_unit_eq15)
model.C_Track_Start_End_Batch_Task_Eq16 = Constraint(S_TASKS, S_UNITS, S_TIME, rule = track_start_end_production_task_eq16)
model.C_Track_Start_End_Batch_Task_Eq17 = Constraint(S_TASKS, S_UNITS, S_TIME, rule = track_start_end_batch_task_eq17)
model.C_Min_Lenght_Run_Eq18 = Constraint(S_TASKS, S_UNITS, S_TIME, rule = min_lenght_run_eq18)
model.C_Max_Lenght_Run_Eq19 = Constraint(S_TASKS, S_UNITS, S_TIME, rule = max_lenght_run_eq19)
model.C_Track_Start_Production_Task_After_Transition_Eq20 = Constraint(S_TASKS, S_UNITS, S_TIME, rule = track_start_production_task_after_transition_eq20)
model.C_Unit_Availability_Eq21 = Constraint(S_UNITS, S_TIME, rule = unit_availability_eq21)
model.C_Material_Availability = Constraint(S_MATERIALS, S_TIME, rule = material_capacity)
model.C_Objective = Objective(expr = objective, sense = maximize)

#######################################################
#              Tightening Constraints                 #
#######################################################

#model.C_Max_Lenght_Run_Eq19_Reformulation = Constraint(S_TASKS, S_UNITS, S_TIME, rule = max_lenght_run_eq19_reformulation)
#model.If_Start_End = Constraint(S_TASKS, S_UNITS, S_TIME, rule = if_start_end)

#model.Y_Start_Lower_Bound = Constraint(S_MATERIALS, rule = y_start_lower_bound)
#model.Y_End_Lower_Bound = Constraint(S_MATERIALS, rule = y_end_lower_bound)
#model.X_Prod_Lower_Bound = Constraint(S_MATERIALS, rule = x_production_lower_bound)

#model.Y_Start_Upper_Bound = Constraint(S_MATERIALS, rule = y_start_upper_bound)
#model.Y_End_Upper_Bound = Constraint(S_MATERIALS, rule = y_end_upper_bound)
#model.X_Prod_Upper_Bound = Constraint(S_MATERIALS, rule = x_production_upper_bound)

#model.Forward_Propagation_Inequality = Constraint(S_TASKS, rule = forward_propagation_inequality)

######################################
#         Forward Propagation        # 
######################################

model.I_Exp = Set()  # Tasks that have been explored.
model.K_Exp = Set()  # Material that have been explored.
model.K_To_Be_Exp = Set()  # Material that have been explored.
model.theta = Param(S_TASKS, S_UNITS, mutable = True, initialize = H)  # Operational time windown for each (i,j).
model.omega = Param(S_MATERIALS, mutable = True, initialize = -1000)  # Maximum cumulative production.
model.mu = Param(S_TASKS, mutable = True, initialize = 0)  # Total production of task i within a planning horizon.       
model.mu_tw = Param(S_TASKS, mutable = True, initialize = 0)  # Total production of task in a time windown.
model.mu_adjusted = Param(S_TASKS, mutable = True, initialize = 0)  # Adjusted value of mu due to production intervals. 
model.epsilon_max = Param(S_UNITS, mutable = True, initialize = 0)  # Maximum number of runs in a unit

def foward_propagation(model):
    
    # Initialize omega with initial inventories and k and i to control elements to be explored.
    print("---------------------------------INITIALIZATION-------------------------------------------")
    print("Initialize omega with initial inventories.")
    print("Initialize sets I_exp and K_exp for materials with initial inventories and tasks that consume them.")
    
    for k in S_MATERIALS:
        
        if STATES[k]['initial'] > 0:
            model.omega[k] = STATES[k]['initial']
            print(f"Omega[{k}] = {model.omega[k].value}.")            
            model.K_To_Be_Exp.add(k)

            #for i in (S_I_CONSUMING_K[k] & S_I_Production_Tasks):
            #    model.I_Exp.add(i)    

        print(f"K_Exp = {model.K_To_Be_Exp.data()}.")
        print(f"I_Exp = {model.I_Exp.data()}.")        
        print("------------------------------------------------------------------------------------------\n")

    for k in S_MATERIALS:
        
        if k in model.K_To_Be_Exp:
            
            # Calculate batch combinations and capacities
            batch_combinations = {}
            combined_capacities = {}
            best_difference = float('inf')

            for i in (S_I_CONSUMING_K[k] & S_I_Production_Tasks):
                print(f"\n\n\t------------------------------Max Cumulative Amount for {i}-{k}------------------------------\n")

                # To Do: this for tasks without SU, SD, ST. Add them latter
                # To Do: what if I have less raw material then my production capacity

                # Since we the floor to have an integer number of runs, this is necessary to catch situation where I can have more runs (and production) considering P_Tau_Min.
                model.mu_tw[i] = min( -(model.omega[k].value/P_rho_MINUS[i,k]), max( 
                                                                    -sum(P_rho_MINUS[i,k]*P_Tau_Max[i,j]*P_Bmax[i,j]*floor(model.theta[i,j].value/(1+P_Tau[i,j]*P_Tau_Max[i,j])) for j in S_J_Executing_I[i]), 
                                                                    -sum(P_rho_MINUS[i,k]*P_Tau_Min[i,j]*P_Bmax[i,j]*floor(model.theta[i,j].value/(1+P_Tau[i,j]*P_Tau_Min[i,j])) for j in S_J_Executing_I[i])
                                                                )
                                    )    
                model.mu[i] = model.mu_tw[i]

                print(f"\tMax cumulative amount for {i} in a time windows mu_tw = {model.mu_tw[i].value}")
                print(f"\tMax cumulative amount for {i} in the planning horizon mu = {model.mu[i].value}")

                for j in S_J_Executing_I[i]:
                    print(f"\n\t\t-------------------Max Number Runs {j}-{i}-------------------")
                    
                    # To Do: define the right denominator (P_Tau_Max and/or P_Tau_Min)
                    # To Do: this for tasks without SU, SD, ST. Add them latter
                    model.epsilon_max[j] = ceil(model.mu[i] / (P_Tau_Max[i,j]*P_Bmax[i,j]))
                    print(f"\t\tMaximum number of runs of task {i} in unit {j} epsilon_max = {model.epsilon_max[j].value}")

                print("\n")

                max_runs = [range(0, value(model.epsilon_max[j]) + 1) for j in S_J_Executing_I[i]]
                combinations = list(product(*max_runs))
                batch_combinations[i] = combinations

                combined_capacities[i] = {
                    combo: {
                        'min_capacity': sum(P_Tau_Min[i,j] * P_Bmin[i,j] * combo[c] for (c,j) in enumerate(S_J_Executing_I[i])),
                        'max_capacity': sum(P_Tau_Max[i,j] * P_Bmax[i,j] * combo[c] for (c,j) in enumerate(S_J_Executing_I[i]))
                    }
                    for combo in combinations
                }  
                
                #for combo in combinations:
                    #for c, j in enumerate(S_J_Executing_I[i]):
                        #print(f"\tTask {i}, c: {c}, j: {j}, production combination = {combo[c]} runs")
                
                for combo, capacities in combined_capacities[i].items():
                    min_capacity = capacities['min_capacity']
                    max_capacity = capacities['max_capacity']
            
                    # Check if mu is within the range
                    if min_capacity <= model.mu[i].value <= max_capacity:
                        model.mu_adjusted[i] = model.mu[i].value  # Return immediately if a match is found
                        #print(f"\tBounded by max capacity = {max_capacity}")
                        break

                    # Otherwise, find the closest max_capacity
                    if abs(max_capacity - model.mu[i].value) < best_difference and max_capacity <= model.mu[i].value:
                        best_difference = abs(max_capacity - model.mu[i].value)
                        model.mu_adjusted[i] = max_capacity
                                        
                print("\n")

                print(f"\tTask {i} has the following feasible production intervals:")
                for combo, capacities in combined_capacities[i].items():
                    print(f"\t\tCombination: {combo} -> Min: {capacities['min_capacity']}, Max: {capacities['max_capacity']}")

                print(f"\tThe calculated mu for task {i} is: {model.mu[i].value}. Its adjusted mu for {i} is: {model.mu_adjusted[i].value}")

                model.I_Exp.add(i)  

        model.K_Exp.add(k)
        model.K_To_Be_Exp.remove(k)

        for i in model.I_Exp:
            for k in S_K_PRODUCED_BY_I[i]:
                if S_K_CONSUMED_BY_I[i] in model.K_Exp:
                    model.K_To_Be_Exp.add(k)
        print(f"K_To_Be_Exp = {model.K_To_Be_Exp.data()}.")

        for k in model.K_Exp:
            if model.omega[k].value < 0:
                model.omega[k] = min(sum(P_rho_PLUS[i,k] * model.mu_adjusted[i].value for i in (S_I_PRODUCING_K[k] & model.I_Exp)), max(model.mu_adjusted[i].value for i in (S_I_PRODUCING_K[k] & model.I_Exp)))
                print(f"The maximum cumulative production (propagate inventory) for material {k} is {model.omega[k].value}.")

        if model.K_Exp == S_MATERIALS and model.I_Exp == (S_I_Production_Tasks):
            print('All materials and tasks have been explored.')
            break





    """ for k in S_MATERIALS: 
        
        # Calculate batch combinations and capacities
        batch_combinations = {}
        combined_capacities = {}
        best_difference = float('inf')
        
        if k in model.K_Exp:
            
            for i in (S_I_CONSUMING_K[k] & S_I_Production_Tasks):
                print(f"\n\n\t------------------------------Max Cumulative Amount for {i}-{k}------------------------------\n")

                # To Do: this for tasks without SU, SD, ST. Add them latter
                # To Do: what if I have less raw material then my production capacity

                # Since we the floor to have an integer number of runs, this is necessary to catch situation where I can have more runs (and production) considering P_Tau_Min.
                model.mu_tw[i] = min( -(model.omega[k].value/P_rho_MINUS[i,k]), max( 
                                                                    -sum(P_rho_MINUS[i,k]*P_Tau_Max[i,j]*P_Bmax[i,j]*floor(model.theta[i,j].value/(1+P_Tau[i,j]*P_Tau_Max[i,j])) for j in S_J_Executing_I[i]), 
                                                                    -sum(P_rho_MINUS[i,k]*P_Tau_Min[i,j]*P_Bmax[i,j]*floor(model.theta[i,j].value/(1+P_Tau[i,j]*P_Tau_Min[i,j])) for j in S_J_Executing_I[i])
                                                                )
                                    )    
                model.mu[i] = model.mu_tw[i]

                print(f"\tMax cumulative amount for {i} in a time windows mu_tw = {model.mu_tw[i].value}")
                print(f"\tMax cumulative amount for {i} in the planning horizon mu = {model.mu[i].value}")

                for j in S_J_Executing_I[i]:
                    print(f"\n\t\t-------------------Max Number Runs {j}-{i}-------------------")
                    
                    # To Do: define the right denominator (P_Tau_Max and/or P_Tau_Min)
                    # To Do: this for tasks without SU, SD, ST. Add them latter
                    model.epsilon_max[j] = ceil(model.mu[i] / (P_Tau_Max[i,j]*P_Bmax[i,j]))
                    print(f"\t\tMaximum number of runs of task {i} in unit {j} epsilon_max = {model.epsilon_max[j].value}")

                print("\n")

                max_runs = [range(0, value(model.epsilon_max[j]) + 1) for j in S_J_Executing_I[i]]
                combinations = list(product(*max_runs))
                batch_combinations[i] = combinations

                combined_capacities[i] = {
                    combo: {
                        'min_capacity': sum(P_Tau_Min[i,j] * P_Bmin[i,j] * combo[c] for (c,j) in enumerate(S_J_Executing_I[i])),
                        'max_capacity': sum(P_Tau_Max[i,j] * P_Bmax[i,j] * combo[c] for (c,j) in enumerate(S_J_Executing_I[i]))
                    }
                    for combo in combinations
                }  
                
                #for combo in combinations:
                    #for c, j in enumerate(S_J_Executing_I[i]):
                        #print(f"\tTask {i}, c: {c}, j: {j}, production combination = {combo[c]} runs")
                
                for combo, capacities in combined_capacities[i].items():
                    min_capacity = capacities['min_capacity']
                    max_capacity = capacities['max_capacity']
            
                    # Check if mu is within the range
                    if min_capacity <= model.mu[i].value <= max_capacity:
                        model.mu_adjusted[i] = model.mu[i].value  # Return immediately if a match is found
                        #print(f"\tBounded by max capacity = {max_capacity}")
                        break

                    # Otherwise, find the closest max_capacity
                    if abs(max_capacity - model.mu[i].value) < best_difference and max_capacity <= model.mu[i].value:
                        best_difference = abs(max_capacity - model.mu[i].value)
                        model.mu_adjusted[i] = max_capacity
                                        
                print("\n")

                print(f"\tTask {i} has the following feasible production intervals:")
                for combo, capacities in combined_capacities[i].items():
                    print(f"\t\tCombination: {combo} -> Min: {capacities['min_capacity']}, Max: {capacities['max_capacity']}")

                print(f"\tThe calculated mu for task {i} is: {model.mu[i].value}. Its adjusted mu for {i} is: {model.mu_adjusted[i].value}")
            
                

        for i in model.I_Exp:
            for k in S_K_PRODUCED_BY_I[i]:
                model.K_Exp.add(k)
        print(f"K_exp = {model.K_Exp.data()}.")
        
        for k in model.K_Exp:
            if model.omega[k].value == 0:
                model.omega[k] = min(sum(P_rho_PLUS[i,k] * model.mu_adjusted[i].value for i in (S_I_PRODUCING_K[k] & model.I_Exp)), max(model.mu_adjusted[i].value for i in (S_I_PRODUCING_K[k] & model.I_Exp)))
                print(f"The maximum cumulative production (propagate inventory) for material {k} is {model.omega[k].value}.")

        if model.K_Exp == S_MATERIALS and model.I_Exp == (S_I_Production_Tasks):
            print('All materials and tasks have been explored.')
            break """


foward_propagation(model)

try:
    solver = SolverFactory('gurobi')
    set_solver_options(solver)
    results = solver.solve(model, tee = True)
    results.write()

except:

    print(f"Error")
   
#for con in model.component_map(Constraint).itervalues():
#    con.pprint()
  
 
plt.figure(figsize=(12,6))

gap = (H+1)/500
idx = 1
lbls = []
ticks = []
for j in sorted(S_UNITS):
    idx -= 1
    for i in sorted(S_I_In_J[j]):
        idx -= 1
        ticks.append(idx)
        lbls.append("{0:s} -> {1:s}".format(j,i))
        plt.plot([0,H+5],[idx,idx],lw=20,alpha=.3,color='y')
        for t in S_TIME:
            if model.V_X[i,j,t]() > 0.0001:
                plt.plot([t+gap,t+P_Tau[i,j]-gap], [idx,idx],'b', lw=20, solid_capstyle='butt')
                txt = "{0:.2f}".format(model.V_B[i,j,t]())
                plt.text(t+P_Tau[i,j]/2, idx, txt, color='white', weight='bold', ha='center', va='center')
plt.xlim(0,H)
plt.gca().set_yticks(ticks)
plt.gca().set_yticklabels(lbls);

#x = [1, 1]
#plt.plot(x)
#plt.show()

plt.figure(figsize=(10,6))
for (k,idx) in zip(STATES.keys(),range(0,len(STATES.keys()))):
    plt.subplot(ceil(len(STATES.keys())/3),3,idx+1)
    tlast,ylast = 0,STATES[k]['initial']
    for (t,y) in zip(list(TIME),[model.V_S[k,t]() for t in TIME]):
        plt.plot([tlast,t,t],[ylast,ylast,y],'b')
        #plt.plot([tlast,t],[ylast,y],'b.',ms=10)
        tlast,ylast = t,y
    plt.ylim(0,1.1*P_Chi[k])
    plt.plot([0,H],[P_Chi[k],P_Chi[k]],'r--')
    plt.title(k)
plt.tight_layout()
plt.show(block=True)


# %%
