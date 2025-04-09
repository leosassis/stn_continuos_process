from pyomo.environ import *
from src.models.sets import create_main_sets_parameters
from src.models.variables import create_variables, init_variables 
from src.models.parameters import create_parameters
from src.models.constraints import create_constraints
from src.models.objective import create_objective_function
from src.models.optimization_config import define_solver
from src.models.constraints_tightening import create_tightening_constraints


def create_model(STN: dict, H: int) -> Any:
    
    model = ConcreteModel()
    
    create_main_sets_parameters(model, STN, H)
    create_variables(model)    
    create_parameters(model, STN, H)
    init_variables(model, H)
    create_constraints(model, STN, H)
    create_tightening_constraints(model, STN, H)
    create_objective_function(model, STN)
    
    solver = define_solver()

    return model, solver


def solve_model(solver: Any, model: ConcreteModel) -> Any:
    
    results = solver.solve(model, tee = True)
    results.write()
    
    return results    