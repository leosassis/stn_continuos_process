import pandas as pd
import logging
from itertools import product
from src.models.model_solve import define_solver
from src.models.formulation_build import (create_model_f1_base_formulation, 
                                          create_model_f2_X_YS_zero_est, 
                                          create_model_f3_ub_YS_task,
                                          create_model_f4_ub_YS_unit,
                                          create_model_f5_ub_X_task,
                                          create_model_f6_ub_X_unit,
                                          create_model_f7_ub_X_group_k,
                                          create_model_f8_ub_YS_group_k,
                                          create_model_f9_ub_YS_task_unit,
                                          create_model_f10_ub_X_task_unit,
                                          create_model_f11_ub_X_YS_group_k,
                                          create_model_f12_all, 
                                          create_model_f0_test)
from src.data.instance_generation import load_network
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


def run_instance(network: str, startup_cost_factor: int, planning_horizon: int, tau_factor: int, beta_factor: int, formulation_number: str, taskID: int, mip_gap_multiplier: int) -> dict:
    """ 
    Builds, solves, and analyze one optimization instance.    
    
    Args:
        - network (str): name of network to be optimized.
        - startup_cost_factor (int): factor to multiply the startup cost when creating instances.
        - planning_horizon (int): size of the planning horizon. 
        - tau_factor (int): factor to multiply tau parameters when creating instances.
        - beta_factor (int): factor to multiply beta parameters when creating instances.
        - formulation_number (str): name of the formulation.
        - taskID (int): id that identifies the data set.
        - mip_gap_multiplier (int): multiplier to increase the mip gap.
    
    Returns:
        - dict: a dictionary of results for excel logging.
    """    
    
    # Step 0: Initialize results dict
    result = initialize_results_dict(network, startup_cost_factor, planning_horizon, tau_factor, beta_factor, "", taskID, mip_gap_multiplier)
    
    try:
        
        logging.info(f"Running instance: network = {network}, startup_cost_factor = {startup_cost_factor}, horizon = {planning_horizon}, tau_factor = {tau_factor}, beta_factor = {beta_factor}, task ID = {taskID}")
        
        # Step 1: Load network            
        stn_data = load_network(network, tau_factor, beta_factor, startup_cost_factor, planning_horizon)
        
        # Step 2: Define the solver
        solver = define_solver()
        
        # Step 3: Build, configure and solve the MILP model  
        if formulation_number == 0:      
            model_milp, formulation_name = create_model_f1_base_formulation(stn_data, planning_horizon)
        elif formulation_number == 1:
            model_milp, formulation_name = create_model_f2_X_YS_zero_est(stn_data, planning_horizon)
        elif formulation_number == 2:
            model_milp, formulation_name = create_model_f3_ub_YS_task(stn_data, planning_horizon)
        elif formulation_number == 3:
            model_milp, formulation_name = create_model_f4_ub_YS_unit(stn_data, planning_horizon)
        elif formulation_number == 4:
            model_milp, formulation_name = create_model_f5_ub_X_task(stn_data, planning_horizon)
        elif formulation_number == 5:
            model_milp, formulation_name = create_model_f6_ub_X_unit(stn_data, planning_horizon)
        elif formulation_number == 6:
            model_milp, formulation_name = create_model_f7_ub_X_group_k(stn_data, planning_horizon)
        elif formulation_number == 7:
            model_milp, formulation_name = create_model_f8_ub_YS_group_k(stn_data, planning_horizon)
        elif formulation_number == 8:
            model_milp, formulation_name = create_model_f9_ub_YS_task_unit(stn_data, planning_horizon)
        elif formulation_number == 9:
            model_milp, formulation_name = create_model_f10_ub_X_task_unit(stn_data, planning_horizon)
        elif formulation_number == 10:
            model_milp, formulation_name = create_model_f11_ub_X_YS_group_k(stn_data, planning_horizon)
        elif formulation_number == 11:
            model_milp, formulation_name = create_model_f12_all(stn_data, planning_horizon)
        elif formulation_number == 12:
            model_milp, formulation_name = create_model_f0_test(stn_data, planning_horizon)        
        else:
            raise Exception(f"Fomrulation number {formulation_number} is not recognized.")
        
        results_milp, stats_milp, results_lp = solve_and_analyze_model(solver, model_milp, planning_horizon, mip_gap_multiplier)
        
        # Step 4: Create result dictionary
        result = create_dict_result(result, stats_milp, results_milp, results_lp, formulation_name, mip_gap_multiplier)
        
        logging.info(
            f"Models were solved. Formulation: {formulation_name}. MILP Objective: {round(results_milp.problem.lower_bound, 2)}." 
        )                       
            
    except Exception as e:
        
        logging.error(
            f"Error while solving instance {network}, startup_cost_factor = {startup_cost_factor}, horizon = {planning_horizon}, tau_factor = {tau_factor}, beta_factor = {beta_factor}, formulation = {formulation_name}, mip_gap_multiplier = {mip_gap_multiplier}"
        )
        logging.exception(e)
        
    return result


def main(taskID: int) -> None:
    """ 
    Main function to run multiple instances of the optimization problem.
    """
    
    with open(f"input_data/datasets/run_{taskID:05}.json", "r") as f:
        dct = json.load(f)    
    
    formulation_number, network, startup_cost_factor, planning_horizon, tau_factor, beta_factor, mip_gap_multiplier = dct["formulation"], dct["network"], dct["startup_cost_factor"], dct["planning_horizon"], dct["tau_factor"], dct["beta_factor"], dct["mip_gap"]
    
    result = run_instance(network, startup_cost_factor, planning_horizon, tau_factor, beta_factor, formulation_number, taskID, mip_gap_multiplier)
    
    with open(f"src/results/result_{taskID:05}.json", "w") as f:
        json.dump(result, f)
                                
    
if __name__=="__main__":
    
    main(taskID)      