from pyomo.environ import *


def unit_capacity_lb_eq2(model, i, j, n):
    """ 
    Lower bound on the processing rate of all tasks.        
    
    Input: set of tasks, units and time points.
    
    Output: constraints on the lower bound of processing rate of all tasks. 
    """
    
    if (i,j) in model.P_Task_Unit_Network:
        return model.V_X[i,j,n]*model.P_Beta_Min[i,j] <= model.V_B[i,j,n] 
    else:
        return Constraint.Skip    


def unit_capacity_ub_eq2(model, i, j, n):
    """ 
    Upper bound on the processing rate of all tasks.        
    
    Input: set of tasks, units and time points.
    
    Output: constraints on the upper bound of processing rate of all tasks. 
    """
    
    if (i,j) in model.P_Task_Unit_Network:
        return model.V_B[i,j,n] <= model.V_X[i,j,n]*model.P_Beta_Max[i,j]
    else:
        return Constraint.Skip


def material_mass_balance_eq3(model, k, n):
    """ 
    Mass balance of material k (except raw material which are considered to be always available). Consider the initial inventory, the inventory in the previou time point, what is consumed, what is produced by production tasks and what is produced by transition tasks.        
    
    Input: set of material and time points.
    
    Output: constraints on on the mass balance of material k. 
    """
    
    if k not in model.S_Raw_Materials:    
        return model.V_S[k,n] == ((model.V_S[k,n-1] 
                                    if n >= 1 else 0) 
                                  
                                + (model.P_Init_Inventory_Material[k] 
                                    if n == 0 else 0)
                                
                                + sum(model.P_Rho_Minus[i,k]*model.V_B[i,j,n] 
                                    for i in model.S_I_Consuming_K[k] 
                                    for j in model.S_J_Executing_I[i])    
                                                                                        
                                + sum(model.P_Rho_Plus[i,k]*model.V_B[i,j,n-model.P_Tau[i,j]]
                                    if n >= model.P_Tau[i,j] else 0 
                                    for i in model.S_I_Producing_K[k] 
                                    for j in model.S_J_Executing_I[i] 
                                    if i in model.S_I_Production_Tasks)
                                
                                + sum(model.P_Rho_Plus[i,k]*model.V_B[i,j,t] 
                                    for t in model.S_Time 
                                    for i in model.S_I_Producing_K[k] 
                                    for j in model.S_J_Executing_I[i] 
                                    if i in model.S_I_All_Transition_Tasks
                                    if (t >= n - model.P_Tau[i,j] and t <= n - 1))
                                
                                - model.P_Material_Demand[k,n])
    else:
        return Constraint.Skip


def material_capacity_eq4(model, k, n):
    """ 
    Storage limits for material k.
    
    Input: set of material and time points
    
    Output: constraints on storage capacity of materials.
    """
    
    return model.V_S[k,n] <= model.P_Chi[k]


def track_transitions_unit_eq12(model, i, j, n):
    if i in model.S_I_Production_Tasks and j in model.S_J_Executing_I[i]:
        return model.V_X_Hat[i,j,n] == ((model.V_X_Hat[i,j,n-1] if n >= 1 else 0) 
                                        
                                      + (model.V_X[i,j,n-1] if n >= 1 else 0)
                                        
                                      + sum(model.V_X[ii,j,n-model.P_Tau[ii,j]] 
                                            for ii in model.S_I_Startup_Tasks
                                            if (j,i,ii) in model.P_Task_Transitions_Unit 
                                            if model.P_Task_Transitions_Unit[j,i,ii] == 1
                                            if n - model.P_Tau[ii,j] >= 0)
                                
                                      - model.V_X[i,j,n]
                                
                                      - sum(model.V_X[ii,j,n] 
                                            for ii in model.S_I_Shutdown_Tasks
                                            if (j,i,ii) in model.P_Task_Transitions_Unit 
                                            if model.P_Task_Transitions_Unit[j,i,ii] == -1))                                         
    else:
        return Constraint.Skip


def track_idle_unit_eq13(model, j, n):
    """ 
    Model the relationship between startup, shutdown and idle model. Basically, if a shutdown happens, the unit goes to idle mode and it leaves it if there is a startup.
    It tracks the idle mode between consecutive time points (model.V_X_Hat_Idle[j,n] and model.V_X_Hat_Idle[j,n-1]); it tracks if a unit has a shutdown or a startup.
    
    Input: set units with startup and shutdown and set of time points.
    
    Output: constraints to model the relationship between startup, shutdown and idle model.
    """
    
    if j in model.S_J_Units_With_Shutdown_Tasks:
        return model.V_X_Hat_Idle[j,n] == ((model.V_X_Hat_Idle[j,n-1] if n >= 1 else 0)
                                         
                                         + (model.P_Unit_Initialization[j] if n == 0 else 0)  
                                         
                                         + sum(model.V_X[i,j,n-model.P_Tau[i,j]] 
                                            for i in model.S_I_Indirect_Transition_Tasks
                                            if (i,j) in model.P_Task_Unit_Network 
                                            if model.P_Task_Unit_Network[i,j] == -1
                                            if n-model.P_Tau[i,j] >= 0)
                                 
                                         - sum(model.V_X[i,j,n] 
                                            for i in model.S_I_Indirect_Transition_Tasks
                                            if (i,j) in model.P_Task_Unit_Network 
                                            if model.P_Task_Unit_Network[i,j] == 1))                                         
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


def track_start_end_run_task_eq16(model, i, j, n):
    """ 
    Models the relationship between the start and end of a run (part 1).
    
    Input: set of tasks, units and time points.
    
    Output: constraints that make sure that start and end variables are properly activated when there is a run.
    """
    
    if i in model.S_I_Production_Tasks and j in model.S_J_Executing_I[i]:
        return model.V_Y_Start[i,j,n] == model.V_X[i,j,n] - (model.V_X[i,j,n-1] if n >= 1 else 0) + model.V_Y_End[i,j,n]
    else:
        return Constraint.Skip


def track_start_end_run_task_eq17(model: ConcreteModel, i: Set, j: Set, n: Set) -> Constraint:
    """ 
    Models the relationship between the start and end of a run by stating that start and end cannot happen happen at the (part 2).
    
    Input: set of tasks, units and time points.
    
    Output: constraints that make sure that start and end variables are properly activated when there is a run.
    """
    
    if i in model.S_I_Production_Tasks and j in model.S_J_Executing_I[i]:
        return model.V_Y_Start[i,j,n] + model.V_Y_End[i,j,n] <= 1
    else:
        return Constraint.Skip


def track_start_end_run_unit_eq22(model: ConcreteModel, j: Set, n: Set) -> Constraint:
    """ 
    Makes sure that in a unit there is a 1 period of interval between the end and start of different tasks.
    
    Input: set of units and time points.
    
    Output: constraints to guarantee an interval between the run of different tasks in a unit.
    """
    
    return sum(model.V_Y_Start[i,j,n] for i in model.S_I_Production_Tasks) + sum(model.V_Y_End[i,j,n] for i in model.S_I_Production_Tasks) <= 1 


def min_lenght_run_eq18(model, i, j, n):
    """ 
    If a run starts, it needs to continue for at least P_Tau_Min periods.
    
    Input: set of tasks, units and time points.
    
    Output: constraints that model the minimum run length.
    """
    
    if (i,j) in model.P_Task_Unit_Network and i in model.S_I_Production_Tasks:
        return model.V_X[i,j,n] >= sum(model.V_Y_Start[i,j,nprime] 
                                       for nprime in model.S_Time 
                                       if (nprime >= n - model.P_Tau_Min[i,j] + 1 and nprime <= n))    
    else:
        return Constraint.Skip


def max_lenght_run_eq19(model, i, j, n):
    """ 
    If a run starts, it can run at most P_Tau_Max periods.
    
    Input: set of tasks, units and time points.
    
    Output: constraints that model the maximum run length.
    """
    
    if (i,j) in model.P_Task_Unit_Network and i in model.S_I_Production_Tasks:
        return sum(model.V_X[i,j,nprime] 
                   for nprime in model.S_Time 
                   if (nprime >= n - model.P_Tau_Max[i,j] and nprime <= n)) <= model.P_Tau_Max[i,j] 
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
    return sum(
            model.V_X[i,j,nprime] 
            for i in model.S_Tasks
            if (i,j) in model.P_Task_Unit_Network 
            for nprime in model.S_Time 
            if ((nprime >= n - model.P_Tau[i,j] + 1) and (nprime <= n))) <= 1
        


""" def unit_availability_eq21(model, j, n):
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
        
        + (model.V_X_Hat_Idle[j,n] if j in model.S_J_Units_With_Shutdown_Tasks else 0)) <= 1 """


def if_start_end(model, i, j, n):
    if (i in model.S_I_Production_Tasks) and j in model.S_J_Executing_I[i] and (n <= (len(model.S_Time) - 1) - model.P_Tau_Max[i,j]):
        return sum(model.V_Y_End[i,j,nprime] for nprime in model.S_Time if nprime >= n + model.P_Tau_Min[i,j] and nprime <= n + model.P_Tau_Max[i,j]) >= model.V_Y_Start[i,j,n]
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


def forward_propagation_inequality(model, i):
    if (i in model.S_I_Production_Tasks): 
        return sum(model.V_B[i,j,n] for n in model.S_Time for j in model.S_J_Executing_I[i] if (i,j) in model.P_Task_Unit_Network) <= model.mu_adjusted[i]        
    else:
        return Constraint.Skip


def est_constraint_x_to_zero(model, i, j):
    if (i in model.S_I_Production_Tasks) and (j in model.S_J_Executing_I[i]) and ((i,j) in model.P_Task_Unit_Network) and (model.P_EST[i,j] > 0):
        return sum(model.V_X[i,j,n] for n in model.S_Time if (n >= 0 and n <= (model.P_EST[i,j] - 1))) == 0
    else:
        return Constraint.Skip


def st_constraint_x_to_zero(model, i, j):
    if (i in model.S_I_Production_Tasks) and (j in model.S_J_Executing_I[i]) and ((i,j) in model.P_Task_Unit_Network) and (model.P_ST[i,j] > 0):
        return sum(model.V_X[i,j,n] for n in model.S_Time if (n >= max(model.S_Time) - model.P_EST[i,j] and n <= max(model.S_Time))) == 0
    else:
        return Constraint.Skip


def est_constraint_upper_bound_number_of_runs(model, i, j):
    if (i in model.S_I_Production_Tasks) and (j in model.S_J_Executing_I[i]) and ((i,j) in model.P_Task_Unit_Network):
        return sum(model.V_Y_Start[i,j,n] for n in model.S_Time) <= floor((max(model.S_Time) + 1 - model.P_EST[i,j])/(model.P_Tau_Min[i,j] + model.P_Tau_End_Task[i]))
    else:
        return Constraint.Skip    


def est_constraint_upper_bound_number_of_runs_unit(model, j):
    return sum(model.V_Y_Start[i,j,n] for i in model.S_I_Production_Tasks if (i,j) in model.P_Task_Unit_Network for n in model.S_Time) <= floor((max(model.S_Time) + 1 - model.P_EST_Unit[j])/(min(model.P_Tau_Min[i,j] for i in model.S_I_Production_Tasks if (i,j) in model.P_Task_Unit_Network) + model.P_Tau_End_Unit[j]))
     
     
def lower_bound_est_variables(model, i, j):
    if (i in model.S_I_Production_Tasks) and (j in model.S_J_Executing_I[i]) and ((i,j) in model.P_Task_Unit_Network) and ((i,j) in model.P_EST):
        return model.V_EST[i,j] >= model.P_EST[i,j]     
    else:
        return Constraint.Skip


def lower_bound_st_variables(model, i, j):
    if (i in model.S_I_Production_Tasks) and (j in model.S_J_Executing_I[i]) and ((i,j) in model.P_Task_Unit_Network) and ((i,j) in model.P_ST):
        return model.V_ST[i,j] >= model.P_ST[i,j]     
    else:
        return Constraint.Skip
    

def est_constraint_upper_bound_number_of_runs_dynamic_est(model, i, j):
    if (i in model.S_I_Production_Tasks) and (j in model.S_J_Executing_I[i]) and ((i,j) in model.P_Task_Unit_Network) and ((i,j) in model.P_EST):
        return sum(model.V_Y_Start[i,j,n] for n in model.S_Time) <= ((max(model.S_Time) + 1 - model.V_EST[i,j])/(model.P_Tau_Min[i,j] - model.P_Tau_End_Task[i]))
    else:
        return Constraint.Skip    


def subsequent_tasks_dynamic_est(model, i, ii, j, jj, k):
    if ((i in model.S_I_Production_Tasks) and (j in model.S_J_Executing_I[i]) and ((i,j) in model.P_Task_Unit_Network) 
    and (ii in model.S_I_Production_Tasks) and (jj in model.S_J_Executing_I[ii]) and ((ii,jj) in model.P_Task_Unit_Network) and (len(model.S_J_Executing_I[ii]) == 1)
    and (k in (model.S_K_Consumed_I[i] & model.S_K_Produced_I[ii])) and (len(model.S_I_Producing_K[k]) == 1)): 
        return model.V_EST[i,j] >= model.V_EST[ii,jj] + max(1, 
                                                              (  ceil( model.P_Tau_Max[ii,jj] * (model.P_Tau_Min[i,j]*model.P_Beta_Min[i,j]) / (model.P_Tau_Max[ii,jj] * model.P_Beta_Max[ii,jj]) ) 
                                                               + ceil( model.P_Tau_End_Task[ii] * (model.P_Tau_Min[i,j]*model.P_Beta_Min[i,j]) / (model.P_Tau_Max[ii,jj] * model.P_Beta_Max[ii,jj]) ) 
                                                               - model.P_Tau_End_Task[ii] + 1 - model.P_Tau_Min[i,j] ) )
    else:
        return Constraint.Skip
    
    
def create_constraints(model, STN, H):
   
    STATES = STN['STATES']
    STATES_SHIPMENT = STN['STATES_SHIPMENT']
    ST_ARCS = STN['ST_ARCS']
    TS_ARCS = STN['TS_ARCS']
    UNIT_TASKS = STN['UNIT_TASKS']
    #TIME = STN['TIME']
    TASKS_TRANSITION_TASKS = STN['TASKS_TRANSITION_TASKS']
    H = H

    #################################################Base Model#################################################

    model.C_Unit_Capacity_LB_Eq2 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = unit_capacity_lb_eq2)
    model.C_Unit_Capacity_UB_Eq2 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = unit_capacity_ub_eq2)
    model.C_Material_Mass_Balance_Eq3 = Constraint(model.S_Materials, model.S_Time, rule = material_mass_balance_eq3)
    model.C_Material_Capacity_Eq4 = Constraint(model.S_Materials, model.S_Time, rule = material_capacity_eq4)
    #model.C_Track_Indirect_Transitions_Eq12 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = track_transitions_unit_eq12)
    #model.C_Track_Idle_Unit_Eq13 = Constraint(model.S_Units, model.S_Time, rule = track_idle_unit_eq13)
    #model.C_Track_Transitions_Units_Eq15 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = track_transitions_unit_eq15)
    model.C_Track_Start_End_Run_Task_Eq16 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = track_start_end_run_task_eq16)
    model.C_Track_Start_End_Run_Task_Eq17 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = track_start_end_run_task_eq17)
    model.C_Track_Start_End_Runs_Unit_Eq_22 = Constraint(model.S_Units, model.S_Time, rule = track_start_end_run_unit_eq22)
    model.C_Min_Lenght_Run_Eq18 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = min_lenght_run_eq18)
    model.C_Max_Lenght_Run_Eq19 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = max_lenght_run_eq19)
    #model.C_Track_Start_Production_Task_After_Transition_Eq20 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = track_start_production_task_after_transition_eq20)
    model.C_Unit_Availability_Eq21 = Constraint(model.S_Units, model.S_Time, rule = unit_availability_eq21)
    
    #model.If_Start_End = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = if_start_end)
    #model.C_Max_Lenght_Run_Reformulation_YS_Eq19 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = max_lenght_run_eq19_reformulation_YS) 
    #model.C_Max_Lenght_Run_Reformulation_YE_Eq19 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = max_lenght_run_eq19_reformulation_YE) 

    
    
    ############################################Tightening Constraints############################################
    
    #Tightening Constraints EST - Static
    #model.C_EST_X_To_Zero = Constraint(model.S_Tasks, model.S_Units, rule = est_constraint_x_to_zero)
    #model.C_ST_X_To_Zero = Constraint(model.S_Tasks, model.S_Units, rule = st_constraint_x_to_zero)
    #model.C_EST_Upper_Bound_Number_Runs = Constraint(model.S_Tasks, model.S_Units, rule = est_constraint_upper_bound_number_of_runs)
    #model.C_EST_Upper_Bound_Number_Runs_Unit = Constraint(model.S_Units, rule = est_constraint_upper_bound_number_of_runs_unit)
    
    #Tightening Constraints EST - Dynamic
    #model.C_Lower_Bound_EST_Dynamic = Constraint(model.S_Tasks, model.S_Units, rule = lower_bound_est_variables)
    #model.C_Lower_Bound_ST_Dynamic = Constraint(model.S_Tasks, model.S_Units, rule = lower_bound_st_variables)
    #model.C_Upper_Bound_Number_Runs_EST_Dynamic = Constraint(model.S_Tasks, model.S_Units, rule = est_constraint_upper_bound_number_of_runs_dynamic_est)
    
    #Tightening Constraints EST - Dynamic - Subsequent Tasks
    #model.C_Subsequent_Tasks_Dynamic_EST = Constraint(model.S_Tasks, model.S_Tasks, model.S_Units, model.S_Units, model.S_Materials, rule = subsequent_tasks_dynamic_est)
    
    #############################################
    #  network_8_fast_upstream_slow_downstream  #
    #############################################
    
    #Tightening Constraints EST - Dynamic - Same Material - network_8_fast_upstream_slow_downstream
    #model.EST_Same_Material_1 = Constraint(expr = model.V_EST['TB1','UA3'] + model.V_EST['TB2','UA3'] >= 2*model.V_EST['TA1','UA1'] + 4)
    #model.EST_Same_Material_2 = Constraint(expr = model.V_EST['TB3','UA4'] + model.V_EST['TB4','UA4'] >= 2*model.V_EST['TA2','UA2'] + 4)
    #model.EST_Same_Material_3 = Constraint(expr = model.V_EST['TC3','UA6'] + model.V_EST['TC4','UA6'] >= 2*model.V_EST['TB4','UA4'] + 3)
    #model.EST_Same_Material_4 = Constraint(expr = model.V_EST['TC1','UA7'] + model.V_EST['TC2','UA7'] >= 2*model.V_EST['TB1','UA3'] + 3)
    
    #Tightening Constraints EST - Dynamic - Same Unit - network_8_fast_upstream_slow_downstream
    #model.EST_Same_Unit_1 = Constraint(expr = model.V_EST['TB1','UA3'] + model.V_EST['TB2','UA3'] >= 2*model.V_EST['TA1','UA1'] + 2 + 6)    
    #model.EST_Same_Unit_2 = Constraint(expr = model.V_EST['TB3','UA4'] + model.V_EST['TB4','UA4'] >= 2*model.V_EST['TA2','UA2'] + 2 + 6)    
    #model.EST_Same_Unit_3 = Constraint(expr = model.V_EST['TC1','UA7'] + model.V_EST['TC2','UA7'] >= 2*model.V_EST['TB1','UA3'] + 2 + 7)    
    #model.EST_Same_Unit_4 = Constraint(expr = model.V_EST['TC3','UA6'] + model.V_EST['TC4','UA6'] >= 2*model.V_EST['TB4','UA4'] + 2 + 7)    
    #model.EST_Same_Unit_5 = Constraint(expr = model.V_EST['TC5','UA5'] + model.V_EST['TC6','UA5'] >= model.V_EST['TB2','UA3'] + model.V_EST['TB3','UA4'] + 2 + 7)    
    
    #############################################
    #              network_10_dow               #
    #############################################   
    
    #Tightening Constraints EST - Dynamic - Same Unit - network_10_dow
    #model.EST_Same_Unit_1 = Constraint(expr = model.V_EST['TA1','UA1'] + model.V_EST['TA2','UA1'] + model.V_EST['TA3','UA1'] >= 21)    
    #model.EST_Same_Unit_2 = Constraint(expr = model.V_EST['TB1','UA2'] + model.V_EST['TB2','UA2'] + model.V_EST['TB3','UA2'] >= model.V_EST['TA1','UA1'] + model.V_EST['TA2','UA1'] + model.V_EST['TA3','UA1'] + 3)    
    #model.EST_Same_Unit_3 = Constraint(expr = model.V_EST['TC1','UA3'] + model.V_EST['TC2','UA3'] + model.V_EST['TC3','UA3'] >= model.V_EST['TB1','UA2'] + model.V_EST['TB2','UA2'] + model.V_EST['TB3','UA2'] + 3)
    #model.EST_Same_Unit_4 = Constraint(expr = model.V_EST['TD1','UA4'] + model.V_EST['TD2','UA4'] + model.V_EST['TD3','UA4'] >= model.V_EST['TC1','UA3'] + model.V_EST['TC2','UA3'] + model.V_EST['TC3','UA3'] + 3)
    #model.EST_Same_Unit_5 = Constraint(expr = model.V_EST['TE1','UA5'] + model.V_EST['TE2','UA5'] + model.V_EST['TE3','UA5'] >= model.V_EST['TD1','UA4'] + model.V_EST['TD2','UA4'] + model.V_EST['TD3','UA4'] + 3)
    #model.EST_Same_Unit_6 = Constraint(expr = model.V_EST['TF1','UA6'] + model.V_EST['TF2','UA6'] + model.V_EST['TF3','UA6'] >= model.V_EST['TE1','UA5'] + model.V_EST['TE2','UA5'] + model.V_EST['TE3','UA5'] + 3)
    
    #model.ST_Same_Unit_1 = Constraint(expr = model.V_ST['TA1','UA1'] + model.V_ST['TA2','UA1'] + model.V_ST['TA3','UA1'] >= 21+15)    
    #model.ST_Same_Unit_2 = Constraint(expr = model.V_ST['TB1','UA2'] + model.V_ST['TB2','UA2'] + model.V_ST['TB3','UA2'] >= 9+12)    
    #model.ST_Same_Unit_3 = Constraint(expr = model.V_ST['TC1','UA3'] + model.V_ST['TC2','UA3'] + model.V_ST['TC3','UA3'] >= 9+9)
    #model.ST_Same_Unit_4 = Constraint(expr = model.V_ST['TD1','UA4'] + model.V_ST['TD2','UA4'] + model.V_ST['TD3','UA4'] >= 9+6)
    #model.ST_Same_Unit_5 = Constraint(expr = model.V_ST['TE1','UA5'] + model.V_ST['TE2','UA5'] + model.V_ST['TE3','UA5'] >= 9+3)
    #model.ST_Same_Unit_6 = Constraint(expr = model.V_ST['TF1','UA6'] + model.V_ST['TF2','UA6'] + model.V_ST['TF3','UA6'] >= 9)
    
    
    