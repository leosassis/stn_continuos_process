from pyomo.environ import *
from numpy import floor
from src.utils.utils import print_dict
from src.models.optimization_config import define_solver

ADD_TIME_PERIOD = 1  # Used for computing the number of time periods
TAU_END_UNIT = 1  # Number of idle periods between two consecutive runs in a unit


def compute_upper_bound_x(model: ConcreteModel, stn: dict) -> None:
    """ 
    Computes upper bounds on x variables based on its operational window and tau values.
    
    Args:
        - model (ConcreteModel): Pyomo model instance.
        - stn (dict): a dictionary containing the network data.
    
    Returns: none.
    """
    
    est = stn['EST']
    number_ys = {}
    upper_bound_x = {}
    number_remaining_periods_for_x = {}
    
    S_Time = model.S_Time
    
    for j, i in est:
        
        tau_max = model.P_Tau_Max[i,j]
        tau_min = model.P_Tau_Min[i,j]
        tau_end = model.P_Tau_End_Task[i]
        max_time_points = max(S_Time) + 1 - est[j,i]
        
        number_ys[j,i] = floor((max_time_points)/(tau_max + tau_end))
        upper_bound_x[j,i] = number_ys[j,i]*tau_max
        number_remaining_periods_for_x[j,i] = max(0, max(S_Time) - est[j,i] - number_ys[j,i]*(tau_max + tau_end))    

        # Try to fit a shorter task in the remaining time
        for tau in range(int(tau_max) - 1, int(tau_min) - 1, - 1):
            if tau <= number_remaining_periods_for_x[j,i]:
                upper_bound_x[j,i] += tau
                break        
    
    stn['UPPER_BOUND_X'] = upper_bound_x
        

def knapsack_constraint(model_max_runs: ConcreteModel, number_time_points_for_x: int, tau_end: int) -> Constraint:
    """
    Defines the knapsack constraint weigthed by run_length + tau_end (number of time points necessary for each run_length) and limited by the number of possible production time points. 
    
    Args:
        - model_max_runs (ConcreteModel): Pyomo model instance.
        - number_time_points_for_x (int): number of available production time points.
        - tau_end (int): number of idle periods between two consecutives runs.
    
    Returns: A Pyomo constraint.
    """
    
    return sum((run_length + tau_end) * model_max_runs.V_Number_Runs[run_length] for run_length in model_max_runs.S_Run_Lenghts) <= number_time_points_for_x


def define_objective(model_max_runs: ConcreteModel) -> Objective:
    """
    Defines the objective function to maximize the number of production time points. 
    
    Args:
        - model_max_runs (ConcreteModel): Pyomo model instance.
    
    Returns: A Pyomo objective.
    """
    
    return sum((run_length) * model_max_runs.V_Number_Runs[run_length] for run_length in model_max_runs.S_Run_Lenghts)


def compute_upper_bound_x(model: ConcreteModel, stn: dict) -> None:
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
    
    upper_bound_x = {}
    
    for (j,i) in est:
        
        tau_max = model.P_Tau_Max[i,j]
        tau_min = model.P_Tau_Min[i,j]
        tau_end = model.P_Tau_End_Task[i]
        number_time_points_for_x = num_periods + ADD_TIME_PERIOD - est[j,i]
        
        model_max_runs = ConcreteModel()        
        
        model_max_runs.S_Run_Lenghts = RangeSet(tau_min, tau_max)
        model_max_runs.V_Number_Runs = Var(model_max_runs.S_Run_Lenghts, domain = NonNegativeIntegers)
        model_max_runs.C_Knapsack_Constraint = Constraint(rule = knapsack_constraint(model_max_runs, number_time_points_for_x, tau_end))
        model_max_runs.C_Objective = Objective(expr = define_objective(model_max_runs), sense = maximize)
        
        solver = define_solver()
        solver.solve(model_max_runs, tee = False)
        
        upper_bound_x[j,i] = sum(run_length * model_max_runs.V_Number_Runs[run_length].value for run_length in model_max_runs.S_Run_Lenghts)
             
    stn['UPPER_BOUND_X'] = upper_bound_x   
    
    
def knapsack_constraint_unit(model_max_runs_unit: ConcreteModel, number_time_points_for_x_unit: int, tau_end_unit: int) -> Constraint:
    """
    Defines the knapsack constraint weigthed by run_length_unit + tau_end_unit (number of time points necessary for each run_length_unit) and limited by the number of possible production time points. 
    
    Args:
        - model_max_runs_unit (ConcreteModel): Pyomo model instance.
        - number_time_points_for_x_unit (int): number of available production time points in a unit.
        - tau_end_unit (int): number of idle periods between two consecutives runs in a unit.
    
    Returns: A Pyomo constraint.
    """
    
    return sum((run_length_unit + tau_end_unit) * model_max_runs_unit.V_Number_Runs_Unit[run_length_unit] for run_length_unit in model_max_runs_unit.S_Run_Lenghts_Unit) <= number_time_points_for_x_unit


def define_objective_unit(model_max_runs_unit: ConcreteModel) -> Objective:
    """
    Defines the objective function to maximize the number of production time points. 
    
    Args:
        - model_max_runs_unit (ConcreteModel): Pyomo model instance.
    
    Returns: A Pyomo objective.
    """
    
    return sum((run_length_unit) * model_max_runs_unit.V_Number_Runs_Unit[run_length_unit] for run_length_unit in model_max_runs_unit.S_Run_Lenghts_Unit)    
    
        
def compute_upper_bound_x_unit(model: ConcreteModel, stn: dict) -> None:
    """ 
    The optimization problem defines the combination of different run lenghts that maximizes the number of production time points in a unit.
    Result is saved in stn['UPPER_BOUND_X_UNIT'].
        
    Args:
        - model (ConcreteModel): Pyomo model instance.
        - stn (dict): a dictionary containing the network data.
    
    Returns: none.
    """
        
    est = stn['EST']
    num_periods = max(model.S_Time)
    
    upper_bound_x_unit = {}
    
    for (j) in model.S_Units:
        
        tau_max_unit = max(model.P_Tau_Max[i,j] for i in model.S_I_In_J[j] if (j,i) in est)
        tau_min_unit = min(model.P_Tau_Min[i,j] for i in model.S_I_In_J[j] if (j,i) in est)
        tau_end_unit = TAU_END_UNIT
        number_time_points_for_x_unit = num_periods + ADD_TIME_PERIOD - min(est[j,i] for i in model.S_I_In_J[j])
        
        model_max_runs_unit = ConcreteModel()        
        
        model_max_runs_unit.S_Run_Lenghts_Unit = RangeSet(tau_min_unit, tau_max_unit)
        model_max_runs_unit.V_Number_Runs_Unit = Var(model_max_runs_unit.S_Run_Lenghts_Unit, domain = NonNegativeIntegers)
        model_max_runs_unit.C_Knapsack_Constraint_Unit = Constraint(rule = knapsack_constraint_unit(model_max_runs_unit, number_time_points_for_x_unit, tau_end_unit))
        model_max_runs_unit.C_Objective_Unit = Objective(expr = define_objective_unit(model_max_runs_unit), sense = maximize)
        
        solver = define_solver()
        solver.solve(model_max_runs_unit, tee = False)
        
        upper_bound_x_unit[j] = sum(run_length_unit * model_max_runs_unit.V_Number_Runs_Unit[run_length_unit].value for run_length_unit in model_max_runs_unit.S_Run_Lenghts_Unit)
               
    stn['UPPER_BOUND_X_UNIT'] = upper_bound_x_unit    
    print(stn['UPPER_BOUND_X_UNIT'])
    