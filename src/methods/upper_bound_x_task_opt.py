from pyomo.environ import *
from numpy import floor
from src.models.model_solve import define_solver
from src.models.base_model_build import load_model_sets_parameters_variables
from src.methods.est import compute_est_subsequent_tasks
from src.models.variables import RUNS_NEED_TO_FINISH_FLAG


ADD_TIME_POINT = 1  # Used for computing the number of time periods


def knapsack_constraint(model_max_production_time_points: ConcreteModel, number_time_points_for_x: int, tau_startup: int, tau_shutdown: int) -> Constraint:
    """
    Defines the knapsack constraint weigthed by run_length + tau_end (number of time points necessary for each run_length) and limited by the number of possible production time points. 
    
    Args:
        - model_max_production_time_points (ConcreteModel): Pyomo model instance.
        - number_time_points_for_x (int): number of available production time points.
        - tau_startup (int): number of time points for the startup operations.
        - tau_shutdown (int): number of time points for shutdown operations or idle periods between two consecutives runs.
    
    Returns: A Pyomo constraint.
    """
    
    return sum((run_length + tau_startup + tau_shutdown) * model_max_production_time_points.V_Number_Runs[run_length] for run_length in model_max_production_time_points.S_Run_Lenghts) <= number_time_points_for_x


def define_objective(model_max_production_time_points: ConcreteModel) -> Objective:
    """
    Defines the objective function to maximize the number of production time points. 
    
    Args:
        - model_max_production_time_points (ConcreteModel): Pyomo model instance.
    
    Returns: A Pyomo objective.
    """
    
    return sum((run_length) * model_max_production_time_points.V_Number_Runs[run_length] for run_length in model_max_production_time_points.S_Run_Lenghts)


def compute_upper_bound_x_task(stn_data: dict, planning_horizon: int) -> None:
    """ 
    The optimization problem defines the combination of different run lenghts that maximizes the number of production time points for each task.
    Result is saved in stn['UPPER_BOUND_X'].
    
    Args:
        - model_init_max_production_task (ConcreteModel): Pyomo model instance.
        - stn_data (dict): a dictionary containing the network data.
    
    Returns: none.
    """
    
    model_init_max_production_task = ConcreteModel()
    
    load_model_sets_parameters_variables(model_init_max_production_task, stn_data, planning_horizon)
    compute_est_subsequent_tasks(model_init_max_production_task, stn_data)
        
    est = stn_data['EST']
    num_periods = max(model_init_max_production_task.S_Time)    
    upper_bound_x_task = {}
    number_runs = {}
    time_points_complete_runs = {}
    remaining_time_points_x = {}
    remaining_time_points = {}
    
    for (i,j) in model_init_max_production_task.P_Task_Unit_Network:
        
        # Skip tasks that are not production tasks
        if i not in model_init_max_production_task.S_I_Production_Tasks:
            continue
        
        # Import tau_max, tau_min, tau_shutdown and number of time points
        tau_max = model_init_max_production_task.P_Tau_Max[i,j]
        tau_min = model_init_max_production_task.P_Tau_Min[i,j]
        tau_shutdown = model_init_max_production_task.P_Tau_End_Task[i]
        tau_startup = 0
        number_time_points_for_x = num_periods + ADD_TIME_POINT - est[j,i]
        
        # Import tau for the production tasks with transitions
        for ii in model_init_max_production_task.S_I_Startup_Tasks:
            if (
                i in model_init_max_production_task.S_I_Production_Tasks_With_Transition and 
                (j,i,ii) in model_init_max_production_task.P_Task_Transitions_Unit
            ):
                tau_startup = model_init_max_production_task.P_Tau[ii,j]
            
        for ii in model_init_max_production_task.S_I_Shutdown_Tasks:
            if (
                i in model_init_max_production_task.S_I_Production_Tasks_With_Transition and
                (j,i,ii) in model_init_max_production_task.P_Task_Transitions_Unit
            ):
                tau_shutdown = model_init_max_production_task.P_Tau[ii,j]
        
        print(f"Production task = {i}, tau_startup = {tau_startup}, tau_shutdown = {tau_shutdown}")
        
        #############################################################################################################
        # UB ON X FOR TASKS WITHOUT TRANSITION                                                                      #
        #############################################################################################################
        
        if (
            RUNS_NEED_TO_FINISH_FLAG == True
        ):
        
            model_max_production_time_points = ConcreteModel()        
            
            model_max_production_time_points.S_Run_Lenghts = RangeSet(tau_min, tau_max)
            model_max_production_time_points.V_Number_Runs = Var(model_max_production_time_points.S_Run_Lenghts, domain = NonNegativeIntegers)
            model_max_production_time_points.C_Knapsack_Constraint = Constraint(rule = knapsack_constraint(model_max_production_time_points, number_time_points_for_x, tau_startup, tau_shutdown))
            model_max_production_time_points.C_Objective = Objective(expr = define_objective(model_max_production_time_points), sense = maximize)
            
            solver = define_solver()
            solver.solve(model_max_production_time_points, tee = False)
            
            upper_bound_x_task[j,i] = sum(run_length * model_max_production_time_points.V_Number_Runs[run_length].value for run_length in model_max_production_time_points.S_Run_Lenghts)
            number_runs[j,i] = sum(model_max_production_time_points.V_Number_Runs[run_length].value for run_length in model_max_production_time_points.S_Run_Lenghts)
            remaining_time_points[j,i] = number_time_points_for_x - upper_bound_x_task[j,i] - (tau_startup + tau_shutdown) * number_runs[j,i]
            
            print(f'Unit: {j}, Task: {i}, Available Time Points = {number_time_points_for_x}, Time Points for X = {upper_bound_x_task[j,i]}, Number of Complete Runs = {number_runs[j,i]}, Remaining Time Points = {remaining_time_points[j,i]}')
            model_max_production_time_points.V_Number_Runs.display() 
            
        elif (
            RUNS_NEED_TO_FINISH_FLAG == False
        ):
            number_runs[j,i] = floor(number_time_points_for_x / (tau_max + tau_startup + tau_shutdown))
            time_points_complete_runs[j,i] = (tau_max + tau_startup + tau_shutdown) * number_runs[j,i]
            remaining_time_points_x[j,i] = number_time_points_for_x - time_points_complete_runs[j,i]
            upper_bound_x_task[j,i] = tau_max * number_runs[j,i] + max(remaining_time_points_x[j,i] - tau_startup, 0) 
            remaining_time_points[j,i] = number_time_points_for_x - time_points_complete_runs[j,i] - remaining_time_points_x[j,i]
            print(f'Unit: {j}, Task: {i}, Available Time Points = {number_time_points_for_x}, Time Points for X = {upper_bound_x_task[j,i]}, Number of Complete Runs = {number_runs[j,i]}, Remaining Time Points = {remaining_time_points[j,i]}')
                
    stn_data['UPPER_BOUND_X_TASK'] = upper_bound_x_task