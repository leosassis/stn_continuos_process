from input_data.networks import (define_stn_network_1,
                                 define_stn_network_2,
                                 define_stn_network_3,
                                 define_stn_network_4, 
                                 define_stn_network_5,
                                 define_stn_network_6,
                                 define_stn_network_tasks_competing, 
                                 define_stn_network_upper_bound_YS, 
                                 define_stn_network_upper_bound_X, 
                                 define_stn_network_indirect_transitions, 
                                 define_stn_network_all_transitions)


def load_network(network_name: str, tau_factor: int, beta_factor: int, startup_cost_factor: int, planning_horizon: int) -> dict:
    """ 
    Loads and returns a dictionary of network data.
    
    Args:
        - network_name (str): identifier of the network.
        - tau_factor (int): multiplyer factor for tau parameters.
        - beta_factor (int): multiplyer factor for beta parameters.
        - startup_cost_factor (int): multiplyer factor for startup cost parameters.
        - planning horizon (int): lenght of the planning horizon.
            
    Returns: 
        dict: a dictionary containing the network data. 
    """
    
    # Create network_1 where tasks/units have the same tau/beta in a stage
    if network_name == "network_1":
        return define_stn_network_1(tau_factor, beta_factor, startup_cost_factor, planning_horizon)
    
    # Create network_2 where tasks/units are different at each stage and tasks TB1 and TB3 have to wait for materials to accumulate before they can start
    elif network_name == "network_2":
        return define_stn_network_2(tau_factor, beta_factor, startup_cost_factor, planning_horizon)
    
    # Create network_3 where tasks/units are different at each stage, tasks TB1 and TB3 have to wait for materials to accumulate, TC% and TC^ are used to test bounds for X
    elif network_name == "network_3":
        return define_stn_network_3(tau_factor, beta_factor, startup_cost_factor, planning_horizon)
    
    # Create network_4 where tasks/units are different at each stage, tasks TB1 and TB3 have to wait for materials to accumulate, TC5 and TC6 are used to test bounds for X and there is one more stage
    elif network_name == "network_4":
        return define_stn_network_4(tau_factor, beta_factor, startup_cost_factor, planning_horizon)
    
    # Create network_5. Same as network_3 plus transitions in some of the tasks. 
    elif network_name == "network_5":
        return define_stn_network_5(tau_factor, beta_factor, startup_cost_factor, planning_horizon)
    
    # Create network_6 where each stage has 1 unit with 3 tasks each. 
    elif network_name == "network_6":
        return define_stn_network_6(tau_factor, beta_factor, startup_cost_factor, planning_horizon)
    
    elif network_name == "network_competing_tasks":
        return define_stn_network_tasks_competing(tau_factor, beta_factor, startup_cost_factor, planning_horizon)
    
    elif network_name == "network_upper_bound_YS":
        return define_stn_network_upper_bound_YS(tau_factor, beta_factor, startup_cost_factor, planning_horizon)
    
    elif network_name == "network_upper_bound_X":
        return define_stn_network_upper_bound_X(tau_factor, beta_factor, startup_cost_factor, planning_horizon)
    
    elif network_name == "network_indirect_transitions":
        return define_stn_network_indirect_transitions(tau_factor, beta_factor, startup_cost_factor, planning_horizon)
    
    elif network_name == "network_all_transitions":
        return define_stn_network_all_transitions(tau_factor, beta_factor, startup_cost_factor, planning_horizon)
    
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
    
    NETWORKS = ["network_4"]
    PLANNING_HORIZONS = [45, 50]
    TAU_FACTORS = [1.2, 1.4, 1.6]
    BETA_FACTORS = [0.5, 0.6, 0.7]
    FORMULATIONS = 12
    DEMAND_FACTORS = [0, 5]
    MIP_GAPS = [1, 5, 10]
    
        
    return FORMULATIONS, NETWORKS, PLANNING_HORIZONS, TAU_FACTORS, BETA_FACTORS, DEMAND_FACTORS, MIP_GAPS 
