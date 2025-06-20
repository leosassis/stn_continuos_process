from input_data.networks import (define_stn_network_1, 
                                define_stn_network_2, 
                                define_stn_network_tasks_competing, 
                                define_stn_network_upper_bound_YS, 
                                define_stn_network_upper_bound_X, 
                                define_stn_network_indirect_transitions)


def load_network(network_name: str, case: str, tau_factor: int, beta_factor: int) -> dict:
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
        return define_stn_network_1(case, tau_factor, beta_factor)
    elif network_name == "network_2":
        return define_stn_network_2(case, tau_factor, beta_factor)
    elif network_name == "network_competing_tasks":
        return define_stn_network_tasks_competing(case, tau_factor, beta_factor)
    elif network_name == "network_upper_bound_YS":
        return define_stn_network_upper_bound_YS(case, tau_factor, beta_factor)
    elif network_name == "network_upper_bound_X":
        return define_stn_network_upper_bound_X(case, tau_factor, beta_factor)
    elif network_name == "network_indirect_transitions":
        return define_stn_network_indirect_transitions(case, tau_factor, beta_factor)
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
    
    #NETWORKS = ["network_1", "network_2"]
    #CASES = ["fast_upstream", "slow_upstream", "uniform"]
    #PLANNING_HORIZON_ARRAY = [25, 35, 50]
    #TAU_FACTOR_MAX = 3
    #BETA_FACTOR_MAX = 3
    
    NETWORKS = ["network_1"]
    CASES = ["fast_upstream_slow_downstream_uniform_stages", "fast_upstream_slow_downstream_nonuniform_stages", "slow_upstream_fast_downstream_uniform_stages"]
    PLANNING_HORIZON_ARRAY = [25, 35, 45]
    TAU_FACTOR_MAX = 2
    BETA_FACTOR_MAX = 2
    
        
    return NETWORKS, CASES, PLANNING_HORIZON_ARRAY, TAU_FACTOR_MAX, BETA_FACTOR_MAX 


def init_based_parameters() -> dict:
    
    return {
            "network": "",
            "case": "",
            "planning_horizon": 0,
            "tau_factor": 0,
            "beta_factor": 0
            }
