from pyomo.environ import *
from numpy import floor
from src.utils.utils import print_dict
from src.models.optimization_config import define_solver


ADD_TIME_PERIOD = 1  # Used for computing the number of time periods


def compute_upper_bound_x_old(model: ConcreteModel, stn: dict) -> None:
    """ 
    Computes upper bounds on x variables based on its operational window and tau values.
    
    Args:
        - model (ConcreteModel): Pyomo model instance.
        - stn (dict): a dictionary containing the network data.
    
    Returns: none.
    """
    
    est = stn['EST']
    number_ys = {}
    upper_bound_x_task = {}
    number_remaining_periods_for_x = {}
    
    S_Time = model.S_Time
    
    for j, i in est:
        
        tau_max = model.P_Tau_Max[i,j]
        tau_min = model.P_Tau_Min[i,j]
        tau_end = model.P_Tau_End_Task[i]
        max_time_points = max(S_Time) + 1 - est[j,i]
        
        number_ys[j,i] = floor((max_time_points)/(tau_max + tau_end))
        upper_bound_x_task[j,i] = number_ys[j,i]*tau_max
        number_remaining_periods_for_x[j,i] = max(0, max(S_Time) - est[j,i] - number_ys[j,i]*(tau_max + tau_end))    

        # Try to fit a shorter task in the remaining time
        for tau in range(int(tau_max) - 1, int(tau_min) - 1, - 1):
            if tau <= number_remaining_periods_for_x[j,i]:
                upper_bound_x_task[j,i] += tau
                break        
    
    stn['UPPER_BOUND_X'] = upper_bound_x_task
        

def knapsack_constraint(model_max_production_time_points: ConcreteModel, number_time_points_for_x: int, tau_end: int) -> Constraint:
    """
    Defines the knapsack constraint weigthed by run_length + tau_end (number of time points necessary for each run_length) and limited by the number of possible production time points. 
    
    Args:
        - model_max_production_time_points (ConcreteModel): Pyomo model instance.
        - number_time_points_for_x (int): number of available production time points.
        - tau_end (int): number of idle periods between two consecutives runs.
    
    Returns: A Pyomo constraint.
    """
    
    return sum((run_length + tau_end) * model_max_production_time_points.V_Number_Runs[run_length] for run_length in model_max_production_time_points.S_Run_Lenghts) <= number_time_points_for_x


def define_objective(model_max_production_time_points: ConcreteModel) -> Objective:
    """
    Defines the objective function to maximize the number of production time points. 
    
    Args:
        - model_max_production_time_points (ConcreteModel): Pyomo model instance.
    
    Returns: A Pyomo objective.
    """
    
    return sum((run_length) * model_max_production_time_points.V_Number_Runs[run_length] for run_length in model_max_production_time_points.S_Run_Lenghts)


def compute_upper_bound_x_task(model: ConcreteModel, stn: dict) -> None:
    """ 
    The optimization problem defines the combination of different run lenghts that maximizes the number of production time points for each task.
    Result is saved in stn['UPPER_BOUND_X'].
    
    Args:
        - model (ConcreteModel): Pyomo model instance.
        - stn (dict): a dictionary containing the network data.
    
    Returns: none.
    """
        
    est = stn['EST']
    num_periods = max(model.S_Time)
    
    upper_bound_x_task = {}
    
    for (j,i) in est:
        
        tau_max = model.P_Tau_Max[i,j]
        tau_min = model.P_Tau_Min[i,j]
        tau_end = model.P_Tau_End_Task[i]
        number_time_points_for_x = num_periods + ADD_TIME_PERIOD - est[j,i]
        print(f'Unit: {j}, task: {i}, est[{i},{j}] = {est[j,i]}, number of time points = {number_time_points_for_x}')
        model_max_production_time_points = ConcreteModel()        
        
        model_max_production_time_points.S_Run_Lenghts = RangeSet(tau_min, tau_max)
        model_max_production_time_points.V_Number_Runs = Var(model_max_production_time_points.S_Run_Lenghts, domain = NonNegativeIntegers)
        model_max_production_time_points.C_Knapsack_Constraint = Constraint(rule = knapsack_constraint(model_max_production_time_points, number_time_points_for_x, tau_end))
        model_max_production_time_points.C_Objective = Objective(expr = define_objective(model_max_production_time_points), sense = maximize)
        
        solver = define_solver()
        solver.solve(model_max_production_time_points, tee = False)
        
        upper_bound_x_task[j,i] = sum(run_length * model_max_production_time_points.V_Number_Runs[run_length].value for run_length in model_max_production_time_points.S_Run_Lenghts)
        model_max_production_time_points.V_Number_Runs.display() 
                
    stn['UPPER_BOUND_X_TASK'] = upper_bound_x_task   
    print(f'Upper bound on X for each task considering its EST: {stn['UPPER_BOUND_X_TASK']}')