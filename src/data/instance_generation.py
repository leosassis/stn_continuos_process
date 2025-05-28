from input_data.networks import define_stn_network_1, define_stn_network_2

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
    CASES = ["fast_upstream"]
    PLANNING_HORIZON_ARRAY = [25]
    TAU_FACTOR_MAX = 2
    BETA_FACTOR_MAX = 2
    
    return NETWORKS, CASES, PLANNING_HORIZON_ARRAY, TAU_FACTOR_MAX, BETA_FACTOR_MAX     