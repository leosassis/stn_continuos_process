from pyomo.environ import *
from src.models.sets import create_main_sets_parameters
from src.models.variables import create_variables, init_variables 
from src.models.parameters import create_parameters, create_est_parameters
from src.models.constraints import create_constraints
from src.models.objective import create_objective_function
from src.models.constraints_est import create_constraints_est
from src.methods.est import compute_est
from src.methods.upper_bound_x import compute_upper_bound_x, compute_upper_bound_x_unit
from pyomo.opt import SolverResults
from src.utils.utils import compute_num_variables_constraints
from src.models.optimization_config import set_solver_options_milp, activate_model_lp_relaxation


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
    compute_est(model, STN)
    compute_upper_bound_x(model, STN)
    compute_upper_bound_x_unit(model, STN)
    create_est_parameters(model, STN)
    create_constraints_est(model)
        
    return model


def solve_model(solver: Any, model: ConcreteModel) -> Any:
    
    results = solver.solve(model, tee = True)
    results.write()
    
    return results    


def solve_and_analyze_model(solver: Any, milp_model: ConcreteModel) -> tuple[SolverResults, SolverResults, dict]:
    
    set_solver_options_milp(solver)
    results_milp: SolverResults = solve_model(solver, milp_model)   
    model_analytics_milp = compute_num_variables_constraints(milp_model)     
    activate_model_lp_relaxation(milp_model)
    results_lp: SolverResults = solve_model(solver, milp_model)
    
    return results_milp, model_analytics_milp, results_lp
