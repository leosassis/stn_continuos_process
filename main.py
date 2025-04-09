import pandas as pd
import time
import numpy as np
from src.models.optimization_config import set_solver_options_milp, set_solver_options_relaxation
from src.models.create_model import solve_model, create_model
from src.utils.utils import compute_product_production, compute_total_production, get_objective_value, print_model_constraints, compute_num_variables_constraints
from src.visualization.plot_results import plot_gantt_chart_X, plot_inventory_chart, plot_gantt_chart_Y
from src.methods.fp import forward_propagation
from src.data.load_data import load_data

def main():
    """ 
    Main function to run the model.
    """    
    
    H_Values = range(55, 56, 55)

    for H in H_Values:
        
        # Step 1: Load data            
        STN = load_data()
        
        # Step 2: Build the optimization model
        model, solver = create_model(STN, H)
        
        # Step 3: Define solver configurations        
        set_solver_options_milp(solver)
        #set_solver_options_relaxation(model)
        
        try:
            # Step 4: Solve the model
            start_time = time.time()
            results = solve_model(solver, model)
            end_time = time.time()
            
            # Step 5: Analyze and visualize the solution    
            plot_gantt_chart_X(H, model) 
            plot_gantt_chart_Y(H, model) 
            
                
        except:
            print("Model was not loaded/solved correctly or it was interrupted.")
            
    
if __name__=="__main__":
    
    main()      