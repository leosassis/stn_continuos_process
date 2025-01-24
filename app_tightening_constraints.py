
##########################################################
#The current model has no utility constraints.           # 
#It assumes unlimited amount of raw materials            #
#It assume no delays: idis, idly, rmi_dly, rmi_n         #
#It assumes no batch units: j_b                          #
#There is no pre-defined tasks for n=0: i_ini            #
##########################################################
import pandas as pd
import time
import numpy as np
from pyomo.environ import *
from optimization import set_solver_options, solve_model, print_model_constraints, compute_num_variables_constraints
from sets import create_main_sets_parameters
from variables import create_variables, init_variables 
from parameters import create_parameters
from utils import plot_gantt_chart, plot_inventory_chart
from fp import forward_propagation
from objective import create_objective_function, get_objective_value
from constraints import create_constraints, add_fp_constraint

from network_2 import define_stn_network
#from network_3 import *

# List to store results for each instance
results_list = []

H_Values = range(25, 101, 25)
beta_min_factors = np.arange(1, 0.49, -0.25)
tau_max_factors = np.arange(1.2, 1.81, 0.2)

for H in H_Values:
    for beta_min_factor in beta_min_factors:
        for tau_max_factor in tau_max_factors:
            print(f"Solving model for H={H}, beta_min_factor={beta_min_factor}, tau_max_factor={tau_max_factor}")
    
            #Define STN network.
            STN = define_stn_network(beta_min_factor, tau_max_factor)
            
            #Create model.
            model = ConcreteModel()
            create_main_sets_parameters(model, STN, H)
            create_variables(model)    
            create_parameters(model, STN, H)
            init_variables(model, H)
            create_constraints(model, STN, H)
            create_objective_function(model, STN, minimize, 'total_cost')
            
            #Solve original model.
            solver = SolverFactory('gurobi')
            set_solver_options(solver, model, model_nature = 'original_model')
            start_time = time.time()
            results = solve_model(solver, model)
            end_time = time.time()    
            
            num_total_vars, num_binary_vars, num_constraints = compute_num_variables_constraints(model)
            objective_value = get_objective_value(model, STN)
            termination_condition = results.solver.termination_condition
            
            print('New Model----------------------------------')
            
            #Solve LP relaxation.
            solver = SolverFactory('gurobi')
            set_solver_options(solver, model, model_nature = 'relaxed_model')
            solve_model(solver, model)
            
            lp_objective_value = get_objective_value(model, STN)
                
            instance_name = f"H{H}_BetaMinFactor{beta_min_factor}_TauMaxFactor{tau_max_factor}"
            
            # Add results as a dictionary
            results_list.append({
                "Instance": instance_name,
                "Objective Function": objective_value,
                "LP Relaxation Objective": lp_objective_value,
                "Solution Time (s)": end_time - start_time,
                "Optimality Gap": termination_condition,
                "Number of Constraints": num_constraints,
                "Total Variables": num_total_vars,
                "Binary Variables": num_binary_vars
            })

            # Convert results list to DataFrame
            results_df = pd.DataFrame(results_list)

            # Save results to Excel
            results_df.to_excel("model_results.xlsx", index=False)
                
