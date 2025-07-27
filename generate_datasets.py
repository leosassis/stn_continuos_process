from src.data.instance_generation import instance_factors_network
import json
import os 
from itertools import product


# Path to folder containing results
DATA_FOLDER = "input_data/datasets"

os.makedirs(DATA_FOLDER, exist_ok = True)


def init_based_parameters() -> dict:
    """ 
    Initialize an empty dictionary to store the parameters for each instance.
    
    Returns:
        dict: an empty dictionary.
    """
    
    return {
            "formulation": 0,
            "network": "",
            "startup_cost_factor": 0,
            "planning_horizon": 0,
            "tau_factor": 0,
            "beta_factor": 0,
            "mip_gap": 0
            }


# Step 1: Load varying parameters to create instances
formulations, networks, planning_horizons, tau_factors, beta_factors, startup_cost_factors, mip_gap_multipliers = instance_factors_network()


# Step 2: Create a json file containing a dictionary with parameters for each instance
for i, (formulation_num, net, horizon, tau, beta, sucost, gap) in enumerate(product(range(formulations), networks, planning_horizons, tau_factors, beta_factors, startup_cost_factors, mip_gap_multipliers), start=1):
    
    params = init_based_parameters().copy()
    
    params.update({
        "formulation": formulation_num,
        "network": net,
        "startup_cost_factor": sucost,
        "planning_horizon": horizon,
        "tau_factor": tau,
        "beta_factor": beta,
        "mip_gap": gap,
    })
    
    with open(f'{DATA_FOLDER}/run_{i:05}.json', 'w') as f:
        json.dump(params, f, indent=2)