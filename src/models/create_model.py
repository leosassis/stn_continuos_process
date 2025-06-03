from pyomo.environ import *
from src.models.sets import create_main_sets_parameters
from src.models.variables import create_variables, init_variables 
from src.models.parameters import create_parameters, create_ppc_parameters, create_opt_parameters
from src.models.constraints import load_basic_model_constraints
from src.models.objective import create_objective_function
from src.models.constraints_est import create_constraints_est_f1, create_constraints_est_f2 
from src.methods.est import compute_est_subsequent_tasks, compute_est_group_tasks
from methods.upper_bound_x_task_opt import compute_upper_bound_x, compute_upper_bound_x_unit
from methods.upper_bound_ys_x_unit_opt import compute_upper_bound_ys_unit


def _initialize_base_model(model: ConcreteModel, state_task_network: dict, planning_horizon: int) -> None:
    """
    Initializes base model components: sets, variables, parameters, and constraints.
    
    Args:
        - model (ConcreteModel): an empty Pyomo model to be configured.
        - state_task_network (dict): a dictionary with the state-task network instance data.
        - planning_horizon (int): planning horizon.

    Returns:
        - None. modifies the model in-place.    
    """
    
    create_main_sets_parameters(model, state_task_network, planning_horizon)
    create_variables(model)    
    create_parameters(model, state_task_network, planning_horizon)
    init_variables(model, planning_horizon)
    load_basic_model_constraints(model)
    create_objective_function(model, state_task_network)
    

def create_model_f0(state_task_network: dict, planning_horizon: int) -> tuple[ConcreteModel, str]:
    """
    Creates the base MILP model.
    
    Args:
        - state_task_network (dict): a dictionary with the state-task network instance data.
        - planning_horizon (int): planning horizon.

    Returns:
        - ConcreteModel: returns a Pyomo model.
    """
    
    model = ConcreteModel()
    
    _initialize_base_model(model, state_task_network, planning_horizon)
    formulation_name = "F0"
    
    return model, formulation_name


def create_model_f1(state_task_network: dict, planning_horizon: int) -> tuple[ConcreteModel, str]:
    """
    Creates the enhanced MILP model with EST calculations and additional constraints.
    
    Args:
        - state_task_network (dict): a dictionary with the state-task network instance data.
        - planning_horizon (int): planning horizon.

    Returns:
        - ConcreteModel: returns a Pyomo model.
    """
    
    model = ConcreteModel()
    
    _initialize_base_model(model, state_task_network, planning_horizon)    
    compute_est_subsequent_tasks(model, state_task_network)
    compute_est_group_tasks(model, state_task_network)
    create_ppc_parameters(model, state_task_network)
    create_constraints_est_f1(model)
    formulation_name = "F1"
        
    return model, formulation_name


def create_model_f2(state_task_network: dict, planning_horizon: int) -> tuple[ConcreteModel, str]:
    """
    Creates the enhanced MILP model with EST calculations and additional constraints based on solving knapsack problems.
    
    Args:
        - state_task_network (dict): a dictionary with the state-task network instance data.
        - planning_horizon (int): planning horizon.

    Returns:
        - ConcreteModel: returns a Pyomo model.
    """
    
    model = ConcreteModel()
    
    _initialize_base_model(model, state_task_network, planning_horizon)    
    compute_est_subsequent_tasks(model, state_task_network)
    compute_est_group_tasks(model, state_task_network)
    compute_upper_bound_x(model, state_task_network)
    compute_upper_bound_x_unit(model, state_task_network)
    compute_upper_bound_ys_unit(model, state_task_network)
    create_ppc_parameters(model, state_task_network)
    create_opt_parameters(model, state_task_network)
    create_constraints_est_f2(model)
    formulation_name = "F2"
        
    return model, formulation_name
