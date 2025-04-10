
def instace_factors_network():
    NETWORKS = ["network_2"]
    CASES = ["slow_upstream", "fast_upstream", "uniform"]
    PLANNING_HORIZON_ARRAY = [25, 35, 50]
    TAU_FACTOR_MAX = 3
    BETA_FACTOR_MAX = 4

    return NETWORKS, CASES, PLANNING_HORIZON_ARRAY, TAU_FACTOR_MAX, BETA_FACTOR_MAX 
