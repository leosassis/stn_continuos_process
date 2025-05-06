from pyomo.environ import *
from src.models.sets import create_main_sets_parameters
from src.models.variables import create_variables, init_variables 
from src.models.parameters import create_parameters, create_est_parameters
from src.models.constraints import create_constraints
from src.models.objective import create_objective_function
from src.models.constraints_est import create_constraints_est
from src.methods.est import compute_est
from src.methods.upper_bound_x import compute_upper_bound_x, compute_upper_bound_x_unit
from src.utils.utils import print_model_constraints


def create_model_f0(state_task_network: dict, planning_horizon: int) -> ConcreteModel:
    
    model = ConcreteModel()
    
    create_main_sets_parameters(model, state_task_network, planning_horizon)
    create_variables(model)    
    create_parameters(model, state_task_network, planning_horizon)
    init_variables(model, planning_horizon)
    create_constraints(model)
    create_objective_function(model, state_task_network)
    
    return model


def create_model_f1(state_task_network: dict, planning_horizon: int) -> ConcreteModel:
    
    model = ConcreteModel()
    
    create_main_sets_parameters(model, state_task_network, planning_horizon)
    create_variables(model)    
    create_parameters(model, state_task_network, planning_horizon)
    init_variables(model, planning_horizon)
    create_constraints(model)
    create_objective_function(model, state_task_network)    
    compute_est(model, state_task_network)
    compute_upper_bound_x(model, state_task_network)
    compute_upper_bound_x_unit(model, state_task_network)
    create_est_parameters(model, state_task_network)
    create_constraints_est(model)
        
    return model
