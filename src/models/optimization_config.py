from pyomo.environ import *


def define_solver() -> Any:
    """ 
    Defines Gurobi as the solver.
    """
    
    return SolverFactory('gurobi')


def set_solver_options_milp(solver: Any) -> None: 
    """ 
    Defines solver options.
    """  
    
    #solver.options['MIPGap'] = 0.01  # Set MIP gap
    solver.options['TimeLimit'] = 3600  # Set time limit


def activate_model_lp_relaxation(model: ConcreteModel) -> None:    
    """ 
    Relaxes binary and integer variables.
    """    
    
    for var in model.component_objects(Var, active=True):            
        for index in var:                
            if var[index].domain == Binary:
                var[index].setlb(0)
                var[index].setub(1)
                var[index].domain = Reals                
            elif var[index].domain == Integers:
                var[index].domain = Reals     