from pyomo.environ import *
from pyomo.opt import SolverResults
from src.models.optimization_config import set_solver_options_milp, activate_model_lp_relaxation
from src.utils.utils import compute_num_variables_constraints, print_model_constraints


def solve_model(solver: Any, model: ConcreteModel) -> SolverResults:
    """
    Solves the given Pyomo model using the provided solver.

    Args:
        - solver (Any): a Pyomo solver instance (e.g., SolverFactory("gurobi")).
        - model (ConcreteModel): the Pyomo model to be solved.

    Returns:
        - SolverResults: results of the solver execution.
    """
    
    results = solver.solve(model, tee = True)
    results.write()
    
    return results    


def solve_and_analyze_model(solver: Any, milp_model: ConcreteModel) -> tuple[SolverResults, dict, SolverResults]:
    """
    Solves the MILP model, analyzes it, and solves its LP relaxation.

    Args:
        - solver (Any): a Pyomo solver instance.
        - milp_model (ConcreteModel): the MILP Pyomo model to be solved.

    Returns:
        Tuple[
            SolverResults: results from solving the MILP,
            dict: model analytics (number of variables, constraints, etc.),
            SolverResults: results from solving the LP relaxation
        ]
    """
    
    set_solver_options_milp(solver)
    results_milp: SolverResults = solve_model(solver, milp_model)   
    model_analytics_milp = compute_num_variables_constraints(milp_model)     
    #activate_model_lp_relaxation(milp_model)
    #results_lp: SolverResults = solve_model(solver, milp_model)
    
    #return results_milp, model_analytics_milp, results_lp
    return results_milp, model_analytics_milp