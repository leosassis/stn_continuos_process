##########################################################
#The current model has no utility constraints.           # 
#It assumes no storage restrictions.                     #
#It assumes unlimited amount of raw materials            #
#It assume no delays: idis, idly, rmi_dly, rmi_n         #
#It assumes no batch units: j_b                          #
#There is no pre-defined tasks for n=0: i_ini            #
#It assumes a simplified objectie function               #
##########################################################

import matplotlib.pyplot as plt 
import numpy as np 
import pandas as pd 
from IPython.display import display, HTML
from pyomo.environ import *


H = 10

Network = {
    # time grid
    'TIME':  range(0, H+1),
    
    # states
    'STATES': {
        'RM'     : {'capacity': 10000, 'initial': 200, 'price':  0, 'isRM': True, 'isIntermed': False, 'isProd': False},
        'IA1'    : {'capacity': 500, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},
        'IA2'    : {'capacity': 500, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},
        'IA3'    : {'capacity': 500, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},
    },

    'STATES_SHIPMENT': {
        ('IA1', 10) : {'demand': 15.0},
    },
    
    # state-to-task arcs indexed by (state, task)
    'ST_ARCS': {
        ('RM', 'TA1') : {'rho': -1.0},
        ('RM', 'TA2') : {'rho': -1.0},
        ('RM', 'TA3') : {'rho': -1.0},
        ('RM', 'TA3I') : {'rho': -1.0},
        ('RM', 'ITA3') : {'rho': -1.0},
    },
    
    # task-to-state arcs indexed by (task, state)
    'TS_ARCS': {
        ('TA1', 'IA1') : {'dur': 1, 'rho': 1.0, 'prod_consump': 1},
        ('TA2', 'IA2') : {'dur': 1, 'rho': 1.0, 'prod_consump': 1},
        ('TA3', 'IA3') : {'dur': 1, 'rho': 1.0, 'prod_consump': 1},
        ('ITA3', 'IA3') : {'dur': 2, 'rho': 0.25, 'prod_consump': 1},
        ('TA3I', 'IA3') : {'dur': 1, 'rho': 0.5, 'prod_consump': 1},
    },
    
    # Tasks and their corresponding transition. 
    # Transition-To-Task = 1. Task-To-Transition = -1.
    # Equivalent to parameter ipits(i, ii) in the GAMS code.
    'TASKS_TRANSITION_TASKS': {
        ('TA3', 'ITA3') : {'isSU': True, 'isSD': False, 'isDirect': False, 'direction': 1},
        ('TA3', 'TA3I') : {'isSU': False, 'isSD': True, 'isDirect': False, 'direction': -1},
    },
    
    # unit data indexed by (unit, task)
    'UNIT_TASKS': {
        ('UA1', 'TA1') : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 3.5, 'Bmax': 3.5, 'Cost': 4, 'vCost': 1, 'direction': 1,},
        ('UA2', 'TA2') : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 2.1, 'Bmax': 2.1, 'Cost': 4, 'vCost': 1, 'direction': 1,},
        ('UA2', 'TA3') : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 2.1, 'Bmax': 2.1, 'Cost': 4, 'vCost': 1, 'direction': 1,},
        ('UA2', 'ITA3') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 2.8, 'Bmax': 2.8, 'Cost': 6, 'vCost': 1, 'direction': 1,},
        ('UA2', 'TA3I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 1.4, 'Bmax': 1.4, 'Cost': 3, 'vCost': 1, 'direction': -1,},
    },
}

STN = Network

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
P_TASKS_PROD_CONSUMP = {(i,k): TS_ARCS[(i,k)]['prod_consump'] for (i,k) in TS_ARCS} 

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
S_I_Indirect_Startup_Tasks = set([i for (ii,i) in TASKS_TRANSITION_TASKS if (TASKS_TRANSITION_TASKS[(ii,i)]['isDirect'] == False and TASKS_TRANSITION_TASKS[(ii,i)]['isSU'] == True) ]) 

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

# S_I_CONSUMING_K[k] is the set of tasks consuming material k. Equivalent to ijk_plus.
S_I_CONSUMING_K = {k: set() for k in STATES}
for (k,i) in ST_ARCS:
    S_I_CONSUMING_K[k].add(i)

# S_I_PRODUCING_K[k] is the set of tasks producing material k. Equivalent to ijk_plus.
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
print("Set of indirect transition to production tasks (startup) S_I_Indirect_Startup_Tasks: ", S_I_Indirect_Startup_Tasks)
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

print("Min batch size of task in unit P_Bmin: ", P_Bmin)
print("Max batch size of task in unit P_Bmax: ", P_Bmax) 

print("Conversion coefficient of consumed materials P_rho_MINUS: ", P_rho_MINUS)
print("Conversion coefficient of produced materials P_rho_PLUS: ", P_rho_PLUS)

print("Minimum lengh of a run P_Tau_Min: ", P_Tau_Min)
print("Maximum lengh of a run P_Tau_Max: ",P_Tau_Max)

print("Storage capacity of each material: ", P_Chi)
print('Demand for material: ', P_K_Demand)
print("Time for executing a task: ", P_Tau)

##############################################################################################
#                                       VARIABLES                                            #
##############################################################################################

model = ConcreteModel()

# V_X[i,j,n] = 1 if unit j processes (sub)task i at time point n.
model.V_X = Var(S_TASKS, S_UNITS, S_TIME, domain = Boolean)

# V_Y_End[i,j,n] = 1 if a run of a continuous task in unit j ends at time point n.
model.V_Y_End = Var(S_TASKS, S_UNITS, S_TIME, domain = Boolean)

# V_Y_Start[i,j,n] = 1 if a run of a continuous task in unit j starts at time point n.
model.V_Y_Start = Var(S_TASKS, S_UNITS, S_TIME, domain = Boolean)

# V_B[i,j,n] is the batch size assigned to task i in unit j at time n.
model.V_B = Var(S_TASKS, S_UNITS, S_TIME, domain = NonNegativeReals)

# V_S[k,n] is the inventory of material k in time n.
model.V_S = Var(S_MATERIALS, S_TIME, domain = NonNegativeReals)

# V_D[k,n] is the amount of material k shipped in time n.
model.V_D = Var(S_MATERIALS, S_TIME, domain = NonNegativeReals)

# V_X_Hat[i,j,n] is 1 if unit j is in task mode i (ready to execute batch subtaks i_SB(i)) at time point n.
model.V_X_Hat = Var(S_TASKS, S_UNITS, S_TIME, domain = Boolean)

# V_X_Hat_Idle[j,n] is 1 if unit j is in idle mode at time point n.
model.V_X_Hat_Idle = Var(S_UNITS, S_TIME, domain = Boolean)

######################################
#               Constraint           #
######################################

# Lower bound on the batch size of all tasks.
def unit_capacity_lb_eq2(model, i, j, n):
    if (i,j) in P_TASK_UNIT:
        return model.V_B[i,j,n] >= model.V_X[i,j,n]*P_Bmin[i,j]
    else:
        return Constraint.Skip    

# Upper bound on the batch size of all tasks.
def unit_capacity_ub_eq2(model, i, j, n):
    if (i,j) in P_TASK_UNIT:
        return model.V_B[i,j,n] <= model.V_X[i,j,n]*P_Bmax[i,j]
    else:
        return Constraint.Skip

def material_mass_balance_eq3(model, k, n):
    if n < H:    
        return model.V_S[k,n+1] == ((model.V_S[k,n] if (n >= 1 and n < H) else STATES[k]['initial']) 
                                        + sum(
                                            P_rho_MINUS[i,k]*model.V_B[i,j,nprime] 
                                            for i in S_TASKS 
                                            for j in S_UNITS 
                                            for nprime in S_TIME 
                                            if i in S_I_CONSUMING_K[k]
                                            if (i,j) in P_TASK_UNIT 
                                            if ((nprime >= n - P_Tau[i,j]-1) and (nprime <= n))
                                        )    
                                        + sum(
                                            P_rho_PLUS[i,k]*model.V_B[i,j,nprime] 
                                            for i in S_TASKS 
                                            for j in S_UNITS 
                                            for nprime in S_TIME 
                                            if i in S_I_PRODUCING_K[k] 
                                            if (i,j) in P_TASK_UNIT 
                                            if ((nprime >= n - P_Tau[i,j]-1) and (nprime <= n))
                                        )
                                        + sum(
                                            P_rho_MINUS[i,k]*model.V_B[i,j,nprime] 
                                            for i in S_TASKS 
                                            for j in S_UNITS 
                                            for nprime in S_TIME 
                                            if i in S_I_CONSUMING_K[k]
                                            if (i,j) in P_TASK_UNIT 
                                            if ((nprime >= n - P_Tau[i,j]-1) and (nprime <= n))
                                        )    
                                        + sum(
                                            P_rho_PLUS[i,k]*model.V_B[i,j,nprime] 
                                            for i in S_TASKS 
                                            for j in S_UNITS 
                                            for nprime in S_TIME 
                                            if i in S_I_PRODUCING_K[k] 
                                            if (i,j) in P_TASK_UNIT 
                                            if ((nprime >= n - P_Tau[i,j]) and (nprime <= n))
                                        )
                                        - (P_K_Demand[k,n] if (k,n) in STATES_SHIPMENT else 0)
                                        - model.V_D[k,n]
        )
    else:
        return Constraint.Skip  

def utility_balance_eq4():
    return

def track_idle_unit_eq13(model, j, n):
    if j in S_J_Units_With_Shutdown_Tasks and n >= 1:
        return model.V_X_Hat_Idle[j,n] == (model.V_X_Hat_Idle[j,n-1]
                                         + sum(
                                            model.V_X[i,j,nprime] 
                                            for i in S_I_Indirect_Transition_Tasks
                                            if P_TASK_UNIT[i,j] < 0
                                            for nprime in S_TIME
                                            if nprime >= n-P_Tau[i,j] and nprime <= n
                                         ) 
                                         - sum(
                                            model.V_X[i,j,nprime] 
                                            for i in S_I_Indirect_Transition_Tasks
                                            if P_TASK_UNIT[i,j] > 0
                                            for nprime in S_TIME
                                            if nprime >= n-P_Tau[i,j] and nprime <= n
                                         )
        )                                         
    else:
        return Constraint.Skip

def track_transitions_unit_eq15(model, i, j, n):
    if j in (S_J_Units_With_Direct_Transition_Tasks and S_J_Units_With_Shutdown_Tasks) and (i,j) in P_TASK_UNIT and i in S_I_Production_Tasks and n >= 1:
        return model.V_X_Hat[i,j,n] == (model.V_X_Hat[i,j,n-1]
                                         + model.V_X[i,j,n-1] - model.V_X[i,j,n]
                                         + sum(
                                            model.V_X[ii,j,n-P_Tau[ii,j]] 
                                            for ii in S_I_All_Transition_Tasks
                                            if P_TASK_TRANSITIONS_UNIT[j,i,ii] > 0
                                            if ii in S_I_Direct_Transition_Tasks
                                            if n >= P_Tau[ii,j]
                                         ) 
                                         - sum(
                                            model.V_X[ii,j,n] 
                                            for ii in S_I_All_Transition_Tasks
                                            if P_TASK_TRANSITIONS_UNIT[j,i,ii] < 0
                                            if ii in S_I_Direct_Transition_Tasks
                                         )
                                         + sum(
                                            model.V_X[ii,j,n-P_Tau[ii,j]] 
                                            for ii in S_I_All_Transition_Tasks
                                            if P_TASK_TRANSITIONS_UNIT[j,i,ii] > 0
                                            if ii in S_I_Indirect_Startup_Tasks
                                            if n >= P_Tau[ii,j]
                                         )
                                         - sum(
                                            model.V_X[ii,j,n] 
                                            for ii in S_I_All_Transition_Tasks
                                            if P_TASK_TRANSITIONS_UNIT[j,i,ii] < 0
                                            if ii in S_I_Indirect_Transition_Tasks    
                                            if ii not in S_I_Indirect_Startup_Tasks
                                         )
        )                                         
    else:
        return Constraint.Skip

# Tracks the start and end of all production tasks.    
def track_start_end_batch_task_eq16(model, i, j, n):
    if n >= 1 and (i,j) in P_TASK_UNIT and i in S_I_Production_Tasks:
        return model.V_Y_Start[i,j,n] == model.V_X[i,j,n] - model.V_X[i,j,n-1] + model.V_Y_End[i,j,n]
    else:
        return Constraint.Skip

def track_start_end_batch_task_eq17(model, i, j, n):
    if (i,j) in P_TASK_UNIT and i in S_I_Production_Tasks:
        return model.V_Y_Start[i,j,n] + model.V_Y_End[i,j,n] <= 1
    else:
        return Constraint.Skip

def min_lenght_run_eq18(model, i, j, n):
    if (i,j) in P_TASK_UNIT and i in S_I_Production_Tasks:
        return model.V_X[i,j,n] >= sum(model.V_Y_Start[i,j,nprime] for nprime in S_TIME if (nprime >= n - P_Tau_Min[i,j] + 1 and nprime <= n))    
    else:
        return Constraint.Skip

def max_lenght_run_eq19(model, i, j, n):
    if (i,j) in P_TASK_UNIT and i in S_I_Production_Tasks:
        return sum(model.V_X[i,j,nprime] for nprime in S_TIME if (nprime >= n - P_Tau_Max[i,j] and nprime <= n)) <= P_Tau_Max[i,j] 
    else:
        return Constraint.Skip

def track_start_production_task_after_transition_eq20(model, i, j, n):
    if (i,j) in P_TASK_UNIT and i in S_I_Production_Tasks and i not in S_I_Production_Tasks_Without_Transition:
        return (
            model.V_X[i,j,n] 
            >= 
            sum(
                model.V_X[iprime,j,nprime] 
                for iprime in (S_I_Direct_Transition_Tasks + S_I_Indirect_Transition_Tasks)
                if P_TASKS_TRANSITIONS[i,iprime] > 0
                for nprime in S_TIME
                if ((nprime >= n - P_Tau[i,j] + 1) and (nprime <= n))                
            )
        )
    else:
        return Constraint.Skip

def unit_availability_eq21(model, j, n):
    return (
        sum(
            model.V_X[i,j,nprime] 
            for (i,j) in P_TASK_UNIT 
            for nprime in S_TIME 
            if ((nprime >= n - P_Tau[i,j] + 1) and (nprime <= n))
      ) 
      + sum(
            model.V_X_Hat[i,j,n] 
            for i in (S_I_Production_Tasks - S_I_Production_Tasks_Without_Transition)
            if i in S_I_In_J[j]
      )
      + (model.V_X_Hat_Idle[j,n] if j in S_J_Units_With_Shutdown_Tasks else 0)

    ) <= 1

def material_capacity(model, k, n):
    return model.V_S[k,n] <= P_Chi[k]

def material_demand(model, k, n):
    return model.V_D[k,n] <= P_Chi[k]

def objective(model):
   return (
            sum((STATES[k]['price']*model.V_D[k,n]) for n in S_TIME for k in S_MATERIALS) 
           -sum((UNIT_TASKS[(j,i)]['Cost']*model.V_X[i,j,n] + UNIT_TASKS[(j,i)]['vCost']*model.V_B[i,j,n]) for (i,j) in P_TASK_UNIT for n in S_TIME) 
          )

 
model.C_Unit_Capacity_LB_Eq2 = Constraint(S_TASKS, S_UNITS, S_TIME, rule = unit_capacity_lb_eq2)
model.C_Unit_Capacity_UB_Eq2 = Constraint(S_TASKS, S_UNITS, S_TIME, rule = unit_capacity_ub_eq2)
model.C_Material_Mass_Balance_Eq3 = Constraint(S_MATERIALS, S_TIME, rule = material_mass_balance_eq3)
model.C_Track_Idle_Unit_Eq13 = Constraint(S_UNITS, S_TIME, rule = track_idle_unit_eq13)
model.C_Track_Transitions_units_Eq15 = Constraint(S_TASKS, S_UNITS, S_TIME, rule = track_transitions_unit_eq15)
model.C_Track_Start_End_Batch_Task_Eq16 = Constraint(S_TASKS, S_UNITS, S_TIME, rule = track_start_end_batch_task_eq16)
model.C_Track_Start_End_Batch_Task_Eq17 = Constraint(S_TASKS, S_UNITS, S_TIME, rule = track_start_end_batch_task_eq17)
model.C_Min_Lenght_Run_Eq18 = Constraint(S_TASKS, S_UNITS, S_TIME, rule = min_lenght_run_eq18)
model.C_Max_Lenght_Run_Eq19 = Constraint(S_TASKS, S_UNITS, S_TIME, rule = max_lenght_run_eq19)
model.C_Track_Start_Production_Task_After_Transition_Eq20 = Constraint(S_UNITS, S_UNITS, S_TIME, rule = track_start_production_task_after_transition_eq20)
model.C_Unit_Availability_Eq21 = Constraint(S_UNITS, S_TIME, rule = unit_availability_eq21)
model.C_Material_Availability = Constraint(S_MATERIALS, S_TIME, rule = material_capacity)
model.C_Material_Demand = Constraint(S_MATERIALS, S_TIME, rule = material_demand)
model.C_Objective = Objective(expr = objective, sense = maximize)

SolverFactory('appsi_highs').solve(model).write() 
#for con in model.component_map(Constraint).itervalues():
#    con.pprint()

# show all of V_X
model.V_X.display()
model.V_Y_Start.display()
model.V_Y_End.display()
model.V_B.display()
model.V_X_Hat.display()
model.V_X_Hat_Idle.display()
model.V_S.display()
model.V_D.display()

