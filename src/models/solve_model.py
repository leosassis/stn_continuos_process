from pyomo.environ import *
from pyomo.opt import SolverResults
from src.models.optimization_config import set_solver_options_milp, activate_model_lp_relaxation
from src.utils.utils import compute_num_variables_constraints, print_model_constraints


def solve_model(solver: Any, model: ConcreteModel) -> dict:
    
    results = solver.solve(model, tee = True)
    results.write()
    
    return results    


def solve_and_analyze_model(solver: Any, milp_model: ConcreteModel) -> tuple[SolverResults, dict, SolverResults]:
    
    set_solver_options_milp(solver)
    results_milp: SolverResults = solve_model(solver, milp_model)   
    model_analytics_milp = compute_num_variables_constraints(milp_model)     
    activate_model_lp_relaxation(milp_model)
    results_lp: SolverResults = solve_model(solver, milp_model)
    
    return results_milp, model_analytics_milp, results_lp