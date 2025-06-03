from pyomo.environ import *


def unit_capacity_lb_eq2(model: ConcreteModel, task, unit, time_point) -> Constraint:
    """
    Enforces a lower bound on the processing rate for a task-unit pair at a given time point.

    Args:
        - model (ConcreteModel): Pyomo model instance.
        - task (str): task index.
        - unit (str): unit index.
        - time_point (int): time point index.

    Returns:
        A Pyomo constraint or Constraint.Skip if the task-unit pair is not in the network.
    """
    
    if (task, unit) in model.P_Task_Unit_Network:
        return model.V_X[task, unit, time_point]*model.P_Beta_Min[task, unit] <= model.V_B[task, unit, time_point] 
    
    return Constraint.Skip    


def unit_capacity_ub_eq2(model: ConcreteModel, task, unit, time_point) -> Constraint:
    """
    Enforces an upper bound on the processing rate for a task-unit pair at a given time point.

    Args:
        - model (ConcreteModel): Pyomo model instance.
        - task (str): task index.
        - unit (str): unit index.
        - time_point (int): time point index.

    Returns:
        A Pyomo constraint or Constraint.Skip if the task-unit pair is not in the network.
    """
    
    if (task, unit) in model.P_Task_Unit_Network:
        return model.V_B[task, unit, time_point] <= model.V_X[task, unit, time_point]*model.P_Beta_Max[task, unit]
    
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

    
def load_basic_model_constraints(model: ConcreteModel) -> None:
   
    model.C_Unit_Capacity_LB_Eq2 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = unit_capacity_lb_eq2)
    model.C_Unit_Capacity_UB_Eq2 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = unit_capacity_ub_eq2)
    model.C_Material_Mass_Balance_Eq3 = Constraint(model.S_Materials, model.S_Time, rule = material_mass_balance_eq3)
    model.C_Material_Capacity_Eq4 = Constraint(model.S_Materials, model.S_Time, rule = material_capacity_eq4)
    model.C_Track_Start_End_Run_Task_Eq16 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = track_start_end_run_task_eq16)
    model.C_Track_Start_End_Run_Task_Eq17 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = track_start_end_run_task_eq17)
    model.C_Track_Start_End_Runs_Unit_Eq_22 = Constraint(model.S_Units, model.S_Time, rule = track_start_end_run_unit_eq22)
    model.C_Min_Lenght_Run_Eq18 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = min_lenght_run_eq18)
    model.C_Max_Lenght_Run_Eq19 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = max_lenght_run_eq19)
    model.C_Unit_Availability_Eq21 = Constraint(model.S_Units, model.S_Time, rule = unit_availability_eq21)
    
    #model.C_Track_Indirect_Transitions_Eq12 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = track_transitions_unit_eq12)
    #model.C_Track_Idle_Unit_Eq13 = Constraint(model.S_Units, model.S_Time, rule = track_idle_unit_eq13)
    #model.C_Track_Transitions_Units_Eq15 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = track_transitions_unit_eq15)
    #model.C_Track_Start_Production_Task_After_Transition_Eq20 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = track_start_production_task_after_transition_eq20)


def load_constraints_bounds_X_Y_units(model: ConcreteModel) -> None:
   
    model.C_Track_Start_End_Run_Task_Eq16 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = track_start_end_run_task_eq16)
    model.C_Track_Start_End_Run_Task_Eq17 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = track_start_end_run_task_eq17)
    model.C_Track_Start_End_Runs_Unit_Eq_22 = Constraint(model.S_Units, model.S_Time, rule = track_start_end_run_unit_eq22)
    model.C_Min_Lenght_Run_Eq18 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = min_lenght_run_eq18)
    model.C_Max_Lenght_Run_Eq19 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = max_lenght_run_eq19)
    model.C_Unit_Availability_Eq21 = Constraint(model.S_Units, model.S_Time, rule = unit_availability_eq21)
       