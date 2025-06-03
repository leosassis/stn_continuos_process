from numpy import floor, ceil


def define_stn_network_1(case: str, tau_factor: int, beta_factor: int) -> dict:
    """
    Create a process scheduling network (STN) based on the specified case.
    
    Args:
        - case (str): defines which case to use for task/unit parameters (i.e., "fast_upstream", "slow_upstream", "uniform").
        - tau_factor (int): factor used to scale tau parameters.
        - beta_factor (int): factor used to scale beta parameters.

    Returns:
        dict: a dictionary defining the structure of the scheduling problem, including:
              STATES, STATE-to-TASK arcs, TASK-to-STATE arcs, UNIT-TASK assignments, etc.
    """
    
    # Helper function to construct a unit-task configuration dictionary
    def _task_data(tau_min, tau_max, Bmin, Bmax, direction=1, Cost=4, vCost=1, sCost=25):
        return {
            'tau_min': tau_min,
            'tau_max': tau_max,
            'tau': 1,
            'Bmin': Bmin,
            'Bmax': Bmax,
            'Cost': Cost,
            'vCost': vCost,
            'sCost': sCost,
            'direction': direction,
        }    
    
    stn = {
        
        # Define all states (raw materials, intermediates, and products)
        'STATES': {
            name: {
                'capacity': 10000,
                'initial': 10000 if name == 'RM' else 0,
                'price': 0 if name.startswith(('RM', 'I')) else 10,
                'isRM': name == 'RM',
                'isIntermed': name.startswith('I') and name != 'RM',
                'isProd': name.startswith('P'),
                'order': idx,
            }
            for idx, name in enumerate(
                ['RM', 'IA1', 'IA2', 'IB1', 'IB2', 'IB3', 'IB4', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6'],
                start=1
            )
        },

        # Placeholder for shipment demands
        'STATES_SHIPMENT': { 
            # Example: ('P4', 28) : {'demand':60},
            #('P1', 25) : {'demand':25},
            #('P2', 25) : {'demand':25},
            #('P3', 25) : {'demand':25},
            #('P4', 25) : {'demand':25},
            #('P5', 25) : {'demand':25},
            #('P6', 25) : {'demand':25},       
        },
        
        # Define input arcs: which states feed which tasks (negative flow)
        'ST_ARCS': {
            ('RM', 'TA1') : {'rho': -1.0, 'direction': -1},          
            ('RM', 'TA2') : {'rho': -1.0, 'direction': -1},           
            ('IA1', 'TB1')  : {'rho': -1.0, 'direction': -1},
            ('IA1', 'TB2')  : {'rho': -1.0, 'direction': -1},           
            ('IA2', 'TB3')  : {'rho': -1.0, 'direction': -1},        
            ('IA2', 'TB4')  : {'rho': -1.0, 'direction': -1},
            ('IB1', 'TC1')  : {'rho': -1.0, 'direction': -1},
            ('IB1', 'TC2')  : {'rho': -1.0, 'direction': -1},           
            ('IB2', 'TC3')  : {'rho': -1.0, 'direction': -1},
            ('IB3', 'TC4')  : {'rho': -1.0, 'direction': -1},            
            ('IB4', 'TC5')  : {'rho': -1.0, 'direction': -1},
            ('IB4', 'TC6')  : {'rho': -1.0, 'direction': -1},
        },
        
        # Define output arcs: which tasks generate which states (positive flow)
        'TS_ARCS': {
            ('TA1', 'IA1')  : {'rho': 1.0, 'direction': 1},            
            ('TA2', 'IA2')  : {'rho': 1.0, 'direction': 1},            
            ('TB1', 'IB1')  : {'rho': 1.0, 'direction': 1},            
            ('TB2', 'IB2')  : {'rho': 1.0, 'direction': 1},            
            ('TB3', 'IB3')  : {'rho': 1.0, 'direction': 1},            
            ('TB4', 'IB4')  : {'rho': 1.0, 'direction': 1},                       
            ('TC1', 'P1')  : {'rho': 1.0, 'direction': 1},            
            ('TC2', 'P2')  : {'rho': 1.0, 'direction': 1},            
            ('TC3', 'P3')  : {'rho': 1.0, 'direction': 1},            
            ('TC4', 'P4')  : {'rho': 1.0, 'direction': 1},            
            ('TC5', 'P5')  : {'rho': 1.0, 'direction': 1},            
            ('TC6', 'P6')  : {'rho': 1.0, 'direction': 1},
        },
        
        # Optional mapping of startup/shutdown transitions between tasks
        'TASKS_TRANSITION_TASKS': { 
            # Example: ('TC3', 'ITC3')   : {'isSU': True, 'isSD': False, 'isDirect': False, 'direction': 1},
            },      
    }
    
    # Define task-unit assignments and parameters per case
    if case == "fast_upstream":
        UNIT_TASKS = {
            ('UA1', 'TA1'): _task_data(4, 6, 25, 30),
            ('UA2', 'TA2'): _task_data(4, 6, 25, 30),
            ('UA3', 'TB1'): _task_data(5, 7, 15, 20),
            ('UA4', 'TB2'): _task_data(5, 7, 15, 20),
            ('UA5', 'TB3'): _task_data(5, 7, 15, 20),
            ('UA5', 'TB4'): _task_data(5, 7, 15, 20),
            ('UA6', 'TC1'): _task_data(int(ceil(5 / tau_factor)), int(ceil(7 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
            ('UA6', 'TC2'): _task_data(int(ceil(5 / tau_factor)), int(ceil(7 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
            ('UA7', 'TC3'): _task_data(int(ceil(5 / tau_factor)), int(ceil(7 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
            ('UA7', 'TC4'): _task_data(int(ceil(5 / tau_factor)), int(ceil(7 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
            ('UA8', 'TC5'): _task_data(int(ceil(5 / tau_factor)), int(ceil(7 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
            ('UA8', 'TC6'): _task_data(int(ceil(5 / tau_factor)), int(ceil(7 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
        }
    elif case == "fast_upstream_slow_downstream_random":
        UNIT_TASKS = {
            ('UA1', 'TA1'): _task_data(4, 6, 25, 30),
            ('UA2', 'TA2'): _task_data(4, 6, 25, 30),
            ('UA3', 'TB1'): _task_data(5, 7, 40, 60),
            ('UA4', 'TB2'): _task_data(5, 7, 15, 20),
            ('UA5', 'TB3'): _task_data(8, 10, 25, 30),
            ('UA5', 'TB4'): _task_data(5, 7, 25, 30),
            ('UA6', 'TC1'): _task_data(int(ceil(5 / tau_factor)), int(ceil(7 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
            ('UA6', 'TC2'): _task_data(int(ceil(3 / tau_factor)), int(ceil(5 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
            ('UA7', 'TC3'): _task_data(int(ceil(5 / tau_factor)), int(ceil(7 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
            ('UA7', 'TC4'): _task_data(int(ceil(3 / tau_factor)), int(ceil(5 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
            ('UA8', 'TC5'): _task_data(int(ceil(5 / tau_factor)), int(ceil(7 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
            ('UA8', 'TC6'): _task_data(int(ceil(3 / tau_factor)), int(ceil(5 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
        }
    elif case == "fast_upstream_slow_downstream_random_changes_downstream_25_demand":
        UNIT_TASKS = {
            ('UA1', 'TA1'): _task_data(4, 6, 25, 30),
            ('UA2', 'TA2'): _task_data(4, 6, 25, 30),
            ('UA3', 'TB1'): _task_data(5, 7, 40, 60),
            ('UA4', 'TB2'): _task_data(5, 7, 15, 20),
            ('UA5', 'TB3'): _task_data(8, 10, 25, 30),
            ('UA5', 'TB4'): _task_data(5, 7, 25, 30),
            ('UA6', 'TC1'): _task_data(int(ceil(5 / tau_factor)), int(ceil(7 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
            ('UA6', 'TC2'): _task_data(int(ceil(3 / tau_factor)), int(ceil(5 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
            ('UA7', 'TC3'): _task_data(int(ceil(5 / tau_factor)), int(ceil(7 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
            ('UA7', 'TC4'): _task_data(int(ceil(3 / tau_factor)), int(ceil(5 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
            ('UA8', 'TC5'): _task_data(int(ceil(5 / tau_factor)), int(ceil(7 * tau_factor)), 15 * beta_factor, 20 * beta_factor),
            ('UA8', 'TC6'): _task_data(int(ceil(5 / tau_factor)), int(ceil(7 * tau_factor)), 40 * beta_factor, 60 * beta_factor),
        }
    elif case == "fast_upstream_slow_downstream_random_changes_downstream_added_new_unit_25_demand":
        UNIT_TASKS = {
            ('UA1', 'TA1'): _task_data(4, 6, 25, 30),
            ('UA2', 'TA2'): _task_data(4, 6, 25, 30),
            ('UA3', 'TB1'): _task_data(5, 7, 40, 60),
            ('UA4', 'TB2'): _task_data(5, 7, 15, 20),
            ('UA5', 'TB3'): _task_data(8, 10, 25, 30),
            ('UA5', 'TB4'): _task_data(5, 7, 25, 30),
            ('UA6', 'TC1'): _task_data(int(ceil(5 / tau_factor)), int(ceil(7 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
            ('UA6', 'TC2'): _task_data(int(ceil(3 / tau_factor)), int(ceil(5 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
            ('UA7', 'TC3'): _task_data(int(ceil(5 / tau_factor)), int(ceil(7 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
            ('UA7', 'TC4'): _task_data(int(ceil(3 / tau_factor)), int(ceil(5 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
            ('UA8', 'TC5'): _task_data(int(ceil(5 / tau_factor)), int(ceil(7 * tau_factor)), 15 * beta_factor, 20 * beta_factor),
            ('UA9', 'TC6'): _task_data(int(ceil(5 / tau_factor)), int(ceil(7 * tau_factor)), 40 * beta_factor, 60 * beta_factor),
        }
    elif case == "fast_upstream_slow_downstream_random_upstream_flexibility":
        UNIT_TASKS = {
            ('UA1', 'TA1'): _task_data(2, 6, 5, 30),
            ('UA2', 'TA2'): _task_data(2, 6, 5, 30),
            ('UA3', 'TB1'): _task_data(2, 7, 5, 60),
            ('UA4', 'TB2'): _task_data(2, 7, 5, 20),
            ('UA5', 'TB3'): _task_data(2, 10, 5, 30),
            ('UA5', 'TB4'): _task_data(2, 7, 5, 30),
            ('UA6', 'TC1'): _task_data(int(ceil(5 / tau_factor)), int(ceil(7 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
            ('UA6', 'TC2'): _task_data(int(ceil(3 / tau_factor)), int(ceil(5 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
            ('UA7', 'TC3'): _task_data(int(ceil(5 / tau_factor)), int(ceil(7 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
            ('UA7', 'TC4'): _task_data(int(ceil(3 / tau_factor)), int(ceil(5 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
            ('UA8', 'TC5'): _task_data(int(ceil(5 / tau_factor)), int(ceil(7 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
            ('UA8', 'TC6'): _task_data(int(ceil(3 / tau_factor)), int(ceil(5 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
        } 
    elif case == "fast_upstream_slow_downstream_random_upstream_flexibility_changes_downstream_added_new_unit_25_demand":
        UNIT_TASKS = {
            ('UA1', 'TA1'): _task_data(2, 6, 5, 30),
            ('UA2', 'TA2'): _task_data(2, 6, 5, 30),
            ('UA3', 'TB1'): _task_data(2, 7, 5, 60),
            ('UA4', 'TB2'): _task_data(2, 7, 5, 20),
            ('UA5', 'TB3'): _task_data(2, 10, 5, 30),
            ('UA5', 'TB4'): _task_data(2, 7, 5, 30),
            ('UA6', 'TC1'): _task_data(int(ceil(5 / tau_factor)), int(ceil(7 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
            ('UA6', 'TC2'): _task_data(int(ceil(3 / tau_factor)), int(ceil(5 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
            ('UA7', 'TC3'): _task_data(int(ceil(5 / tau_factor)), int(ceil(7 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
            ('UA7', 'TC4'): _task_data(int(ceil(3 / tau_factor)), int(ceil(5 * tau_factor)), 5 * beta_factor, 6 * beta_factor),
            ('UA8', 'TC5'): _task_data(int(ceil(5 / tau_factor)), int(ceil(7 * tau_factor)), 15 * beta_factor, 20 * beta_factor),
            ('UA9', 'TC6'): _task_data(int(ceil(5 / tau_factor)), int(ceil(7 * tau_factor)), 40 * beta_factor, 60 * beta_factor),
        }    
    elif case == "slow_upstream":    
        UNIT_TASKS = {
            ('UA1', 'TA1'): _task_data(int(ceil(5 / tau_factor)), int(ceil(7 * tau_factor)), 5, 6 * beta_factor),
            ('UA2', 'TA2'): _task_data(int(ceil(5 / tau_factor)), int(ceil(7 * tau_factor)), 5, 6 * beta_factor),
            ('UA3', 'TB1'): _task_data(4, 6, 15, 20),
            ('UA4', 'TB2'): _task_data(4, 6, 15, 20),
            ('UA5', 'TB3'): _task_data(4, 6, 15, 20),
            ('UA5', 'TB4'): _task_data(4, 6, 15, 20),
            ('UA6', 'TC1'): _task_data(5, 6, 25, 30),
            ('UA6', 'TC2'): _task_data(5, 6, 25, 30),
            ('UA7', 'TC3'): _task_data(5, 6, 25, 30),
            ('UA7', 'TC4'): _task_data(5, 6, 25, 30),
            ('UA8', 'TC5'): _task_data(5, 6, 25, 30),
            ('UA8', 'TC6'): _task_data(5, 6, 25, 30),
        }
    elif case == "uniform":    
        UNIT_TASKS = {
            ('UA1', 'TA1') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),
            ('UA2', 'TA2') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),            
            ('UA3', 'TB1') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),
            ('UA4', 'TB2') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),
            ('UA5', 'TB3') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),
            ('UA5', 'TB4') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),          
            ('UA6', 'TC1') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),
            ('UA6', 'TC2') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),
            ('UA7', 'TC3') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),
            ('UA7', 'TC4') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),
            ('UA8', 'TC5') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),
            ('UA8', 'TC6') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),
        }
    elif case == "uniform_fast_upstream":    
        UNIT_TASKS = {
            ('UA1', 'TA1') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 70 / beta_factor, 90),
            ('UA2', 'TA2') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 70 / beta_factor, 90),            
            ('UA3', 'TB1') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),
            ('UA4', 'TB2') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),
            ('UA5', 'TB3') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),
            ('UA5', 'TB4') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),          
            ('UA6', 'TC1') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),
            ('UA6', 'TC2') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),
            ('UA7', 'TC3') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),
            ('UA7', 'TC4') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),
            ('UA8', 'TC5') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),
            ('UA8', 'TC6') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),
        }               
    elif case == "uniform_fast_downstream":    
        UNIT_TASKS = {
            ('UA1', 'TA1') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),
            ('UA2', 'TA2') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),            
            ('UA3', 'TB1') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),
            ('UA4', 'TB2') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),
            ('UA5', 'TB3') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),
            ('UA5', 'TB4') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 25 / beta_factor, 30),          
            ('UA6', 'TC1') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 60 / beta_factor, 80),
            ('UA6', 'TC2') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 60 / beta_factor, 80),
            ('UA7', 'TC3') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 60 / beta_factor, 80),
            ('UA7', 'TC4') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 60 / beta_factor, 80),
            ('UA8', 'TC5') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 60 / beta_factor, 80),
            ('UA8', 'TC6') : _task_data(int(floor(4 / tau_factor)), int(ceil(7 * tau_factor)), 60 / beta_factor, 80),
        }      
    # Assign unit-task parameters to stn    
    stn['UNIT_TASKS'] = UNIT_TASKS  
        
    return stn


def define_stn_network_2(case, tau_factor, beta_factor) -> dict:
    
    STN = {
        # states
        'STATES': {
            'RM'     : {'capacity': 10000, 'initial': 10000, 'price': 0, 'isRM': True, 'isIntermed': False, 'isProd': False, 'order': 1,},            
            'IA1'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 2,},       
            'IA2'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 3,},       
            'IA3'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 4,},                   
            'IB1'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 5,},       
            'IB2'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 6,},       
            'IB3'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 7,},                   
            'IC1'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 8,},       
            'IC2'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 9,},       
            'IC3'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 10,},                   
            'ID1'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 11,},       
            'ID2'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 12,},       
            'ID3'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 13,},                 
            'IE1'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 14,},       
            'IE2'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 15,},       
            'IE3'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 16,},              
            'P1'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 17,},       
            'P2'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 18,},       
            'P3'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 19,},       
        },

        'STATES_SHIPMENT': { 
            #('P1', 25) : {'demand':15},        
            #('P2', 25) : {'demand':15},
            #('P3', 25) : {'demand':15},
        },
        
        # state-to-task arcs indexed by (state, task)
        'ST_ARCS': {
            ('RM', 'TA1') : {'rho': -1.0, 'direction': -1},          
            ('RM', 'TA2') : {'rho': -1.0, 'direction': -1},
            ('RM', 'TA3') : {'rho': -1.0, 'direction': -1},           
            ('IA1', 'TB1')  : {'rho': -1.0, 'direction': -1},
            ('IA2', 'TB2')  : {'rho': -1.0, 'direction': -1},           
            ('IA3', 'TB3')  : {'rho': -1.0, 'direction': -1},             
            ('IB1', 'TC1')  : {'rho': -1.0, 'direction': -1},
            ('IB2', 'TC2')  : {'rho': -1.0, 'direction': -1},           
            ('IB3', 'TC3')  : {'rho': -1.0, 'direction': -1},              
            ('IC1', 'TD1')  : {'rho': -1.0, 'direction': -1},
            ('IC2', 'TD2')  : {'rho': -1.0, 'direction': -1},           
            ('IC3', 'TD3')  : {'rho': -1.0, 'direction': -1},              
            ('ID1', 'TE1')  : {'rho': -1.0, 'direction': -1},
            ('ID2', 'TE2')  : {'rho': -1.0, 'direction': -1},           
            ('ID3', 'TE3')  : {'rho': -1.0, 'direction': -1},             
            ('IE1', 'TF1')  : {'rho': -1.0, 'direction': -1},
            ('IE2', 'TF2')  : {'rho': -1.0, 'direction': -1},           
            ('IE3', 'TF3')  : {'rho': -1.0, 'direction': -1},                  
        },
        
        # task-to-state arcs indexed by (task, state)
        'TS_ARCS': {
            ('TA1', 'IA1')  : {'rho': 1.0, 'direction': 1},            
            ('TA2', 'IA2')  : {'rho': 1.0, 'direction': 1},
            ('TA3', 'IA3')  : {'rho': 1.0, 'direction': 1},            
            ('TB1', 'IB1')  : {'rho': 1.0, 'direction': 1},            
            ('TB2', 'IB2')  : {'rho': 1.0, 'direction': 1},
            ('TB3', 'IB3')  : {'rho': 1.0, 'direction': 1},            
            ('TC1', 'IC1')  : {'rho': 1.0, 'direction': 1},            
            ('TC2', 'IC2')  : {'rho': 1.0, 'direction': 1},
            ('TC3', 'IC3')  : {'rho': 1.0, 'direction': 1},            
            ('TD1', 'ID1')  : {'rho': 1.0, 'direction': 1},            
            ('TD2', 'ID2')  : {'rho': 1.0, 'direction': 1},
            ('TD3', 'ID3')  : {'rho': 1.0, 'direction': 1},            
            ('TE1', 'IE1')  : {'rho': 1.0, 'direction': 1},            
            ('TE2', 'IE2')  : {'rho': 1.0, 'direction': 1},
            ('TE3', 'IE3')  : {'rho': 1.0, 'direction': 1},            
            ('TF1', 'P1')  : {'rho': 1.0, 'direction': 1},            
            ('TF2', 'P2')  : {'rho': 1.0, 'direction': 1},
            ('TF3', 'P3')  : {'rho': 1.0, 'direction': 1},
        },
        
        # Tasks and their corresponding transition. 
        # Transition-To-Task = 1. Task-To-Transition = -1.
        # Equivalent to parameter ipits(i, ii) in the GAMS code.
        'TASKS_TRANSITION_TASKS': { 
            },                
    }
    
    # unit data indexed by (unit, task)
    if case == "fast_upstream":
        UNIT_TASKS = {
            ('UA1', 'TA1') : {'tau_min': 6, 'tau_max': 14, 'tau': 1, 'Bmin': 65, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA1', 'TA2') : {'tau_min': 6, 'tau_max': 14, 'tau': 1, 'Bmin': 65, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA1', 'TA3') : {'tau_min': 6, 'tau_max': 14, 'tau': 1, 'Bmin': 65, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},            
            ('UA2', 'TB1') : {'tau_min': 2, 'tau_max': 4, 'tau': 1, 'Bmin': 65, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA2', 'TB2') : {'tau_min': 2, 'tau_max': 4, 'tau': 1, 'Bmin': 65, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA2', 'TB3') : {'tau_min': 2, 'tau_max': 4, 'tau': 1, 'Bmin': 65, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},            
            ('UA3', 'TC1') : {'tau_min': 2, 'tau_max': 4, 'tau': 1, 'Bmin': 65, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA3', 'TC2') : {'tau_min': 2, 'tau_max': 4, 'tau': 1, 'Bmin': 65, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA3', 'TC3') : {'tau_min': 2, 'tau_max': 4, 'tau': 1, 'Bmin': 65, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},            
            ('UA4', 'TD1') : {'tau_min': 3, 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA4', 'TD2') : {'tau_min': 3, 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA4', 'TD3') : {'tau_min': 3, 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},            
            ('UA5', 'TE1') : {'tau_min': 3, 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TE2') : {'tau_min': 3, 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TE3') : {'tau_min': 3, 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},            
            ('UA6', 'TF1') : {'tau_min': 3, 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA6', 'TF2') : {'tau_min': 3, 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA6', 'TF3') : {'tau_min': 3, 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
        }    
    elif case == "fast_upstream_slow_downstream_random":
        UNIT_TASKS = {
            ('UA1', 'TA1') : {'tau_min': 6, 'tau_max': 14, 'tau': 1, 'Bmin': 65, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA1', 'TA2') : {'tau_min': 6, 'tau_max': 14, 'tau': 1, 'Bmin': 65, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA1', 'TA3') : {'tau_min': 6, 'tau_max': 14, 'tau': 1, 'Bmin': 65, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},            
            ('UA2', 'TB1') : {'tau_min': 2, 'tau_max': 4, 'tau': 1, 'Bmin': 65, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA2', 'TB2') : {'tau_min': 2, 'tau_max': 4, 'tau': 1, 'Bmin': 65, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA2', 'TB3') : {'tau_min': 2, 'tau_max': 4, 'tau': 1, 'Bmin': 65, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},            
            ('UA3', 'TC1') : {'tau_min': 2, 'tau_max': 4, 'tau': 1, 'Bmin': 65, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA3', 'TC2') : {'tau_min': 2, 'tau_max': 4, 'tau': 1, 'Bmin': 65, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA3', 'TC3') : {'tau_min': 2, 'tau_max': 4, 'tau': 1, 'Bmin': 65, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},            
            ('UA4', 'TD1') : {'tau_min': 3, 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA4', 'TD2') : {'tau_min': 3, 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA4', 'TD3') : {'tau_min': 3, 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},            
            ('UA5', 'TE1') : {'tau_min': 3, 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TE2') : {'tau_min': 3, 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TE3') : {'tau_min': 3, 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},            
            ('UA6', 'TF1') : {'tau_min': 3, 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA6', 'TF2') : {'tau_min': 3, 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA6', 'TF3') : {'tau_min': 3, 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
        }    
    elif case == "slow_upstream":
        UNIT_TASKS = {
            ('UA1', 'TA1') : {'tau_min': int(ceil(4/tau_factor)), 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA1', 'TA2') : {'tau_min': int(ceil(4/tau_factor)), 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA1', 'TA3') : {'tau_min': int(ceil(4/tau_factor)), 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},            
            ('UA2', 'TB1') : {'tau_min': int(ceil(4/tau_factor)), 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA2', 'TB2') : {'tau_min': int(ceil(4/tau_factor)), 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA2', 'TB3') : {'tau_min': int(ceil(4/tau_factor)), 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},            
            ('UA3', 'TC1') : {'tau_min': int(ceil(4/tau_factor)), 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA3', 'TC2') : {'tau_min': int(ceil(4/tau_factor)), 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA3', 'TC3') : {'tau_min': int(ceil(4/tau_factor)), 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},            
            ('UA4', 'TD1') : {'tau_min': 3, 'tau_max': 6, 'tau': 1, 'Bmin': 30, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA4', 'TD2') : {'tau_min': 3, 'tau_max': 6, 'tau': 1, 'Bmin': 30, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA4', 'TD3') : {'tau_min': 3, 'tau_max': 6, 'tau': 1, 'Bmin': 30, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},            
            ('UA5', 'TE1') : {'tau_min': 3, 'tau_max': 6, 'tau': 1, 'Bmin': 30, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TE2') : {'tau_min': 3, 'tau_max': 6, 'tau': 1, 'Bmin': 30, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TE3') : {'tau_min': 3, 'tau_max': 6, 'tau': 1, 'Bmin': 30, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},            
            ('UA6', 'TF1') : {'tau_min': 3, 'tau_max': 6, 'tau': 1, 'Bmin': 30, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA6', 'TF2') : {'tau_min': 3, 'tau_max': 6, 'tau': 1, 'Bmin': 30, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA6', 'TF3') : {'tau_min': 3, 'tau_max': 6, 'tau': 1, 'Bmin': 30, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
        }
    elif case == "uniform":
        UNIT_TASKS = {
            ('UA1', 'TA1') : {'tau_min': int(floor(6/tau_factor)), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA1', 'TA2') : {'tau_min': int(floor(6/tau_factor)), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA1', 'TA3') : {'tau_min': int(floor(6/tau_factor)), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},            
            ('UA2', 'TB1') : {'tau_min': int(floor(6/tau_factor)), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA2', 'TB2') : {'tau_min': int(floor(6/tau_factor)), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA2', 'TB3') : {'tau_min': int(floor(6/tau_factor)), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},            
            ('UA3', 'TC1') : {'tau_min': int(floor(6/tau_factor)), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA3', 'TC2') : {'tau_min': int(floor(6/tau_factor)), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA3', 'TC3') : {'tau_min': int(floor(6/tau_factor)), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},            
            ('UA4', 'TD1') : {'tau_min': int(floor(6/tau_factor)), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA4', 'TD2') : {'tau_min': int(floor(6/tau_factor)), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA4', 'TD3') : {'tau_min': int(floor(6/tau_factor)), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},            
            ('UA5', 'TE1') : {'tau_min': int(floor(6/tau_factor)), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TE2') : {'tau_min': int(floor(6/tau_factor)), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TE3') : {'tau_min': int(floor(6/tau_factor)), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},            
            ('UA6', 'TF1') : {'tau_min': int(floor(6/tau_factor)), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA6', 'TF2') : {'tau_min': int(floor(6/tau_factor)), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA6', 'TF3') : {'tau_min': int(floor(6/tau_factor)), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
        }
    elif case == "fast_upstream_slow_downstream_random_last_unit":
        UNIT_TASKS = {
            ('UA1', 'TA1') : {'tau_min': 6, 'tau_max': 14, 'tau': 1, 'Bmin': 65, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA1', 'TA2') : {'tau_min': 6, 'tau_max': 14, 'tau': 1, 'Bmin': 65, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA1', 'TA3') : {'tau_min': 6, 'tau_max': 14, 'tau': 1, 'Bmin': 65, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},            
            ('UA2', 'TB1') : {'tau_min': 2, 'tau_max': 4, 'tau': 1, 'Bmin': 65, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA2', 'TB2') : {'tau_min': 2, 'tau_max': 4, 'tau': 1, 'Bmin': 65, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA2', 'TB3') : {'tau_min': 2, 'tau_max': 4, 'tau': 1, 'Bmin': 65, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},            
            ('UA3', 'TC1') : {'tau_min': 2, 'tau_max': 4, 'tau': 1, 'Bmin': 65, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA3', 'TC2') : {'tau_min': 2, 'tau_max': 4, 'tau': 1, 'Bmin': 65, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA3', 'TC3') : {'tau_min': 2, 'tau_max': 4, 'tau': 1, 'Bmin': 65, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},            
            ('UA4', 'TD1') : {'tau_min': 3, 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA4', 'TD2') : {'tau_min': 3, 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA4', 'TD3') : {'tau_min': 3, 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},            
            ('UA5', 'TE1') : {'tau_min': 3, 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TE2') : {'tau_min': 3, 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TE3') : {'tau_min': 3, 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},            
            ('UA6', 'TF1') : {'tau_min': 3, 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA6', 'TF2') : {'tau_min': 3, 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 30, 'Bmax': 50*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA6', 'TF3') : {'tau_min': 3, 'tau_max': int(ceil(7*tau_factor)), 'tau': 1, 'Bmin': 15, 'Bmax': 25*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
        }
        
    STN['UNIT_TASKS'] = UNIT_TASKS  
            
    return STN


def define_stn_network_tasks_competing(case, tau_factor, beta_factor) -> dict:
    
    STN = {
    # states
    'STATES': {
        'RM'     : {'capacity': 10000, 'initial': 10000, 'price':  0, 'isRM': True, 'isIntermed': False, 'isProd': False, 'order': 1,},
        'I1'     : {'capacity': 10000, 'initial': 0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 2,},                
        'P1'     : {'capacity': 10000, 'initial': 0, 'price': 1000, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 3,},       
        'P2'     : {'capacity': 10000, 'initial': 0, 'price': 1000, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 4,},       
    },

    'STATES_SHIPMENT': {
        #('P1', 12) : {'demand':75},        
        #('P2', 12) : {'demand':160},        
    },
    
    # state-to-task arcs indexed by (state, task)
    'ST_ARCS': {
        ('RM', 'T0')  : {'rho': -1.0, 'direction': -1},
        ('I1', 'T1')  : {'rho': -1.0, 'direction': -1},
        ('I1', 'T2')  : {'rho': -1.0, 'direction': -1},
    },
    
    # task-to-state arcs indexed by (task, state)
    'TS_ARCS': {
        ('T0', 'I1')  : {'rho': 1.0, 'direction': 1},      
        ('T1', 'P1')  : {'rho': 1.0, 'direction': 1},      
        ('T2', 'P2')  : {'rho': 1.0, 'direction': 1},      
    },
    
    # Tasks and their corresponding transition. 
    # Transition-To-Task = 1. Task-To-Transition = -1.
    # Equivalent to parameter ipits(i, ii) in the GAMS code.
    'TASKS_TRANSITION_TASKS': {         
    },
    
    # unit data indexed by (unit, task)
    'UNIT_TASKS': {
        ('U0', 'T0') : {'tau_min': 6, 'tau_max': 6, 'tau': 1, 'Bmin': 35, 'Bmax': 35, 'Cost': 4, 'vCost': 1, 'sCost': 30, 'direction': 1,},
        ('U1', 'T1') : {'tau_min': 3, 'tau_max': 6, 'tau': 1, 'Bmin': 18, 'Bmax': 20, 'Cost': 4, 'vCost': 1, 'sCost': 30, 'direction': 1,},              
        ('U2', 'T2') : {'tau_min': 3, 'tau_max': 6, 'tau': 1, 'Bmin': 18, 'Bmax': 20, 'Cost': 4, 'vCost': 1, 'sCost': 30, 'direction': 1,},       
    },
}
    
    return STN


def define_stn_network_upper_bounds(case, tau_factor, beta_factor) -> dict:
    
    STN = {
    # states
    'STATES': {
        'RM'     : {'capacity': 10000, 'initial': 10000, 'price':  0, 'isRM': True, 'isIntermed': False, 'isProd': False, 'order': 1,},
        'I1'     : {'capacity': 10000, 'initial': 0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 2,},                
        'P1'     : {'capacity': 10000, 'initial': 0, 'price': 1000, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 3,},       
        'P2'     : {'capacity': 10000, 'initial': 0, 'price': 1000, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 4,},       
    },

    'STATES_SHIPMENT': {
        #('P1', 12) : {'demand':75},        
        #('P2', 12) : {'demand':160},        
    },
    
    # state-to-task arcs indexed by (state, task)
    'ST_ARCS': {
        ('RM', 'T0')  : {'rho': -1.0, 'direction': -1},
        ('I1', 'T1')  : {'rho': -1.0, 'direction': -1},
        ('I1', 'T2')  : {'rho': -1.0, 'direction': -1},
    },
    
    # task-to-state arcs indexed by (task, state)
    'TS_ARCS': {
        ('T0', 'I1')  : {'rho': 1.0, 'direction': 1},      
        ('T1', 'P1')  : {'rho': 1.0, 'direction': 1},      
        ('T2', 'P2')  : {'rho': 1.0, 'direction': 1},      
    },
    
    # Tasks and their corresponding transition. 
    # Transition-To-Task = 1. Task-To-Transition = -1.
    # Equivalent to parameter ipits(i, ii) in the GAMS code.
    'TASKS_TRANSITION_TASKS': {         
    },
    
    # unit data indexed by (unit, task)
    'UNIT_TASKS': {
        ('U0', 'T0') : {'tau_min': 3, 'tau_max': 5, 'tau': 1, 'Bmin': 25, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 30, 'direction': 1,},
        ('U1', 'T1') : {'tau_min': 2, 'tau_max': 3, 'tau': 1, 'Bmin': 120, 'Bmax': 130, 'Cost': 4, 'vCost': 1, 'sCost': 30, 'direction': 1,},              
        ('U1', 'T2') : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 15, 'Bmax': 20, 'Cost': 4, 'vCost': 1, 'sCost': 30, 'direction': 1,},       
    },
}
    
    return STN
