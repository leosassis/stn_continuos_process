from input_data.networks import define_stn_network_1, define_stn_network_2

def load_network(network, case, tau_factor, beta_factor) -> dict:
    """ 
    According to the inputs, returns a dictionary with the data for the selected network.
    """
    
    if network == "network_1":
        return define_stn_network_1(case, tau_factor, beta_factor)
    elif network == "network_2":
        return define_stn_network_2(case, tau_factor, beta_factor) 
    