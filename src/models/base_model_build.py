from pyomo.environ import *
from src.models.sets import create_main_sets_parameters
from src.models.variables import create_variables, init_variables 
from src.models.parameters import create_basic_parameters
from src.models.constraints import load_constraints_basic_model, load_constraints_basic_model_for_operations_x_y
from src.models.objective import create_objective_function


def load_model_sets_parameters_variables(model: ConcreteModel, stn_data: dict, planning_horizon: int) -> None:
    """
    Initializes base model components: sets, variables and parameters.
    
    Args:
        - model (ConcreteModel): an empty Pyomo model to be configured.
        - stn_data (dict): a dictionary with the state-task network instance data.
        - planning_horizon (int): planning horizon.
    
    Returns:
        - None. modifies the model in-place.    
    """    
    
    create_main_sets_parameters(model, stn_data, planning_horizon)
    create_variables(model)    
    create_basic_parameters(model, stn_data, planning_horizon)
    init_variables(model, planning_horizon)
    

def load_basic_model_constraints_objective(model: ConcreteModel, stn_data: dict, planning_horizon: int, model_type: str) -> None:
    """
    Initializes base model components: sets, variables, parameters, and constraints.
    
    Args:
        - model (ConcreteModel): an empty Pyomo model to be configured.
        - stn_data (dict): a dictionary with the state-task network instance data.
        - planning_horizon (int): planning horizon.
        - model_type (str): a string indicating which base model to load (e.g., 'base_model', 'bound_production_operations', 'bound_startups')

    Returns:
        - None. modifies the model in-place.    
    """
    
    if model_type == 'base_model':
        load_constraints_basic_model(model)
        create_objective_function(model, stn_data, 'base_model')
    elif model_type == 'bound_production_operations':
        load_constraints_basic_model_for_operations_x_y(model)
        create_objective_function(model, stn_data, 'bound_production_operations')
    elif model_type == 'bound_startups':
        load_constraints_basic_model_for_operations_x_y(model)
        create_objective_function(model, stn_data, 'bound_startups')
        