from pyomo.environ import *
from sets import create_main_sets_parameters
from variables import create_variables, init_variables 
from parameters import create_parameters
from constraints import create_constraints
from objective import create_objective_function

def set_solver_options(solver, model, model_nature) -> None:
      
    if model_nature == 'original_model':
        
        print("#######################")
        print("Original Solution......")
        print("#######################\n")
        
        #solver.options['MIPGap'] = 0.01  # Set MIP gap
        solver.options['TimeLimit'] = 1200  # Set time limit
    
    elif model_nature == 'relaxed_model':
        
        print("#######################")
        print("Relaxed Solution.......")
        print("#######################\n")
        
        for var in model.component_objects(Var, active=True):            
            for index in var:                
                if var[index].domain == Binary:
                    var[index].setlb(0)
                    var[index].setub(1)
                    var[index].domain = Reals                
                elif var[index].domain == Integers:
                    var[index].domain = Reals     
    
    else:
        raise ValueError(f"Unknown model_nature: {model_nature}")       
    
def solve_model(solver, model):
    
    results = solver.solve(model, tee = True)
    results.write()
    return results

def print_model_constraints(model):
    
    for con in model.component_map(Constraint).itervalues():
        con.pprint()
        
def compute_num_variables_constraints(model):
    
        num_constraints = sum(len(constraint) for constraint in model.component_objects(Constraint, active=True))
        num_total_vars = sum(len(var) for var in model.component_objects(Var, active=True))
        num_binary_vars = sum(1 for v in model.component_objects(Var, active=True) for index in v if v[index].domain == Binary)
        
        return num_total_vars, num_binary_vars, num_constraints

def create_model(model, STN, H):
    
    create_main_sets_parameters(model, STN, H)
    create_variables(model)    
    create_parameters(model, STN, H)
    init_variables(model, H)
    create_constraints(model, STN, H)
    create_objective_function(model, STN)