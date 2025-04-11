import pandas as pd
import time
import numpy as np
from src.models.optimization_config import set_solver_options_milp, set_solver_options_relaxation
from src.models.create_model import solve_model, create_model
from src.utils.utils import compute_product_production, compute_total_production, get_objective_value, print_model_constraints, compute_num_variables_constraints
from src.visualization.plot_results import plot_gantt_chart_X, plot_inventory_chart, plot_gantt_chart_Y
from src.methods.fp import forward_propagation
from src.data.load_data import load_network
from src.data.preprocessing import instace_factors_network
from src.methods.est import compute_est_cuts


def main():
    """ 
    Main function to run the model.
    """    
    
    # Step 0: Load Data to Create Instances
    #networks, cases, planning_horizon_array, tau_factor_max, beta_factor_max = instace_factors_network()
    
    #for network in networks:
    #    for case in cases:
    #        for H in planning_horizon_array:
    #            for tau_factor in range(1, tau_factor_max):
    #                for beta_factor in range(1, beta_factor_max):
                        
                        # Step 1: Create Network            
    STN = load_network("network_1", "fast_upstream", 2, 3)
    
    # Step 2: Build the optimization model
    model, solver = create_model(STN, 25)
    
    compute_est_cuts(model, STN)
    
    # Step 3: Define solver configurations        
    #set_solver_options_milp(solver)
    #set_solver_options_relaxation(model)
    
    """ try:
        # Step 4: Solve the model
        start_time = time.time()
        results = solve_model(solver, model)
        end_time = time.time()
        
        # Step 5: Analyze and visualize the solution    
        #plot_gantt_chart_X(H, model) 
                    
            
    except:
        print("Model was not loaded/solved correctly or it was interrupted.")
     """        
    
if __name__=="__main__":
    
    main()      