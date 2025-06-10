from pyomo.environ import *
from src.models.model_build import load_model_sets_parameters_variables, load_basic_model_constraints_objective
from src.models.parameters import create_ppc_parameters, create_est_parameters, create_opt_parameters
from src.models.constraints_est import load_constraints_set_to_zero_x_ys_est, load_constraints_preprocessing, load_constraints_preprocessing_optimization 
from src.methods.est import compute_est_subsequent_tasks
from src.methods.est_group import compute_est_group_tasks
from src.methods.upper_bound_x_task_opt import compute_upper_bound_x_task
from src.models.model_solve import solve_model, define_solver
from src.methods.upper_bound_ys_x_unit_opt import compute_upper_bound_x_unit, compute_upper_bound_y_unit
from src.visualization.plot_results import plot_gantt_chart


def create_model_f0_base_formulation(stn_data: dict, planning_horizon: int) -> tuple[ConcreteModel, str]:
    """
    Creates the base MILP model.
    
    Args:
        - stn_data (dict): a dictionary with the state-task network instance data.
        - planning_horizon (int): planning horizon.

    Returns:
        - ConcreteModel: returns a Pyomo model.
    """
    
    model = ConcreteModel()
    
    load_model_sets_parameters_variables(model, stn_data, planning_horizon)
    load_basic_model_constraints_objective(model, stn_data, planning_horizon, 'base_model')
    
    formulation_name = "F0"
    
    return model, formulation_name


def create_model_f1_basic_preprocessing_formulation(stn_data: dict, planning_horizon: int) -> tuple[ConcreteModel, str]:
    """
    Creates the enhanced MILP model with EST calculations and additional constraints.
    
    Args:
        - stn_data (dict): a dictionary with the state-task network instance data.
        - planning_horizon (int): planning horizon.

    Returns:
        - ConcreteModel: returns a Pyomo model.
    """
    
    model = ConcreteModel()
    
    load_model_sets_parameters_variables(model, stn_data, planning_horizon)
    load_basic_model_constraints_objective(model, stn_data, planning_horizon, 'base_model')    
    compute_est_subsequent_tasks(model, stn_data)
    compute_est_group_tasks(model, stn_data)
    create_est_parameters(model, stn_data)
    create_ppc_parameters(model, stn_data)
    load_constraints_set_to_zero_x_ys_est(model)
    load_constraints_preprocessing(model)
    
    formulation_name = "F1"
        
    return model, formulation_name


def create_model_f2_basic_preprocessing_optimization_formulation(stn_data: dict, planning_horizon: int) -> tuple[ConcreteModel, str]:
    """"
    Creates the enhanced MILP model with EST calculations and additional constraints based on solving knapsack problems.
    
    Args:
        - stn_data (dict): a dictionary with the state-task network instance data.
        - planning_horizon (int): planning horizon.

    Returns:
        - ConcreteModel: returns a Pyomo model.
    """
    
    compute_upper_bound_x_task(stn_data, planning_horizon)    
    compute_upper_bound_x_unit(stn_data, planning_horizon)
    compute_upper_bound_y_unit(stn_data, planning_horizon)
    
    print(stn_data['UPPER_BOUND_X_TASK'])
    print(stn_data['UPPER_BOUND_X_UNIT'])
    print(stn_data['UPPER_BOUND_Y_UNIT'])    
        
    model = ConcreteModel()
    
    load_model_sets_parameters_variables(model, stn_data, planning_horizon)
    load_basic_model_constraints_objective(model, stn_data, planning_horizon, 'base_model')       
    compute_est_group_tasks(model, stn_data)                
    create_est_parameters(model, stn_data)
    create_opt_parameters(model, stn_data)
    load_constraints_set_to_zero_x_ys_est(model)
    load_constraints_preprocessing_optimization(model)
    
    formulation_name = "F2"
        
    return model, formulation_name