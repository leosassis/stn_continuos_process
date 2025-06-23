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
            "network": "",
            "case": "",
            "planning_horizon": 0,
            "tau_factor": 0,
            "beta_factor": 0
            }


# Step 1: Load varying parameters to create instances
networks, cases, planning_horizons, tau_factor_max, beta_factor_max = instance_factors_network()


# Step 2: Create a json file containing a dictionary with parameters for each instance
for i, (net, case, horizon, tau, beta) in enumerate(product(networks, cases, planning_horizons, range(1, tau_factor_max), range(1, beta_factor_max)), start=1):
    
    params = init_based_parameters().copy()
    
    params.update({
        "network": net,
        "case": case,
        "planning_horizon": horizon,
        "tau_factor": tau,
        "beta_factor": beta,
    })
    
    with open(f'{DATA_FOLDER}/run_{i:03}.json', 'w') as f:
        json.dump(params, f, indent=2)