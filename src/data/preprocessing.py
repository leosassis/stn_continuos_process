
def instace_factors_network():
    
    NETWORKS = ["network_1", "network_2"]
    CASES = ["fast_upstream", "slow_upstream", "uniform"]
    PLANNING_HORIZON_ARRAY = [25, 35, 50]
    TAU_FACTOR_MAX = 3
    BETA_FACTOR_MAX = 3

    return NETWORKS, CASES, PLANNING_HORIZON_ARRAY, TAU_FACTOR_MAX, BETA_FACTOR_MAX 
