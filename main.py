import pandas as pd
import logging
from itertools import product
from src.models.model_solve import define_solver
from src.models.formulation_build import create_model_f0_base_formulation, create_model_f1_basic_preprocessing_formulation, create_model_f2_basic_preprocessing_optimization_formulation
from src.data.instance_generation import load_network, instance_factors_network
from src.data.postprocessing import initialize_results_dict, create_dict_result
from src.models.model_solve import solve_and_analyze_model 
import sys
import json

# Get the command line argument
command_line_args = sys.argv[1:]
assert len(command_line_args) == 1
taskID = int(command_line_args[0])

# Constant
RESULTS_PATH = "src/results/model_results.xlsx"

# Set up logging
logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')


def run_instance(network: str, case: str, planning_horizon: int, tau_factor: int, beta_factor: int, formulation_number: int) -> dict:
    """ 
    Builds, solves, and analyze one optimization instance.    
    
    Args:
        - network (str): name of network to be optimized.
        - case (str): network configuration (e.g., fast_upstream, uniform, slow_upstream).
        - planning_horizon (int): size of the planning horizon. 
        - tau_factor (int): factor to multiply tau parameters when creating instances.
        - beta_factor (int): factor to multiply beta parameters when creating instances.
    
    Returns:
        - dict: a dictionary of results for excel logging.
    """    
    
    # Step 0: Initialize results dict
    result = initialize_results_dict(network, case, planning_horizon, tau_factor, beta_factor, formulation_name = "")
    
    try:
        
        logging.info(f"Running instance: network = {network}, case = {case}, horizon = {planning_horizon}, tau_factor = {tau_factor}, beta_factor = {beta_factor}")
        
        # Step 1: Load network            
        stn_data = load_network(network, case, tau_factor, beta_factor)
        
        # Step 2: Define the solver
        solver = define_solver()
        
        # Step 3: Build, configure and solve the MILP model  
        if formulation_number == 0:      
            model_milp, formulation_name = create_model_f0_base_formulation(stn_data, planning_horizon)
        elif formulation_number == 1:
            model_milp, formulation_name = create_model_f1_basic_preprocessing_formulation(stn_data, planning_horizon)
        elif formulation_number == 2:
            model_milp, formulation_name = create_model_f2_basic_preprocessing_optimization_formulation(stn_data, planning_horizon)
        else:
            raise Exception(f"Fomrulation number {formulation_number} is not recognized.")
        results_milp, stats_milp, results_lp = solve_and_analyze_model(solver, model_milp, planning_horizon)
        
        # Step 4: Create result dictionary
        result = create_dict_result(result, stats_milp, results_milp, results_lp, formulation_name)
        
        logging.info(
            f"Models were solved. Formulation: {formulation_name}. MILP Objective: {round(results_milp.problem.lower_bound, 2)}." 
        )                       
            
    except Exception as e:
        
        logging.error(
            f"Error while solving instance {network}, {case}, horizon = {planning_horizon}, tau_factor = {tau_factor}, beta_factor = {beta_factor}, formulation = {formulation_name}"
        )
        logging.exception(e)
        
    return result


def main(taskID: int) -> None:
    """ 
    Main function to run multiple instances of the optimization problem.
    """
    
    runNumber = taskID
    
    with open(f"input_data/datasets/run_{runNumber:03}.json", "r") as f:
        dct = json.load(f)    
    
    print(dct)
    network, case, planning_horizon, tau_factor, beta_factor = dct["network"], dct["case"], dct["planning_horizon"], dct["tau_factor"], dct["beta_factor"]
    #formulationNumber = taskID % 3
    formulationNumber = 0
    
    result = run_instance(network, case, planning_horizon, tau_factor, beta_factor, formulationNumber)
    
    with open(f"src/results/result_{taskID:03}.json", "w") as f:
        json.dump(result, f)
                                
    
if __name__=="__main__":
    
    main(taskID)      