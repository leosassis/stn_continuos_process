from pyomo.environ import *
from src.models.base_model_build import load_model_sets_parameters_variables, load_basic_model_constraints_objective
from src.models.parameters import create_parameters_tightening_constraints
from src.models.constraints_est import (load_constraint_set_to_zero_x_est, 
                                        load_constraint_set_to_zero_ys_est,
                                        load_constraint_ub_ys_task,
                                        load_constraint_ub_ys_unit,
                                        load_constraint_ub_x_task,
                                        load_constraint_ub_x_unit,
                                        load_constraint_clique_X_group_k,
                                        load_constraint_clique_Y_group_k) 
from src.methods.est import compute_est_subsequent_tasks
from src.methods.est_group import compute_est_group_tasks
from src.methods.upper_bound_x_task_opt import compute_upper_bound_x_task
from src.methods.upper_bound_ys_x_unit_opt import (compute_upper_bound_x_unit, 
                                                   compute_upper_bound_y_unit)


def create_model_f1_base_formulation(stn_data: dict, planning_horizon: int) -> tuple[ConcreteModel, str]:
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
    
    formulation_name = "F1_Base_Model"
    
    return model, formulation_name


def create_model_f2_X_YS_zero_est(stn_data: dict, planning_horizon: int) -> tuple[ConcreteModel, str]:
    """
    Creates the base MILP model plus the constraints that sets X and YS to 0 from n = 0 to n = est - 1.
    
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
    create_parameters_tightening_constraints(model, stn_data, "")
    load_constraint_set_to_zero_x_est(model)
    load_constraint_set_to_zero_ys_est(model)
    
    formulation_name = "F2_X_YS_0_EST"
    
    return model, formulation_name


def create_model_f3_ub_YS_task(stn_data: dict, planning_horizon: int) -> tuple[ConcreteModel, str]:
    """
    Creates the base MILP model plus the constraint that sets YS to 0 from n = 0 to n = est - 1.
    
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
    create_parameters_tightening_constraints(model, stn_data, "UB_YS_Task")
    load_constraint_set_to_zero_x_est(model)
    load_constraint_set_to_zero_ys_est(model)
    load_constraint_ub_ys_task(model)
    
    formulation_name = "F3_UB_YS_Task"
    
    return model, formulation_name


def create_model_f4_ub_YS_unit(stn_data: dict, planning_horizon: int) -> tuple[ConcreteModel, str]:
    """
    Creates the base MILP model plus the constraint that sets YS to 0 from n = 0 to n = est - 1.
    
    Args:
        - stn_data (dict): a dictionary with the state-task network instance data.
        - planning_horizon (int): planning horizon.

    Returns:
        - ConcreteModel: returns a Pyomo model.
    """
    
    compute_upper_bound_y_unit(stn_data, planning_horizon)
    
    model = ConcreteModel()
    
    load_model_sets_parameters_variables(model, stn_data, planning_horizon)
    load_basic_model_constraints_objective(model, stn_data, planning_horizon, 'base_model')       
    create_parameters_tightening_constraints(model, stn_data, "UB_YS_Unit")    
    load_constraint_set_to_zero_x_est(model)
    load_constraint_set_to_zero_ys_est(model)
    load_constraint_ub_ys_unit(model)
    
    formulation_name = "F4_UB_YS_Unit"
    
    return model, formulation_name


def create_model_f5_ub_X_task(stn_data: dict, planning_horizon: int) -> tuple[ConcreteModel, str]:
    """
    Creates the base MILP model plus the constraint that sets X to 0 from n = 0 to n = est - 1.
    
    Args:
        - stn_data (dict): a dictionary with the state-task network instance data.
        - planning_horizon (int): planning horizon.

    Returns:
        - ConcreteModel: returns a Pyomo model.
    """
    
    compute_upper_bound_x_task(stn_data, planning_horizon)
    
    model = ConcreteModel()
    
    load_model_sets_parameters_variables(model, stn_data, planning_horizon)
    load_basic_model_constraints_objective(model, stn_data, planning_horizon, 'base_model')       
    create_parameters_tightening_constraints(model, stn_data, "UB_X_Task")    
    load_constraint_set_to_zero_x_est(model)
    load_constraint_set_to_zero_ys_est(model)
    load_constraint_ub_x_task(model)
    
    formulation_name = "F5_UB_X_Task"
    
    return model, formulation_name


def create_model_f6_ub_X_unit(stn_data: dict, planning_horizon: int) -> tuple[ConcreteModel, str]:
    """
    Creates the base MILP model plus the constraint that sets X to 0 from n = 0 to n = est - 1.
    
    Args:
        - stn_data (dict): a dictionary with the state-task network instance data.
        - planning_horizon (int): planning horizon.

    Returns:
        - ConcreteModel: returns a Pyomo model.
    """
    
    compute_upper_bound_x_unit(stn_data, planning_horizon)
    
    model = ConcreteModel()
    
    load_model_sets_parameters_variables(model, stn_data, planning_horizon)
    load_basic_model_constraints_objective(model, stn_data, planning_horizon, 'base_model')       
    create_parameters_tightening_constraints(model, stn_data, "UB_X_Unit") 
    load_constraint_set_to_zero_x_est(model)
    load_constraint_set_to_zero_ys_est(model)   
    load_constraint_ub_x_unit(model)
    
    formulation_name = "F6_UB_X_Unit"
    
    return model, formulation_name


def create_model_f7_ub_X_group_k(stn_data: dict, planning_horizon: int) -> tuple[ConcreteModel, str]:
    """
    Creates the base MILP model plus the constraint that sets X to 0 from n = 0 to n = est - 1.
    
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
    create_parameters_tightening_constraints(model, stn_data, "EST_Group_K")    
    load_constraint_set_to_zero_x_est(model)
    load_constraint_set_to_zero_ys_est(model)
    load_constraint_clique_X_group_k(model)
    
    formulation_name = "F7_UB_X_Group_K"
    
    return model, formulation_name


def create_model_f8_ub_YS_group_k(stn_data: dict, planning_horizon: int) -> tuple[ConcreteModel, str]:
    """
    Creates the base MILP model plus the constraint that sets X to 0 from n = 0 to n = est - 1.
    
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
    create_parameters_tightening_constraints(model, stn_data, "EST_Group_K")    
    load_constraint_set_to_zero_x_est(model)
    load_constraint_set_to_zero_ys_est(model)
    load_constraint_clique_Y_group_k(model)
    
    formulation_name = "F8_UB_YS_Group_K"
    
    return model, formulation_name


def create_model_f9_ub_YS_task_unit(stn_data: dict, planning_horizon: int) -> tuple[ConcreteModel, str]:
    """
    Creates the base MILP model plus the constraint that sets YS to 0 from n = 0 to n = est - 1.
    
    Args:
        - stn_data (dict): a dictionary with the state-task network instance data.
        - planning_horizon (int): planning horizon.

    Returns:
        - ConcreteModel: returns a Pyomo model.
    """
    
    compute_upper_bound_y_unit(stn_data, planning_horizon)
    
    model = ConcreteModel()
    
    load_model_sets_parameters_variables(model, stn_data, planning_horizon)
    load_basic_model_constraints_objective(model, stn_data, planning_horizon, 'base_model')       
    create_parameters_tightening_constraints(model, stn_data, "UB_YS_Task")
    create_parameters_tightening_constraints(model, stn_data, "UB_YS_Unit")
    load_constraint_set_to_zero_x_est(model)
    load_constraint_set_to_zero_ys_est(model)
    load_constraint_ub_ys_task(model)
    load_constraint_ub_ys_unit(model)
    
    formulation_name = "F9_UB_YS_Task_Unit"
    
    return model, formulation_name


def create_model_f10_ub_X_task_unit(stn_data: dict, planning_horizon: int) -> tuple[ConcreteModel, str]:
    """
    Creates the base MILP model plus the constraint that sets X to 0 from n = 0 to n = est - 1.
    
    Args:
        - stn_data (dict): a dictionary with the state-task network instance data.
        - planning_horizon (int): planning horizon.

    Returns:
        - ConcreteModel: returns a Pyomo model.
    """
    
    compute_upper_bound_x_task(stn_data, planning_horizon)
    compute_upper_bound_x_unit(stn_data, planning_horizon)
    
    model = ConcreteModel()
    
    load_model_sets_parameters_variables(model, stn_data, planning_horizon)
    load_basic_model_constraints_objective(model, stn_data, planning_horizon, 'base_model')       
    create_parameters_tightening_constraints(model, stn_data, "UB_X_Task")
    create_parameters_tightening_constraints(model, stn_data, "UB_X_Unit")
    load_constraint_set_to_zero_x_est(model)
    load_constraint_set_to_zero_ys_est(model)
    load_constraint_ub_x_task(model)
    load_constraint_ub_x_unit(model)
    
    formulation_name = "F10_UB_X_Task_Unit"
    
    return model, formulation_name


def create_model_f11_ub_X_YS_group_k(stn_data: dict, planning_horizon: int) -> tuple[ConcreteModel, str]:
    """
    Creates the base MILP model plus the constraint that sets X to 0 from n = 0 to n = est - 1.
    
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
    create_parameters_tightening_constraints(model, stn_data, "EST_Group_K")
    load_constraint_set_to_zero_x_est(model)
    load_constraint_set_to_zero_ys_est(model)    
    load_constraint_clique_X_group_k(model)
    load_constraint_clique_Y_group_k(model)
    
    formulation_name = "F11_UB_X_YS_Group_K"
    
    return model, formulation_name


def create_model_f12_all(stn_data: dict, planning_horizon: int) -> tuple[ConcreteModel, str]:
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
    
    model = ConcreteModel()
    
    load_model_sets_parameters_variables(model, stn_data, planning_horizon)
    load_basic_model_constraints_objective(model, stn_data, planning_horizon, 'base_model')       
    compute_est_group_tasks(model, stn_data)                
    create_parameters_tightening_constraints(model, stn_data, "All")    
    load_constraint_set_to_zero_x_est(model) 
    load_constraint_set_to_zero_ys_est(model)
    load_constraint_ub_ys_task(model)
    load_constraint_ub_ys_unit(model)
    load_constraint_ub_x_task(model)
    load_constraint_ub_x_unit(model)
    load_constraint_clique_X_group_k(model)
    load_constraint_clique_Y_group_k(model)
    
    formulation_name = "F12_All"
        
    return model, formulation_name


def create_model_f0_test(stn_data: dict, planning_horizon: int) -> tuple[ConcreteModel, str]:
    """
    Creates the base MILP model plus the constraint that sets YS to 0 from n = 0 to n = est - 1.
    
    Args:
        - stn_data (dict): a dictionary with the state-task network instance data.
        - planning_horizon (int): planning horizon.

    Returns:
        - ConcreteModel: returns a Pyomo model.
    """
    compute_upper_bound_x_task(stn_data, planning_horizon)
    #compute_upper_bound_x_unit(stn_data, planning_horizon)
    #compute_upper_bound_y_unit(stn_data, planning_horizon)        
        
    model = ConcreteModel()
    
    load_model_sets_parameters_variables(model, stn_data, planning_horizon)
    load_basic_model_constraints_objective(model, stn_data, planning_horizon, 'base_model')
    
    formulation_name = "F0_Test"
    
    return model, formulation_name