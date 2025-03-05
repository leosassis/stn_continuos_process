from pyomo.environ import *

# Lower bound on the batch size of all tasks.
def unit_capacity_lb_eq2(model, i, j, n):
    if (i,j) in model.P_Task_Unit_Network:
        return model.V_X[i,j,n]*model.P_Beta_Min[i,j] <= model.V_B[i,j,n] 
    else:
        return Constraint.Skip    

# Upper bound on the batch size of all tasks.
def unit_capacity_ub_eq2(model, i, j, n):
    if (i,j) in model.P_Task_Unit_Network:
        return model.V_B[i,j,n] <= model.V_X[i,j,n]*model.P_Beta_Max[i,j]
    else:
        return Constraint.Skip

def material_mass_balance_eq3(model, k, n):
    if k not in model.S_Raw_Materials:    
        return model.V_S[k,n] == ((model.V_S[k,n-1] if n >= 1 else 0) 
                                  
                                + (model.P_Init_Inventory_Material[k] if n == 0 else 0)
                                
                                + sum(
                                    model.P_Rho_Minus[i,k]*model.V_B[i,j,n] 
                                    for i in model.S_I_Consuming_K[k] 
                                    for j in model.S_J_Executing_I[i])    
                                                                                        
                                + sum(
                                    model.P_Rho_Plus[i,k]*model.V_B[i,j,n-1]
                                    if n >= 1 else 0 
                                    for i in model.S_I_Producing_K[k] 
                                    for j in model.S_J_Executing_I[i] 
                                    if i in model.S_I_Production_Tasks)
                                
                                + sum(
                                    model.P_Rho_Plus[i,k]*model.V_B[i,j,t] 
                                    for t in model.S_Time 
                                    for i in model.S_I_Producing_K[k] 
                                    for j in model.S_J_Executing_I[i] 
                                    if i in model.S_I_All_Transition_Tasks
                                    if t >= n - model.P_Tau[i,j] and t <= n - 1)
                                
                                - model.P_Material_Demand[k,n])
    else:
        return Constraint.Skip

def track_idle_unit_eq13(model, j, n):
    if j in model.S_J_Units_With_Shutdown_Tasks:
        return model.V_X_Hat_Idle[j,n] == ((model.V_X_Hat_Idle[j,n-1] if n >= 1 else 0)
                                         
                                + (model.P_Unit_Initialization[j] if n == 0 else 0)  
                                         
                                + sum(
                                    model.V_X[i,j,n-model.P_Tau[i,j]] 
                                    for i in model.S_I_Indirect_Transition_Tasks
                                    if (i,j) in model.P_Task_Unit_Network 
                                    if model.P_Task_Unit_Network[i,j] == -1
                                    if n-model.P_Tau[i,j] >= 0)
                                 
                                - sum(
                                    model.V_X[i,j,n] 
                                    for i in model.S_I_Indirect_Transition_Tasks
                                    if (i,j) in model.P_Task_Unit_Network 
                                    if model.P_Task_Unit_Network[i,j] == 1))                                         
    else:
        return Constraint.Skip

def track_transitions_unit_eq12(model, i, j, n):
    if i in model.S_I_Production_Tasks and j in model.S_J_Executing_I[i]:
        return model.V_X_Hat[i,j,n] == ((model.V_X_Hat[i,j,n-1] if n >= 1 else 0) 
                                        
                                + (model.V_X[i,j,n-1] if n >= 1 else 0)
                                        
                                + sum(
                                    model.V_X[ii,j,n-model.P_Tau[ii,j]] 
                                    for ii in model.S_I_Startup_Tasks
                                    if (j,i,ii) in model.P_Task_Transitions_Unit 
                                    if model.P_Task_Transitions_Unit[j,i,ii] == 1
                                    if n - model.P_Tau[ii,j] >= 0)
                                
                                - model.V_X[i,j,n]
                                
                                - sum(
                                    model.V_X[ii,j,n] 
                                    for ii in model.S_I_Shutdown_Tasks
                                    if (j,i,ii) in model.P_Task_Transitions_Unit 
                                    if model.P_Task_Transitions_Unit[j,i,ii] == -1))                                         
    else:
        return Constraint.Skip


def track_transitions_unit_eq15(model, i, j, n):
    if j in (model.S_J_Units_With_Direct_Transition_Tasks or model.S_J_Units_With_Shutdown_Tasks) and (i,j) in model.P_Task_Unit_Network and i in model.S_I_Production_Tasks:
        return model.V_X_Hat[i,j,n] == ((model.V_X_Hat[i,j,n-1] if n >= 1 else 0)
                                         + (model.V_X[i,j,n-1] if n >= 1 else 0)
                                         - model.V_X[i,j,n]
                                         + sum(
                                            model.V_X[ii,j,n-model.P_Tau[ii,j]] 
                                            for ii in model.S_I_Direct_Transition_Tasks
                                            if (j,i,ii) in model.P_Task_Transitions_Unit 
                                            if model.P_Task_Transitions_Unit[j,i,ii] == 1
                                            if n >= model.P_Tau[ii,j])
                                          
                                         - sum(
                                            model.V_X[ii,j,n] 
                                            for ii in model.S_I_Direct_Transition_Tasks
                                            if (j,i,ii) in model.P_Task_Transitions_Unit 
                                            if model.P_Task_Transitions_Unit[j,i,ii] == -1)
                                         
                                         + sum(
                                            model.V_X[ii,j,n-model.P_Tau[ii,j]] 
                                            for ii in model.S_I_Startup_Tasks
                                            if (j,i,ii) in model.P_Task_Transitions_Unit 
                                            if model.P_Task_Transitions_Unit[j,i,ii] == 1
                                            if n >= model.P_Tau[ii,j])
                                         
                                         - sum(
                                            model.V_X[ii,j,n] 
                                            for ii in model.S_I_Shutdown_Tasks
                                            if (j,i,ii) in model.P_Task_Transitions_Unit 
                                            if model.P_Task_Transitions_Unit[j,i,ii] == -1))                                         
    else:
        return Constraint.Skip

# Tracks the start and end of all production tasks.    
def track_start_end_production_task_eq16(model, i, j, n):
    if i in model.S_I_Production_Tasks and j in model.S_J_Executing_I[i]:
        return model.V_Y_Start[i,j,n] == model.V_X[i,j,n] - (model.V_X[i,j,n-1] if n >= 1 else 0) + model.V_Y_End[i,j,n]
    else:
        return Constraint.Skip

def track_start_end_batch_task_eq17(model, i, j, n):
    if i in model.S_I_Production_Tasks and j in model.S_J_Executing_I[i]:
        return model.V_Y_Start[i,j,n] + model.V_Y_End[i,j,n] <= 1
    else:
        return Constraint.Skip

def min_lenght_run_eq18(model, i, j, n):
    if (i,j) in model.P_Task_Unit_Network and i in model.S_I_Production_Tasks:
        return model.V_X[i,j,n] >= sum(model.V_Y_Start[i,j,nprime] for nprime in model.S_Time if (nprime >= n - model.P_Tau_Min[i,j] + 1 and nprime <= n))    
    else:
        return Constraint.Skip

def max_lenght_run_eq19(model, i, j, n):
    if (i,j) in model.P_Task_Unit_Network and i in model.S_I_Production_Tasks:
        return sum(model.V_X[i,j,nprime] for nprime in model.S_Time if (nprime >= n - model.P_Tau_Max[i,j] and nprime <= n)) <= model.P_Tau_Max[i,j] 
    else:
        return Constraint.Skip

def max_lenght_run_eq19_reformulation_YS(model, i, j, n):
    if (i,j) in model.P_Task_Unit_Network and i in model.S_I_Production_Tasks:
        return model.V_X[i,j,n] <= sum(model.V_Y_Start[i,j,nprime] for nprime in model.S_Time if ( (nprime >= n - model.P_Tau_Max[i,j] + 1) and (nprime <= n) )) 
    else:
        return Constraint.Skip


def max_lenght_run_eq19_reformulation_YE(model, i, j, n):
    if (i,j) in model.P_Task_Unit_Network and i in model.S_I_Production_Tasks:
        return model.V_X[i,j,n] <= sum(model.V_Y_End[i,j,nprime] for nprime in model.S_Time if ( (nprime >= n + 1) and (nprime <= n + model.P_Tau_Max[i,j]) )) 
    else:
        return Constraint.Skip

    
def track_start_production_task_after_transition_eq20(model, i, j, n):
    if i in model.S_I_Production_Tasks_With_Transition and j in model.S_J_Executing_I[i]:
        return (model.V_X[i,j,n] >= 
                                    sum(
                                        model.V_X[ii,j,nprime-model.P_Tau[ii,j]] 
                                        for ii in model.S_I_All_Transition_Tasks
                                        if (i,ii) in model.P_Task_Transitions 
                                        if model.P_Task_Transitions[i,ii] == 1
                                        for nprime in model.S_Time
                                        if ((nprime >= n - model.P_Tau_Min[i,j] + 1) and (nprime <= n))  
                                        if nprime-model.P_Tau[ii,j] >= 0))
    else:
        return Constraint.Skip

def unit_availability_eq21(model, j, n):
    return (
        sum(
            model.V_X[i,j,nprime] 
            for i in model.S_Tasks
            if (i,j) in model.P_Task_Unit_Network 
            for nprime in model.S_Time 
            if ((nprime >= n - model.P_Tau[i,j] + 1) and (nprime <= n))) 
        
        + sum(
            model.V_X_Hat[i,j,n] 
            for i in (model.S_I_Production_Tasks_With_Transition)
            if i in model.S_I_In_J[j])
        
        + (model.V_X_Hat_Idle[j,n] if j in model.S_J_Units_With_Shutdown_Tasks else 0)) <= 1

def material_capacity(model, k, n):
    return model.V_S[k,n] <= model.P_Chi[k]

def if_start_end(model, i, j, n):
    if (i in model.S_I_Production_Tasks) and j in model.S_J_Executing_I[i] and (n <= (len(model.S_Time) - 1) - model.P_Tau_Max[i,j]):
        return sum(model.V_Y_End[i,j,nprime] for nprime in model.S_Time if nprime >= n + model.P_Tau_Min[i,j] and nprime <= n + model.P_Tau_Max[i,j]) >= model.V_Y_Start[i,j,n]
    else:
        return Constraint.Skip

def forward_propagation_inequality(model, i):
    if (i in model.S_I_Production_Tasks): 
        return sum(model.V_B[i,j,n] for n in model.S_Time for j in model.S_J_Executing_I[i] if (i,j) in model.P_Task_Unit_Network) <= model.mu_adjusted[i]        
    else:
        return Constraint.Skip

def est_constraint_1(model, i, j):
    if (i in model.S_I_Production_Tasks) and (j in model.S_J_Executing_I[i]) and ((i,j) in model.P_Task_Unit_Network):
        return sum(model.V_X[i,j,n] for n in model.S_Time) <= max(model.S_Time) - model.P_EST[i,j]
    else:
        return Constraint.Skip
    
def est_constraint_2(model, j):
    return sum(model.V_X[i,j,n] for i in model.S_I_Production_Tasks if (i,j) in model.P_Task_Unit_Network for n in model.S_Time) <= max(model.S_Time) - model.P_EST_Unit[j]
    
    
def create_constraints(model, STN, H):
   
    STATES = STN['STATES']
    STATES_SHIPMENT = STN['STATES_SHIPMENT']
    ST_ARCS = STN['ST_ARCS']
    TS_ARCS = STN['TS_ARCS']
    UNIT_TASKS = STN['UNIT_TASKS']
    #TIME = STN['TIME']
    TASKS_TRANSITION_TASKS = STN['TASKS_TRANSITION_TASKS']
    H = H

    model.C_Unit_Capacity_LB_Eq2 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = unit_capacity_lb_eq2)
    model.C_Unit_Capacity_UB_Eq2 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = unit_capacity_ub_eq2)
    model.C_Track_Idle_Unit_Eq13 = Constraint(model.S_Units, model.S_Time, rule = track_idle_unit_eq13)
    model.C_Track_Transitions_units_Eq15 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = track_transitions_unit_eq15)
    model.C_Track_Start_End_Batch_Task_Eq16 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = track_start_end_production_task_eq16)
    model.C_Track_Start_End_Batch_Task_Eq17 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = track_start_end_batch_task_eq17)
    model.C_Min_Lenght_Run_Eq18 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = min_lenght_run_eq18)
    model.C_Max_Lenght_Run_Eq19 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = max_lenght_run_eq19)
    model.C_Track_Start_Production_Task_After_Transition_Eq20 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = track_start_production_task_after_transition_eq20)
    model.C_Unit_Availability_Eq21 = Constraint(model.S_Units, model.S_Time, rule = unit_availability_eq21)
    model.C_Material_Availability = Constraint(model.S_Materials, model.S_Time, rule = material_capacity)
    model.C_Material_Mass_Balance_Eq3 = Constraint(model.S_Materials, model.S_Time, rule = material_mass_balance_eq3)
    model.If_Start_End = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = if_start_end)
    #model.C_Max_Lenght_Run_Eq19_Reformulation_YS = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = max_lenght_run_eq19_reformulation_YS)
    #model.C_Max_Lenght_Run_Eq19_Reformulation_YE = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = max_lenght_run_eq19_reformulation_YE)
    #model.C_Forward_Propagation_Inequality = Constraint(model.S_Tasks, rule = forward_propagation_inequality)
    #model.C_EST_1 = Constraint(model.S_Tasks, model.S_Units, rule = est_constraint_1)
    #model.C_EST_2 = Constraint(model.S_Units, rule = est_constraint_2)
    