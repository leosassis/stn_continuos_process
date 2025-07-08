from pyomo.environ import *
from pyomo.opt import SolverResults
from src.utils.utils import compute_num_variables_constraints
from src.visualization.plot_results import plot_gantt_chart
from src.utils.utils import print_model_constraints

def define_solver() -> Any:
    """ 
    Defines Gurobi as the solver.
    
    Args:
        - none.
    
    Returns:
        - solver (Any): Pyomo SolverFactory instance configured for Gurobi.
    """
    
    return SolverFactory('gurobi')


def set_solver_options_milp(solver: Any, mip_gap_multiplier) -> None: 
    """ 
    Sets solver options for MILP optimization.
    
    Args:
        - solver (Any): Pyomo solver instance (e.g., Gurobi).
        - mip_gap_multiplier (int): multiplier to increase the mip gap.
    
    Returns:
        - none.
    """  
    
    solver.options['MIPGap'] = mip_gap_multiplier * 0.0001  # Set MIP gap
    solver.options['TimeLimit'] = 24 * 3600  # Set time limit


def activate_model_lp_relaxation(model: ConcreteModel) -> None:    
    """ 
    Relaxes all binary and integer variables in the model to continuous variables.
    
    Args:
        - model (ConcreteModel): Pyomo model instance.
    
    Returns:
        - none.
    """   
    
    for var in model.component_objects(Var, active=True):            
        for index in var:                
            if var[index].domain == Binary:
                var[index].setlb(0)
                var[index].setub(1)
                var[index].domain = Reals                
            elif var[index].domain == Integers:
                var[index].domain = Reals     
                
                
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


def solve_and_analyze_model(solver: Any, model_milp: ConcreteModel, planning_horizon: int, mip_gap_multiplier: int) -> tuple[SolverResults, dict, SolverResults]:
    """
    Solves the MILP model, analyzes it, and solves its LP relaxation.
    There is also the possibility to print Gantt charts.

    Args:
        - solver (Any): a Pyomo solver instance.
        - model_milp (ConcreteModel): the MILP Pyomo model to be solved.
        - planning_horizon (int): size of the planning horizon.
        - mip_gap_multiplier (int): multiplier to increase the mip gap.

    Returns:
        Tuple[
            SolverResults: results from solving the MILP,
            dict: model analytics (number of variables, constraints, etc.),
            SolverResults: results from solving the LP relaxation
        ]
    """
    
    
    set_solver_options_milp(solver, mip_gap_multiplier)
    
    results_milp: SolverResults = solve_model(solver, model_milp)   
    model_analytics_milp = compute_num_variables_constraints(model_milp)
    #plot_gantt_chart(planning_horizon, model_milp, "X")
    #plot_gantt_chart(planning_horizon, model_milp, "Y")
    #plot_gantt_chart(planning_horizon, model_milp, "B")
    #print_model_constraints(model_milp)
    
    activate_model_lp_relaxation(model_milp)
    results_lp: SolverResults = solve_model(solver, model_milp)
    #plot_gantt_chart(planning_horizon, model_milp, "X")
    #plot_gantt_chart(planning_horizon, model_milp, "Y")
    #plot_gantt_chart(planning_horizon, model_milp, "B")
    
    return results_milp, model_analytics_milp, results_lp