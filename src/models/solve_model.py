from pyomo.environ import *
from pyomo.opt import SolverResults
from src.models.optimization_config import set_solver_options_milp, activate_model_lp_relaxation
from src.utils.utils import compute_num_variables_constraints, print_model_constraints
from src.visualization.plot_results import plot_gantt_chart


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


def solve_and_analyze_model(solver: Any, model_milp: ConcreteModel, planning_horizon: int) -> tuple[SolverResults, dict, SolverResults]:
    """
    Solves the MILP model, analyzes it, and solves its LP relaxation.
    There is also the possibility to print Gantt charts.

    Args:
        - solver (Any): a Pyomo solver instance.
        - model_milp (ConcreteModel): the MILP Pyomo model to be solved.
        - planning_horizon (int): size of the planning horizon.

    Returns:
        Tuple[
            SolverResults: results from solving the MILP,
            dict: model analytics (number of variables, constraints, etc.),
            SolverResults: results from solving the LP relaxation
        ]
    """
    
    set_solver_options_milp(solver)
    results_milp: SolverResults = solve_model(solver, model_milp)   
    model_analytics_milp = compute_num_variables_constraints(model_milp)
    #plot_gantt_chart(planning_horizon, model_milp, "X") 
    #plot_gantt_chart(planning_horizon, model_milp, "Y")     
    #plot_gantt_chart(planning_horizon, model_milp, "B")     
    
    activate_model_lp_relaxation(model_milp)
    results_lp: SolverResults = solve_model(solver, model_milp)
    #plot_gantt_chart(planning_horizon, model_milp, "X") 
    #plot_gantt_chart(planning_horizon, model_milp, "Y")     
    #plot_gantt_chart(planning_horizon, model_milp, "B")     
    
    return results_milp, model_analytics_milp, results_lp