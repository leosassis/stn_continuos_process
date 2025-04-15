import pandas as pd
import time
import logging
from itertools import product
from src.models.optimization_config import set_solver_options_milp, set_solver_options_relaxation, define_solver
from src.models.create_model import solve_model, create_model, create_model_est
from src.utils.utils import compute_product_production, compute_total_production, get_objective_value, print_model_constraints, compute_num_variables_constraints
from src.visualization.plot_results import plot_gantt_chart_X, plot_inventory_chart, plot_gantt_chart_Y
from src.data.load_data import load_network
from src.data.preprocessing import instace_factors_network
from src.data.postprocessing import initialize_results_dict, create_dict_result
from pyomo.opt import SolverResults

# Set up logging
logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')


def run_instance(network: str, case: str, H: int, tau_factor: int, beta_factor:int) -> dict:
    """ 
    Builds, solves, and analyze one optimization instance.
    Returns a dictionary of results for excel logging.
    """    
    
    # Spet 0: Initialize results dict
    result = initialize_results_dict(network, case, H, tau_factor, beta_factor)
    
    try:
        
        logging.info(f"Running instance: network = {network}, case = {case}, horizon = {H}, tau_factor = {tau_factor}, beta_factor = {beta_factor}")
        
        # Step 1: Load network            
        STN = load_network(network, case, tau_factor, beta_factor)

        # Step 2: Define the solver
        solver = define_solver()
        
        # Step 3: Build, configure and solve the MILP model
        model_milp = create_model(STN, H)
        set_solver_options_milp(solver)
        results_milp: SolverResults = solve_model(solver, model_milp)
        
        set_solver_options_relaxation(model_milp)
        results_lp: SolverResults = solve_model(solver, model_milp)
    
        # Step 4: Build, configure and solve the MILP+est model
        model_milp_est = create_model_est(STN, H)
        set_solver_options_milp(solver)
        results_milp_est: SolverResults = solve_model(solver, model_milp_est)
        
        set_solver_options_relaxation(model_milp_est)
        results_est_lp: SolverResults = solve_model(solver, model_milp_est)
        
        # Step 5: Create result dictionary
        result = create_dict_result(result, model_milp, results_milp, results_lp, model_milp_est, results_milp_est, results_est_lp)
        
        # Step 6: Analyze and visualize the solution    
        #plot_gantt_chart_X(25, model) 
        
        logging.info(f"Model solved in {round(results_milp.solver.time, 2)} s. MILP Objective: {round(results_milp.problem.lower_bound, 2)}. MILP + EST Objective: {round(results_milp_est.problem.lower_bound, 2)}")            
            
    except Exception as e:
        
        logging.error(f"Error while solving instance {network}, {case}, horizon = {H}, tau_factor = {tau_factor}, beta_factor = {beta_factor}.")
        logging.exception(e)
        
    return result


def main() -> None:
    """ 
    Main function to run multiple instances of the optimization problem.
    """
    
    # Step 1: Load Data to create instances
    networks, cases, planning_horizons, tau_factor_max, beta_factor_max = instace_factors_network()
    
    # Step 2: Create combinations of parameters to create instances
    results_list = []
    
    for network, case, H, tau_factor, beta_factor in product(networks, cases, planning_horizons, range(1, tau_factor_max), range(1, beta_factor_max)):
        
        result = run_instance(network, case, H, tau_factor, beta_factor)
        results_list.append(result)
    
    # Step 3: Create an Excel file with the list of results
    df_results = pd.DataFrame(results_list)
    df_results.to_excel("src/results/model_results.xlsx", index = False)
    
    logging.info("Results saved to model_results.xlsx")
                                
    
if __name__=="__main__":
    
    main()      