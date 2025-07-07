from numpy import floor, ceil


def define_stn_network_1(tau_factor: int, beta_factor: int, demand_factor: int, planning_horizon: int) -> dict:
    """
    Create network_1 where tasks/units have the same tau/beta in a stage.
    
    Args:
        - case (str): defines which case to use for task/unit parameters (i.e., "fast_upstream", "slow_upstream", "uniform").
        - tau_factor (int): factor used to scale tau parameters.
        - beta_factor (int): factor used to scale beta parameters.

    Returns:
        dict: a dictionary defining the structure of the scheduling problem, including:
              STATES, STATE-to-TASK arcs, TASK-to-STATE arcs, UNIT-TASK assignments, etc.
    """
    
    stn = {
        
        # Define all states (raw materials, intermediates, and products)
        'STATES': {
            'RM'     : {'capacity': 10000, 'initial': 10000, 'price': 0, 'isRM': True, 'isIntermed': False, 'isProd': False, 'order': 1,},            
            'IA1'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 2,},       
            'IA2'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 3,},       
            'IB1'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 5,},       
            'IB2'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 6,},       
            'IB3'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 7,},                   
            'IB4'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 8,},                   
            'P1'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 9,},       
            'P2'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 10,},       
            'P3'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 11,},              
            'P4'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 12,},       
            'P5'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 13,},       
            'P6'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 14,},                      
        },
        
        # Placeholder for shipment demands
        'STATES_SHIPMENT': { 
            ('P1', planning_horizon) : {'demand':10 * demand_factor},
            #('P2', planning_horizon) : {'demand':10 * demand_factor},
            #('P3', planning_horizon) : {'demand':10 * demand_factor},
            #('P4', planning_horizon) : {'demand':10 * demand_factor},
            #('P5', planning_horizon) : {'demand':10 * demand_factor},
            #('P6', planning_horizon) : {'demand':10 * demand_factor},      
        },
        
        # Define input arcs: which states feed which tasks (negative flow)
        'ST_ARCS': {
            ('RM', 'TA1')   : {'rho': -1.0, 'direction': -1},          
            ('RM', 'TA2')   : {'rho': -1.0, 'direction': -1},           
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
            ('TC1', 'P1')   : {'rho': 1.0, 'direction': 1},            
            ('TC2', 'P2')   : {'rho': 1.0, 'direction': 1},            
            ('TC3', 'P3')   : {'rho': 1.0, 'direction': 1},            
            ('TC4', 'P4')   : {'rho': 1.0, 'direction': 1},            
            ('TC5', 'P5')   : {'rho': 1.0, 'direction': 1},            
            ('TC6', 'P6')   : {'rho': 1.0, 'direction': 1},
        },
        
        # Optional mapping of startup/shutdown transitions between tasks
        'TASKS_TRANSITION_TASKS': { 
            # Example: ('TC3', 'ITC3')   : {'isSU': True, 'isSD': False, 'isDirect': False, 'direction': 1},
            
        },
        
        'UNIT_TASKS' : {
            ('UA1', 'TA1'): {'tau_min': 4, 'tau_max': 6, 'tau': 1, 'Bmin': 25, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA2', 'TA2'): {'tau_min': 4, 'tau_max': 6, 'tau': 1, 'Bmin': 25, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA3', 'TB1'): {'tau_min': 5, 'tau_max': 7, 'tau': 1, 'Bmin': 15, 'Bmax': 20, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA4', 'TB2'): {'tau_min': 5, 'tau_max': 7, 'tau': 1, 'Bmin': 15, 'Bmax': 20, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TB3'): {'tau_min': 5, 'tau_max': 7, 'tau': 1, 'Bmin': 15, 'Bmax': 20, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TB4'): {'tau_min': 5, 'tau_max': 7, 'tau': 1, 'Bmin': 15, 'Bmax': 20, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA6', 'TC1'): {'tau_min': int(ceil(5 / tau_factor)), 'tau_max': int(ceil(7 * tau_factor)), 'tau': 1, 'Bmin': 5 * beta_factor, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA6', 'TC2'): {'tau_min': int(ceil(5 / tau_factor)), 'tau_max': int(ceil(7 * tau_factor)), 'tau': 1, 'Bmin': 5 * beta_factor, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA7', 'TC3'): {'tau_min': int(ceil(5 / tau_factor)), 'tau_max': int(ceil(7 * tau_factor)), 'tau': 1, 'Bmin': 5 * beta_factor, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA7', 'TC4'): {'tau_min': int(ceil(5 / tau_factor)), 'tau_max': int(ceil(7 * tau_factor)), 'tau': 1, 'Bmin': 5 * beta_factor, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA8', 'TC5'): {'tau_min': int(ceil(5 / tau_factor)), 'tau_max': int(ceil(7 * tau_factor)), 'tau': 1, 'Bmin': 5 * beta_factor, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA8', 'TC6'): {'tau_min': int(ceil(5 / tau_factor)), 'tau_max': int(ceil(7 * tau_factor)), 'tau': 1, 'Bmin': 5 * beta_factor, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
        }      
    } 
        
    return stn


def define_stn_network_2(tau_factor: int, beta_factor: int, demand_factor: int, planning_horizon: int) -> dict:
    """
    Create network_2 where tasks/units are different at each stage and tasks TB1 and TB3 have to wait for materials to accumulate before they can start.
    
    Args:
        - case (str): defines which case to use for task/unit parameters (i.e., "fast_upstream", "slow_upstream", "uniform").
        - tau_factor (int): factor used to scale tau parameters.
        - beta_factor (int): factor used to scale beta parameters.

    Returns:
        dict: a dictionary defining the structure of the scheduling problem, including:
              STATES, STATE-to-TASK arcs, TASK-to-STATE arcs, UNIT-TASK assignments, etc.
    """
    
    stn = {
        
        # Define all states (raw materials, intermediates, and products)
        'STATES': {
            'RM'     : {'capacity': 10000, 'initial': 10000, 'price': 0, 'isRM': True, 'isIntermed': False, 'isProd': False, 'order': 1,},            
            'IA1'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 2,},       
            'IA2'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 3,},       
            'IB1'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 5,},       
            'IB2'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 6,},       
            'IB3'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 7,},                   
            'IB4'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 8,},                   
            'P1'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 9,},       
            'P2'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 10,},       
            'P3'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 11,},              
            'P4'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 12,},       
            'P5'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 13,},       
            'P6'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 14,},                      
        },
        
        # Placeholder for shipment demands
        'STATES_SHIPMENT': { 
            ('P1', planning_horizon) : {'demand':10 * demand_factor},
            #('P2', planning_horizon) : {'demand':10 * demand_factor},
            #('P3', planning_horizon) : {'demand':10 * demand_factor},
            #('P4', planning_horizon) : {'demand':10 * demand_factor},
            #('P5', planning_horizon) : {'demand':10 * demand_factor},
            #('P6', planning_horizon) : {'demand':10 * demand_factor},      
        },
        
        # Define input arcs: which states feed which tasks (negative flow)
        'ST_ARCS': {
            ('RM', 'TA1')   : {'rho': -1.0, 'direction': -1},          
            ('RM', 'TA2')   : {'rho': -1.0, 'direction': -1},           
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
            ('TC1', 'P1')   : {'rho': 1.0, 'direction': 1},            
            ('TC2', 'P2')   : {'rho': 1.0, 'direction': 1},            
            ('TC3', 'P3')   : {'rho': 1.0, 'direction': 1},            
            ('TC4', 'P4')   : {'rho': 1.0, 'direction': 1},            
            ('TC5', 'P5')   : {'rho': 1.0, 'direction': 1},            
            ('TC6', 'P6')   : {'rho': 1.0, 'direction': 1},
        },
        
        # Optional mapping of startup/shutdown transitions between tasks
        'TASKS_TRANSITION_TASKS': { 
            # Example: ('TC3', 'ITC3')   : {'isSU': True, 'isSD': False, 'isDirect': False, 'direction': 1},
            
        },
        
        'UNIT_TASKS' : {
            ('UA1', 'TA1'): {'tau_min': 4, 'tau_max': 6, 'tau': 1, 'Bmin': 25, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA2', 'TA2'): {'tau_min': 4, 'tau_max': 6, 'tau': 1, 'Bmin': 25, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA3', 'TB1'): {'tau_min': 5, 'tau_max': 7, 'tau': 1, 'Bmin': 40, 'Bmax': 60, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA4', 'TB2'): {'tau_min': 5, 'tau_max': 7, 'tau': 1, 'Bmin': 15, 'Bmax': 20, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TB3'): {'tau_min': 8, 'tau_max': 10, 'tau': 1, 'Bmin': 25, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TB4'): {'tau_min': 5, 'tau_max': 7, 'tau': 1, 'Bmin': 25, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA6', 'TC1'): {'tau_min': int(ceil(5 / tau_factor)), 'tau_max': int(ceil(7 * tau_factor)), 'tau': 1, 'Bmin': 5 * beta_factor, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA6', 'TC2'): {'tau_min': int(ceil(3 / tau_factor)), 'tau_max': int(ceil(5 * tau_factor)), 'tau': 1, 'Bmin': 5 * beta_factor, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA7', 'TC3'): {'tau_min': int(ceil(5 / tau_factor)), 'tau_max': int(ceil(7 * tau_factor)), 'tau': 1, 'Bmin': 5 * beta_factor, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA7', 'TC4'): {'tau_min': int(ceil(3 / tau_factor)), 'tau_max': int(ceil(5 * tau_factor)), 'tau': 1, 'Bmin': 5 * beta_factor, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA8', 'TC5'): {'tau_min': int(ceil(5 / tau_factor)), 'tau_max': int(ceil(7 * tau_factor)), 'tau': 1, 'Bmin': 5 * beta_factor, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA8', 'TC6'): {'tau_min': int(ceil(3 / tau_factor)), 'tau_max': int(ceil(5 * tau_factor)), 'tau': 1, 'Bmin': 5 * beta_factor, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
        }      
    } 
        
    return stn


def define_stn_network_3(tau_factor: int, beta_factor: int, demand_factor: int, planning_horizon: int) -> dict:
    """
    Create network_3 where tasks/units are different at each stage, tasks TB1 and TB3 have to wait for materials to accumulate, TC5 and TC6 are used to test bounds for X.
    
    Args:
        - case (str): defines which case to use for task/unit parameters (i.e., "fast_upstream", "slow_upstream", "uniform").
        - tau_factor (int): factor used to scale tau parameters.
        - beta_factor (int): factor used to scale beta parameters.

    Returns:
        dict: a dictionary defining the structure of the scheduling problem, including:
              STATES, STATE-to-TASK arcs, TASK-to-STATE arcs, UNIT-TASK assignments, etc.
    """
    
    stn = {
        
        # Define all states (raw materials, intermediates, and products)
        'STATES': {
            'RM'     : {'capacity': 10000, 'initial': 10000, 'price': 0, 'isRM': True, 'isIntermed': False, 'isProd': False, 'order': 1,},            
            'IA1'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 2,},       
            'IA2'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 3,},       
            'IB1'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 5,},       
            'IB2'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 6,},       
            'IB3'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 7,},                   
            'IB4'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 8,},                   
            'P1'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 9,},       
            'P2'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 10,},       
            'P3'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 11,},              
            'P4'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 12,},       
            'P5'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 13,},       
            'P6'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 14,},                      
        },
        
        # Placeholder for shipment demands
        'STATES_SHIPMENT': { 
            ('P1', planning_horizon) : {'demand':10 * demand_factor},
            ('P2', planning_horizon) : {'demand':10 * demand_factor},
            ('P3', planning_horizon) : {'demand':10 * demand_factor},
            ('P4', planning_horizon) : {'demand':10 * demand_factor},
            ('P5', planning_horizon) : {'demand':10 * demand_factor},
            ('P6', planning_horizon) : {'demand':10 * demand_factor},      
        },
        
        # Define input arcs: which states feed which tasks (negative flow)
        'ST_ARCS': {
            ('RM', 'TA1')   : {'rho': -1.0, 'direction': -1},          
            ('RM', 'TA2')   : {'rho': -1.0, 'direction': -1},           
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
            ('TC1', 'P1')   : {'rho': 1.0, 'direction': 1},            
            ('TC2', 'P2')   : {'rho': 1.0, 'direction': 1},            
            ('TC3', 'P3')   : {'rho': 1.0, 'direction': 1},            
            ('TC4', 'P4')   : {'rho': 1.0, 'direction': 1},            
            ('TC5', 'P5')   : {'rho': 1.0, 'direction': 1},            
            ('TC6', 'P6')   : {'rho': 1.0, 'direction': 1},
        },
        
        # Optional mapping of startup/shutdown transitions between tasks
        'TASKS_TRANSITION_TASKS': { 
            # Example: ('TC3', 'ITC3')   : {'isSU': True, 'isSD': False, 'isDirect': False, 'direction': 1},
            
        },
        
        'UNIT_TASKS' : {
            ('UA1', 'TA1'): {'tau_min': 4, 'tau_max': 6, 'tau': 1, 'Bmin': 25, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA2', 'TA2'): {'tau_min': 5, 'tau_max': 7, 'tau': 1, 'Bmin': 45, 'Bmax': 55, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA3', 'TB1'): {'tau_min': 5, 'tau_max': 7, 'tau': 1, 'Bmin': 40, 'Bmax': 60, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA4', 'TB2'): {'tau_min': 5, 'tau_max': 7, 'tau': 1, 'Bmin': 15, 'Bmax': 20, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TB3'): {'tau_min': 8, 'tau_max': 10, 'tau': 1, 'Bmin': 60, 'Bmax': 65, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TB4'): {'tau_min': 5, 'tau_max': 7, 'tau': 1, 'Bmin': 30, 'Bmax': 35, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA6', 'TC1'): {'tau_min': int(ceil(7 / tau_factor)), 'tau_max': 7, 'tau': 1, 'Bmin': 5, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA6', 'TC2'): {'tau_min': int(ceil(5 / tau_factor)), 'tau_max': 5, 'tau': 1, 'Bmin': 5, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA7', 'TC3'): {'tau_min': int(ceil(7 / tau_factor)), 'tau_max': 7, 'tau': 1, 'Bmin': 5, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA7', 'TC4'): {'tau_min': int(ceil(5 / tau_factor)), 'tau_max': 5, 'tau': 1, 'Bmin': 5, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA8', 'TC5'): {'tau_min': 13, 'tau_max': 15, 'tau': 1, 'Bmin': 5, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA9', 'TC6'): {'tau_min': 13, 'tau_max': 15, 'tau': 1, 'Bmin': 5, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
        }      
    } 
        
    return stn


def define_stn_network_4(tau_factor: int, beta_factor: int, demand_factor: int, planning_horizon: int) -> dict:
    """
    Create network_4 where tasks/units are different at each stage, tasks TB1 and TB3 have to wait for materials to accumulate, TC% and TC^ are used to test bounds for X.
    
    Args:
        - case (str): defines which case to use for task/unit parameters (i.e., "fast_upstream", "slow_upstream", "uniform").
        - tau_factor (int): factor used to scale tau parameters.
        - beta_factor (int): factor used to scale beta parameters.

    Returns:
        dict: a dictionary defining the structure of the scheduling problem, including:
              STATES, STATE-to-TASK arcs, TASK-to-STATE arcs, UNIT-TASK assignments, etc.
    """
    
    stn = {
        
        # Define all states (raw materials, intermediates, and products)
        'STATES': {
            'RM'     : {'capacity': 10000, 'initial': 10000, 'price': 0, 'isRM': True, 'isIntermed': False, 'isProd': False, 'order': 1,},            
            'IA1'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 2,},       
            'IA2'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 3,},       
            'IB1'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 5,},       
            'IB2'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 6,},       
            'IB3'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 7,},                   
            'IB4'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 8,},                   
            'P1'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 9,},       
            'P2'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 10,},       
            'P3'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 11,},              
            'P4'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 12,},       
            'P5'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 13,},       
            'P6'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 14,},       
            'P7'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 15,},       
            'P8'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 16,},       
        },
        
        # Placeholder for shipment demands
        'STATES_SHIPMENT': { 
            ('P1', planning_horizon) : {'demand':10 * demand_factor},
            #('P2', planning_horizon) : {'demand':10 * demand_factor},
            #('P3', planning_horizon) : {'demand':10 * demand_factor},
            #('P4', planning_horizon) : {'demand':10 * demand_factor},
            #('P5', planning_horizon) : {'demand':10 * demand_factor},
            #('P6', planning_horizon) : {'demand':10 * demand_factor},       
            #('P7', planning_horizon) : {'demand':10 * demand_factor},       
            #('P8', planning_horizon) : {'demand':10 * demand_factor},       
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
            ('IB4', 'TC7')  : {'rho': -1.0, 'direction': -1},
            ('IB4', 'ITC7') : {'rho': -1.0, 'direction': -1},
            ('IB4', 'TC7I') : {'rho': -1.0, 'direction': -1},
            ('IB4', 'TC8')  : {'rho': -1.0, 'direction': -1},
            ('IB4', 'ITC8') : {'rho': -1.0, 'direction': -1},
            ('IB4', 'TC8I') : {'rho': -1.0, 'direction': -1},
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
            ('TC7', 'P7')  : {'rho': 1.0, 'direction': 1},
            ('ITC7', 'P7') : {'rho': 1.0, 'direction': 1},
            ('TC7I', 'P7') : {'rho': 1.0, 'direction': 1}, 
            ('TC8', 'P8')  : {'rho': 1.0, 'direction': 1},
            ('ITC8', 'P8') : {'rho': 1.0, 'direction': 1},
            ('TC8I', 'P8') : {'rho': 1.0, 'direction': 1}, 
        },
        
        # Optional mapping of startup/shutdown transitions between tasks
        'TASKS_TRANSITION_TASKS': { 
            # Example: ('TC3', 'ITC3')   : {'isSU': True, 'isSD': False, 'isDirect': False, 'direction': 1},
            ('TC7', 'ITC7')   : {'isSU': True, 'isSD': False, 'isDirect': False, 'direction': 1},
            ('TC7', 'TC7I')   : {'isSU': False, 'isSD': True, 'isDirect': False, 'direction': -1},
            ('TC8', 'ITC8')   : {'isSU': True, 'isSD': False, 'isDirect': False, 'direction': 1},
            ('TC8', 'TC8I')   : {'isSU': False, 'isSD': True, 'isDirect': False, 'direction': -1},
        },
        
        'UNIT_TASKS' : {
            ('UA1', 'TA1'): {'tau_min': 4, 'tau_max': 6, 'tau': 1, 'Bmin': 50, 'Bmax': 60, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA2', 'TA2'): {'tau_min': 8, 'tau_max': 10, 'tau': 1, 'Bmin': 30, 'Bmax': 45, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA3', 'TB1'): {'tau_min': 4, 'tau_max': 6, 'tau': 1, 'Bmin': 20, 'Bmax': 25, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA3', 'TB2'): {'tau_min': 7, 'tau_max': 9, 'tau': 1, 'Bmin': 15, 'Bmax': 20, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA4', 'TB3'): {'tau_min': 5, 'tau_max': 7, 'tau': 1, 'Bmin': 15, 'Bmax': 20, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA4', 'TB4'): {'tau_min': 4, 'tau_max': 8, 'tau': 1, 'Bmin': 20, 'Bmax': 25, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TC1'): {'tau_min': int(ceil(4 / tau_factor)), 'tau_max': int(ceil(5 * tau_factor)), 'tau': 1, 'Bmin': 5 * beta_factor, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TC2'): {'tau_min': int(ceil(4 / tau_factor)), 'tau_max': int(ceil(5 * tau_factor)), 'tau': 1, 'Bmin': 5 * beta_factor, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA6', 'TC3'): {'tau_min': int(ceil(5 / tau_factor)), 'tau_max': int(ceil(7 * tau_factor)), 'tau': 1, 'Bmin': 5 * beta_factor, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA7', 'TC4'): {'tau_min': int(ceil(5 / tau_factor)), 'tau_max': int(ceil(7 * tau_factor)), 'tau': 1, 'Bmin': 5 * beta_factor, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA8', 'TC5'): {'tau_min': int(ceil(4 / tau_factor)), 'tau_max': int(ceil(5 * tau_factor)), 'tau': 1, 'Bmin': 30, 'Bmax': 40, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA8', 'TC6'): {'tau_min': int(ceil(4 / tau_factor)), 'tau_max': int(ceil(5 * tau_factor)), 'tau': 1, 'Bmin': 5, 'Bmax': 6, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UC9', 'TC7')  : {'tau_min': 3, 'tau_max': 5, 'tau': 1, 'Bmin': 4, 'Bmax': 5, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UC9', 'ITC7') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 6, 'Bmax': 8, 'Cost': 4, 'vCost': 1, 'sCost': 0, 'direction': 1,},
            ('UC9', 'TC7I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 6, 'Bmax': 8, 'Cost': 4, 'vCost': 1, 'sCost': 0, 'direction': -1,},
            ('UC9', 'TC8')  : {'tau_min': 3, 'tau_max': 5, 'tau': 1, 'Bmin': 4, 'Bmax': 5, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UC9', 'ITC8') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 6, 'Bmax': 8, 'Cost': 4, 'vCost': 1, 'sCost': 0, 'direction': 1,},
            ('UC9', 'TC8I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 6, 'Bmax': 8, 'Cost': 4, 'vCost': 1, 'sCost': 0, 'direction': -1,},
        }
    }
    
    return stn


def define_stn_network_5(tau_factor: int, beta_factor: int, demand_factor: int, planning_horizon: int) -> dict:
    """
    Same as network_3 plus transitions in some of the tasks. 
    network_3 = where tasks/units are different at each stage, tasks TB1 and TB3 have to wait for materials to accumulate, TC5 and TC6 are used to test bounds for X.
    
    Args:
        - case (str): defines which case to use for task/unit parameters (i.e., "fast_upstream", "slow_upstream", "uniform").
        - tau_factor (int): factor used to scale tau parameters.
        - beta_factor (int): factor used to scale beta parameters.

    Returns:
        dict: a dictionary defining the structure of the scheduling problem, including:
              STATES, STATE-to-TASK arcs, TASK-to-STATE arcs, UNIT-TASK assignments, etc.
    """
    
    stn = {
        
        # Define all states (raw materials, intermediates, and products)
        'STATES': {
            'RM'     : {'capacity': 10000, 'initial': 10000, 'price': 0, 'isRM': True, 'isIntermed': False, 'isProd': False, 'order': 1,},            
            'IA1'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 2,},       
            'IA2'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 3,},       
            'IB1'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 5,},       
            'IB2'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 6,},       
            'IB3'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 7,},                   
            'IB4'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 8,},                   
            'P1'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 9,},       
            'P2'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 10,},       
            'P3'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 11,},              
            'P4'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 12,},       
            'P5'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 13,},       
            'P6'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 14,},                      
        },
        
        # Placeholder for shipment demands
        'STATES_SHIPMENT': { 
            ('P1', planning_horizon) : {'demand':10 * demand_factor},
            ('P2', planning_horizon) : {'demand':10 * demand_factor},
            ('P3', planning_horizon) : {'demand':10 * demand_factor},
            ('P4', planning_horizon) : {'demand':10 * demand_factor},
            ('P5', planning_horizon) : {'demand':10 * demand_factor},
            ('P6', planning_horizon) : {'demand':10 * demand_factor},      
        },
        
        # Define input arcs: which states feed which tasks (negative flow)
        'ST_ARCS': {
            ('RM', 'TA1')   : {'rho': -1.0, 'direction': -1},          
            ('RM', 'TA2')   : {'rho': -1.0, 'direction': -1},           
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
            ('TC1', 'P1')   : {'rho': 1.0, 'direction': 1},            
            ('TC2', 'P2')   : {'rho': 1.0, 'direction': 1},            
            ('TC3', 'P3')   : {'rho': 1.0, 'direction': 1},            
            ('TC4', 'P4')   : {'rho': 1.0, 'direction': 1},            
            ('TC5', 'P5')   : {'rho': 1.0, 'direction': 1},            
            ('TC6', 'P6')   : {'rho': 1.0, 'direction': 1},
        },
        
        # Optional mapping of startup/shutdown transitions between tasks
        'TASKS_TRANSITION_TASKS': { 
            # Example: ('TC3', 'ITC3')   : {'isSU': True, 'isSD': False, 'isDirect': False, 'direction': 1},
            
        },
        
        'UNIT_TASKS' : {
            ('UA1', 'TA1'): {'tau_min': 4, 'tau_max': 6, 'tau': 1, 'Bmin': 25, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA2', 'TA2'): {'tau_min': 5, 'tau_max': 7, 'tau': 1, 'Bmin': 45, 'Bmax': 55, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA3', 'TB1'): {'tau_min': 5, 'tau_max': 7, 'tau': 1, 'Bmin': 40, 'Bmax': 60, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA4', 'TB2'): {'tau_min': 5, 'tau_max': 7, 'tau': 1, 'Bmin': 15, 'Bmax': 20, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TB3'): {'tau_min': 8, 'tau_max': 10, 'tau': 1, 'Bmin': 60, 'Bmax': 65, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TB4'): {'tau_min': 5, 'tau_max': 7, 'tau': 1, 'Bmin': 30, 'Bmax': 35, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA6', 'TC1'): {'tau_min': int(ceil(7 / tau_factor)), 'tau_max': 7, 'tau': 1, 'Bmin': 5, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA6', 'TC2'): {'tau_min': int(ceil(5 / tau_factor)), 'tau_max': 5, 'tau': 1, 'Bmin': 5, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA7', 'TC3'): {'tau_min': int(ceil(7 / tau_factor)), 'tau_max': 7, 'tau': 1, 'Bmin': 5, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA7', 'TC4'): {'tau_min': int(ceil(5 / tau_factor)), 'tau_max': 5, 'tau': 1, 'Bmin': 5, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA8', 'TC5'): {'tau_min': 13, 'tau_max': 15, 'tau': 1, 'Bmin': 5, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA9', 'TC6'): {'tau_min': 13, 'tau_max': 15, 'tau': 1, 'Bmin': 5, 'Bmax': 6 * beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
        }      
    } 
        
    return stn


def define_stn_network_6(tau_factor: int, beta_factor: int, demand_factor: int, planning_horizon: int) -> dict:
    """
    Create network_6 where each stage has 1 unit with 3 tasks each. 
        
    Args:
        - case (str): defines which case to use for task/unit parameters (i.e., "fast_upstream", "slow_upstream", "uniform").
        - tau_factor (int): factor used to scale tau parameters.
        - beta_factor (int): factor used to scale beta parameters.

    Returns:
        dict: a dictionary defining the structure of the scheduling problem, including:
              STATES, STATE-to-TASK arcs, TASK-to-STATE arcs, UNIT-TASK assignments, etc.
    """
    
    stn = {
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
            ('P1', planning_horizon) : {'demand':10 * demand_factor},        
            #('P2', planning_horizon) : {'demand':10 * beta_factor},
            #('P3', planning_horizon) : {'demand':10 * beta_factor},
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
            # Example: ('TC3', 'ITC3')   : {'isSU': True, 'isSD': False, 'isDirect': False, 'direction': 1}, 
        
        },
        
        'UNIT_TASKS' : {
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
    }
    
    return stn

################################################################################################################################################################################################
# TEST NETWORKS                                                                                                                                                                                # 
################################################################################################################################################################################################

def define_stn_network_tasks_competing(tau_factor: int, beta_factor: int, demand_factor: int, planning_horizon: int) -> dict:
    
    stn = {
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
        ('U0', 'T0') : {'tau_min': 4, 'tau_max': 25, 'tau': 1, 'Bmin': 45, 'Bmax': 50, 'Cost': 4, 'vCost': 1, 'sCost': 30, 'direction': 1,},
        ('U1', 'T1') : {'tau_min': 6, 'tau_max': 6, 'tau': 1, 'Bmin': 30, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 30, 'direction': 1,},              
        ('U2', 'T2') : {'tau_min': 6, 'tau_max': 6, 'tau': 1, 'Bmin': 30, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 30, 'direction': 1,},       
    },
}
    
    return stn


def define_stn_network_upper_bound_YS(tau_factor: int, beta_factor: int, demand_factor: int, planning_horizon: int) -> dict:
    
    stn = {
    # states
    'STATES': {
        'RM'     : {'capacity': 10000, 'initial': 10000, 'price':  0, 'isRM': True, 'isIntermed': False, 'isProd': False, 'order': 1,},
        'I1'     : {'capacity': 10000, 'initial': 0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 2,},                
        'P1'     : {'capacity': 10000, 'initial': 0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 3,},       
        'P2'     : {'capacity': 10000, 'initial': 0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 4,},       
    },

    'STATES_SHIPMENT': {
        #('P1', 15) : {'demand':160},        
        #('P2', 15) : {'demand':75},        
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
    
    return stn


def define_stn_network_upper_bound_X(tau_factor: int, beta_factor: int, demand_factor: int, planning_horizon: int) -> dict:
    
    stn = {
    # states
    'STATES': {
        'RM'     : {'capacity': 10000, 'initial': 10000, 'price':  0, 'isRM': True, 'isIntermed': False, 'isProd': False, 'order': 1,},
        'I1'     : {'capacity': 10000, 'initial': 0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 2,},                
        'P1'     : {'capacity': 10000, 'initial': 0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 3,},       
        'P2'     : {'capacity': 10000, 'initial': 0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 4,},       
    },

    'STATES_SHIPMENT': {
        #('P1', 12) : {'demand':160},        
        #('P2', 12) : {'demand':75},        
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
        ('U0', 'T0') : {'tau_min': 3, 'tau_max': 6, 'tau': 1, 'Bmin': 25, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 30, 'direction': 1,},
        ('U1', 'T1') : {'tau_min': 9, 'tau_max': 11, 'tau': 1, 'Bmin': 45, 'Bmax': 50, 'Cost': 4, 'vCost': 1, 'sCost': 30, 'direction': 1,},              
        ('U1', 'T2') : {'tau_min': 2, 'tau_max': 4, 'tau': 1, 'Bmin': 30, 'Bmax': 40, 'Cost': 4, 'vCost': 1, 'sCost': 30, 'direction': 1,},       
    },
}
    
    return stn


def define_stn_network_indirect_transitions(tau_factor: int, beta_factor: int, demand_factor: int, planning_horizon: int) -> dict:
    
    stn = {
    # states
    'STATES': {
        'RM'     : {'capacity': 10000, 'initial': 10000, 'price':  0, 'isRM': True, 'isIntermed': False, 'isProd': False, 'order': 1,},
        'IA1'    : {'capacity': 10000, 'initial': 0, 'price': 100, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 2,},                
        'P1'     : {'capacity': 10000, 'initial': 0, 'price': 100, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 3,},       
    },

    'STATES_SHIPMENT': {
        #('P1', 8) : {'demand':10},        
        #('P1', 10) : {'demand':25},        
    },
    
    # state-to-task arcs indexed by (state, task)
    'ST_ARCS': {
        ('RM', 'TA1') : {'rho': -1.0, 'direction': -1},
        ('RM', 'TA2') : {'rho': -1.0, 'direction': -1},
        ('IA1', 'TC1')  : {'rho': -1.0, 'direction': -1},
        ('IA1', 'ITC1') : {'rho': -1.0, 'direction': -1},
        ('IA1', 'TC1I') : {'rho': -1.0, 'direction': -1},
    },
    
    # task-to-state arcs indexed by (task, state)
    'TS_ARCS': {
        ('TA1', 'IA1')  : {'rho': 1.0, 'direction': 1},      
        ('TA2', 'IA1')  : {'rho': 1.0, 'direction': 1},      
        ('TC1', 'P1')  : {'rho': 1.0, 'direction': 1},
        ('ITC1', 'P1') : {'rho': 1.0, 'direction': 1},
        ('TC1I', 'P1') : {'rho': 1.0, 'direction': 1},        
    },
    
    # Tasks and their corresponding transition. 
    # Transition-To-Task = 1. Task-To-Transition = -1.
    # Equivalent to parameter ipits(i, ii) in the GAMS code.
    'TASKS_TRANSITION_TASKS': { 
        ('TC1', 'ITC1')   : {'isSU': True, 'isSD': False, 'isDirect': False, 'direction': 1},
        ('TC1', 'TC1I')   : {'isSU': False, 'isSD': True, 'isDirect': False, 'direction': -1},
    },
    
    # unit data indexed by (unit, task)
    'UNIT_TASKS': {
        ('UA1', 'TA1')  : {'tau_min': 4, 'tau_max': 6, 'tau': 1, 'Bmin': 6, 'Bmax': 8, 'Cost': 4, 'vCost': 1, 'sCost': 40.5, 'direction': 1,},
        ('UA2', 'TA2')  : {'tau_min': 3, 'tau_max': 5, 'tau': 1, 'Bmin': 7, 'Bmax': 9, 'Cost': 4, 'vCost': 1, 'sCost': 40.5, 'direction': 1,},              
        ('UC3', 'TC1')  : {'tau_min': 4, 'tau_max': 6, 'tau': 1, 'Bmin': 6, 'Bmax': 8, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
        ('UC3', 'ITC1') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 4, 'Bmax': 4, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},
        ('UC3', 'TC1I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 2, 'Bmax': 2, 'Cost': 3, 'vCost': 1, 'sCost': 0, 'direction': -1,},
    },
}
    
    return stn