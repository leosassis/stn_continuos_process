from input_data.networks import (define_stn_network_1,
                                 define_stn_network_1_nonuniform,
                                 define_stn_network_2, 
                                 define_stn_network_3, 
                                 define_stn_network_tasks_competing, 
                                 define_stn_network_upper_bound_YS, 
                                 define_stn_network_upper_bound_X, 
                                 define_stn_network_indirect_transitions)


def load_network(network_name: str, tau_factor: int, beta_factor: int, demand_factor: int, planning_horizon: int) -> dict:
    """ 
    Loads and returns a dictionary of network data.
    
    Args:
        - network_name (str): identifier of the network.
        - case (str): configuration of the network (e.g., 'fast_upstream').
        - tau_factor (int): multiplying factor for tau parameters.
        - beta_factor (int): multiplying factor for beta parameters.
            
    Returns: 
        dict: a dictionary containing the network data. 
    """
    
    if network_name == "network_1":
        return define_stn_network_1(tau_factor, beta_factor, demand_factor, planning_horizon)
    elif network_name == "network_1_nonuniform":
        return define_stn_network_1_nonuniform(tau_factor, beta_factor, demand_factor, planning_horizon)
    elif network_name == "network_2":
        return define_stn_network_2(tau_factor, beta_factor, demand_factor, planning_horizon)
    elif network_name == "network_3":
        return define_stn_network_3(tau_factor, beta_factor, demand_factor, planning_horizon)
    elif network_name == "network_competing_tasks":
        return define_stn_network_tasks_competing(tau_factor, beta_factor, demand_factor, planning_horizon)
    elif network_name == "network_upper_bound_YS":
        return define_stn_network_upper_bound_YS(tau_factor, beta_factor, demand_factor, planning_horizon)
    elif network_name == "network_upper_bound_X":
        return define_stn_network_upper_bound_X(tau_factor, beta_factor, demand_factor, planning_horizon)
    elif network_name == "network_indirect_transitions":
        return define_stn_network_indirect_transitions(tau_factor, beta_factor, demand_factor, planning_horizon)
    else:
        raise ValueError(f"Unsupported network name: {network_name}") 
    

def instance_factors_network() -> tuple[list[str], list[str], list[int], int, int]:
    """ 
    Defines the configuration parameters for generating instances.
    
    Returns:
        tuple:
            - list of networks (list of str).
            - list of cases (list of str).
            - list of horizons (list of int).
            - maximum tau multiplier (int).
            - maximum beta multiplier (int). 
    """
    
    NETWORKS = ["network_1_nonuniform"]
    PLANNING_HORIZON_ARRAY = [25, 30, 35, 40, 45, 50]
    TAU_FACTOR_MAX = 3
    BETA_FACTOR_MAX = 3
    FORMULATIONS = 14
    DEMAND_FACTOR_MAX = 1
    
        
    return FORMULATIONS, NETWORKS, PLANNING_HORIZON_ARRAY, TAU_FACTOR_MAX, BETA_FACTOR_MAX, DEMAND_FACTOR_MAX 
