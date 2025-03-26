#from input_data.network_2 import define_stn_network
#from input_data.network_7_slow_upstream_fast_downstream import define_stn_network
from input_data.network_8_fast_upstream_slow_downstream import define_stn_network

def load_data() -> dict:
    
    return define_stn_network()