
def instace_factors_network():
    """ 
    Defines and returns the data to create instances. 
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
