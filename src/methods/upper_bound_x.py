from pyomo.environ import *
from numpy import floor
from src.utils.utils import print_dict
from src.models.optimization_config import define_solver
from src.utils.utils import print_model_constraints

def compute_upper_bound_x(model: ConcreteModel, STN: dict) -> None:
    """ 
    Computes upper bounds on x variables based on its operational window.
    """
    
    est = STN['EST']
    number_ys = {}
    upper_bound_x = {}
    number_remaining_periods_for_x = {}
    
    S_Time = model.S_Time
    
    for j, i in est:
        
        tau_max = model.P_Tau_Max[i,j]
        tau_min = model.P_Tau_Min[i,j]
        tau_end = model.P_Tau_End_Task[i]
        
        number_ys[j,i] = floor((max(S_Time) + 1 - est[j,i])/(tau_max + tau_end))
        upper_bound_x[j,i] = number_ys[j,i]*tau_max
        number_remaining_periods_for_x[j,i] = max(0, max(S_Time) - est[j,i] - number_ys[j,i]*(tau_max + tau_end))    
    
        for tau in range(int(tau_max) -1, int(tau_min) -1, -1):
            if tau <= number_remaining_periods_for_x[j,i]:
                upper_bound_x[j,i] += tau
                break        
    
    STN['UPPER_BOUND_X'] = upper_bound_x
    print_dict(upper_bound_x)
    

def knapsack_constraint(model_max_runs: ConcreteModel, num_production_time_points: int, tau_end: int) -> Constraint:
    """
    Defines the knapsack constraint limited by the number of possible production time points. 
    """
    
    return sum((run_lenght + tau_end) * model_max_runs.V_Number_Runs[run_lenght] for run_lenght in model_max_runs.S_Run_Lenghts) <= num_production_time_points

def define_objective(model_max_runs: ConcreteModel, tau_end: int) -> Objective:
    """
    Defines the objective function to maximize the number of production time points. 
    """
    
    return sum((run_lenght) * model_max_runs.V_Number_Runs[run_lenght] for run_lenght in model_max_runs.S_Run_Lenghts)


def compute_upper_bound_x_knapsack_problem(model: ConcreteModel, STN: dict) -> None:
    """ 
    The optimization problem defines the combination of different run lenghts that maximizes the number of production time points. 
    """
        
    est = STN['EST']
    num_periods = max(model.S_Time)
    upper_bound_x = {}
    objective = {}
    
    for (j,i) in est:
        
        tau_max_periods = model.P_Tau_Max[i,j]
        tau_min_periods = model.P_Tau_Min[i,j]
        tau_end = model.P_Tau_End_Task[i]
        model_max_runs = ConcreteModel()
        
        num_production_time_points = num_periods + 1 - est[j,i]
        model_max_runs.S_Run_Lenghts = RangeSet(tau_min_periods, tau_max_periods)
        model_max_runs.V_Number_Runs = Var(model_max_runs.S_Run_Lenghts, domain = NonNegativeIntegers)
        model_max_runs.C_Knapsack_Constraint = Constraint(rule = knapsack_constraint(model_max_runs, num_production_time_points, tau_end))
        model_max_runs.C_Objective = Objective(expr = define_objective(model_max_runs, tau_end), sense = maximize)
        
        solver = define_solver()
        solver.solve(model_max_runs, tee = False)
        
        upper_bound_x[j,i] = sum(run_lenght * model_max_runs.V_Number_Runs[run_lenght].value for run_lenght in model_max_runs.S_Run_Lenghts)
        print(f"upper_bound_x[{j},{i}]={upper_bound_x[j,i]}")
        objective[j,i] = sum(run_lenght * model_max_runs.V_Number_Runs[run_lenght].value for run_lenght in model_max_runs.S_Run_Lenghts)
        print(f"number_of_runs[{j},{i}]={objective[j,i]}")
        
        model_max_runs.V_Number_Runs.display()
        #print_model_constraints(model_max_runs)
    
    STN['UPPER_BOUND_X'] = upper_bound_x   
        
    print_dict(upper_bound_x)
    print_dict(objective)
    model_max_runs.V_Number_Runs.display()