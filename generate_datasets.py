from src.data.instance_generation import instance_factors_network, init_based_parameters
import json
import os 
from itertools import product


os.makedirs('input_data/datasets', exist_ok = True)


# Step 1: Load varying parameters to create instances
networks, cases, planning_horizons, tau_factor_max, beta_factor_max = instance_factors_network()

for i, (net, case, horizon, tau, beta) in enumerate(product(networks, cases, planning_horizons, range(1, tau_factor_max), range(1, beta_factor_max)), start=1):
    
    params = init_based_parameters().copy()
    
    params.update({
        "network": net,
        "case": case,
        "planning_horizon": horizon,
        "tau_factor": tau,
        "beta_factor": beta,
    })
    
    with open(f'input_data/datasets/run_{i:03}.json', 'w') as f:
        json.dump(params, f, indent=2)