from pyomo.environ import *
from numpy import floor
from src.models.optimization_config import define_solver

ADD_TIME_PERIOD = 1  # Used for computing the number of time periods
TAU_END_UNIT = 1  # Number of idle periods between two consecutive runs in a unit


def knapsack_constraint_unit(model_max_runs_unit: ConcreteModel, number_time_points_unit: int, tau_end_unit: int) -> Constraint:
    """
    Defines the knapsack constraint weigthed by run_length_unit + tau_end_unit (number of time points necessary for each run_length_unit) and limited by the number of possible production time points. 
    
    Args:
        - model_max_runs_unit (ConcreteModel): Pyomo model instance.
        - number_time_points_unit (int): number of available production time points.
        - tau_end_unit (int): number of idle periods between two consecutives runs.
    
    Returns: A Pyomo constraint.
    """
    
    return sum((run_length_unit + tau_end_unit) * model_max_runs_unit.V_Number_Runs_Unit[run_length_unit] for run_length_unit in model_max_runs_unit.S_Run_Lenghts_Unit) <= number_time_points_unit


def define_objective_unit(model_max_runs_unit: ConcreteModel) -> Objective:
    """
    Defines the objective function to maximize the number of production time points. 
    
    Args:
        - model_max_runs_unit (ConcreteModel): Pyomo model instance.
    
    Returns: A Pyomo objective.
    """
    
    return sum(model_max_runs_unit.V_Number_Runs_Unit[run_length_unit] for run_length_unit in model_max_runs_unit.S_Run_Lenghts_Unit)


def compute_upper_bound_ys_unit(model: ConcreteModel, state_task_network: dict) -> None:
    """ 
    The optimization problem defines the combination of different run lenghts that maximizes the number of production time points for each task.
    Result is saved in stn['UPPER_BOUND_X'].
    
    Args:
        - model (ConcreteModel): Pyomo model instance.
        - state_task_network (dict): a dictionary containing the network data.
    
    Returns: none.
    """
        
    est = state_task_network['EST']
    num_periods = max(model.S_Time)
    
    print(est)
    
    upper_bound_y_unit = {}
    
    for (j) in model.S_Units:
        
        tau_max_unit = max(model.P_Tau_Max[i,j] for i in model.S_I_In_J[j] if (j,i) in est)
        tau_min_unit = min(model.P_Tau_Min[i,j] for i in model.S_I_In_J[j] if (j,i) in est)
        tau_end_unit = TAU_END_UNIT
        number_time_points_unit = num_periods + ADD_TIME_PERIOD - min(est[j,i] for i in model.S_I_In_J[j])
        
        model_max_runs_unit = ConcreteModel()        
        
        model_max_runs_unit.S_Run_Lenghts_Unit = RangeSet(tau_min_unit, tau_max_unit)
        model_max_runs_unit.V_Number_Runs_Unit = Var(model_max_runs_unit.S_Run_Lenghts_Unit, domain = NonNegativeIntegers)
        model_max_runs_unit.C_Knapsack_Constraint_Unit = Constraint(rule = knapsack_constraint_unit(model_max_runs_unit, number_time_points_unit, tau_end_unit))
        model_max_runs_unit.C_Objective_Unit = Objective(expr = define_objective_unit(model_max_runs_unit), sense = maximize)
        
        solver = define_solver()
        solver.solve(model_max_runs_unit, tee = False)
        
        upper_bound_y_unit[j] = sum(model_max_runs_unit.V_Number_Runs_Unit[run_length_unit].value for run_length_unit in model_max_runs_unit.S_Run_Lenghts_Unit)
        
    state_task_network['UPPER_BOUND_Y_UNIT'] = upper_bound_y_unit  