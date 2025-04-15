from pyomo.environ import *
from src.models.sets import create_main_sets_parameters
from src.models.variables import create_variables, init_variables 
from src.models.parameters import create_parameters, create_est_parameters
from src.models.constraints import create_constraints
from src.models.objective import create_objective_function
from src.models.constraints_est import create_constraints_est
from src.methods.est import compute_est_cuts


def create_model(STN: dict, H: int) -> ConcreteModel:
    
    model = ConcreteModel()
    
    create_main_sets_parameters(model, STN, H)
    create_variables(model)    
    create_parameters(model, STN, H)
    init_variables(model, H)
    create_constraints(model)
    create_objective_function(model, STN)
    
    return model


def create_model_est(STN: dict, H: int) -> ConcreteModel:
    
    model = ConcreteModel()
    
    create_main_sets_parameters(model, STN, H)
    create_variables(model)    
    create_parameters(model, STN, H)
    init_variables(model, H)
    create_constraints(model)
    create_objective_function(model, STN)    
    compute_est_cuts(model, STN)
    create_est_parameters(model, STN)
    create_constraints_est(model)
        
    return model


def solve_model(solver: Any, model: ConcreteModel) -> Any:
    
    results = solver.solve(model, tee = True)
    results.write()
    
    return results    