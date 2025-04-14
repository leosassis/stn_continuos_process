from numpy import floor, ceil

def define_stn_network_1(case, tau_factor, beta_factor) -> dict:
    
    STN = {
        
        # states
        'STATES': {
            'RM'     : {'capacity': 10000, 'initial': 10000, 'price': 0, 'isRM': True, 'isIntermed': False, 'isProd': False, 'order': 1,},
            'IA1'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 2,},       
            'IA2'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 3,},       
            'IB1'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 4,},       
            'IB2'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 5,},       
            'IB3'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 6,},       
            'IB4'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False, 'order': 7,},       
            'P1'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 8,},       
            'P2'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 9,},       
            'P3'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 10,},       
            'P4'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 11,},       
            'P5'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 12,},       
            'P6'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True, 'order': 13,},       
        },

        'STATES_SHIPMENT': { 
        },
        
        # state-to-task arcs indexed by (state, task)
        'ST_ARCS': {
            ('RM', 'TA1') : {'rho': -1.0, 'direction': -1},          
            ('RM', 'TA2') : {'rho': -1.0, 'direction': -1},
           
            ('IA1', 'TB1')  : {'rho': -1.0, 'direction': -1},
            ('IA1', 'TB2')  : {'rho': -1.0, 'direction': -1},           
            ('IA2', 'TB3')  : {'rho': -1.0, 'direction': -1},        
            ('IA2', 'TB4')  : {'rho': -1.0, 'direction': -1},        
        
            ('IB1', 'TC1')  : {'rho': -1.0, 'direction': -1},
            ('IB1', 'TC2')  : {'rho': -1.0, 'direction': -1},           
            ('IB2', 'TC5')  : {'rho': -1.0, 'direction': -1},
            ('IB3', 'TC6')  : {'rho': -1.0, 'direction': -1},            
            ('IB4', 'TC3')  : {'rho': -1.0, 'direction': -1},
            ('IB4', 'TC4')  : {'rho': -1.0, 'direction': -1},
        },
        
        # task-to-state arcs indexed by (task, state)
        'TS_ARCS': {
            ('TA1', 'IA1')  : {'rho': 1.0, 'direction': 1},            
            ('TA2', 'IA2')  : {'rho': 1.0, 'direction': 1},
            
            ('TB1', 'IB1')  : {'rho': 1.0, 'direction': 1},            
            ('TB2', 'IB2')  : {'rho': 1.0, 'direction': 1},            
            ('TB3', 'IB3')  : {'rho': 1.0, 'direction': 1},            
            ('TB4', 'IB4')  : {'rho': 1.0, 'direction': 1},
                       
            ('TC1', 'P1')  : {'rho': 1.0, 'direction': 1},            
            ('TC2', 'P2')  : {'rho': 1.0, 'direction': 1},            
            ('TC5', 'P3')  : {'rho': 1.0, 'direction': 1},            
            ('TC6', 'P4')  : {'rho': 1.0, 'direction': 1},            
            ('TC3', 'P5')  : {'rho': 1.0, 'direction': 1},            
            ('TC4', 'P6')  : {'rho': 1.0, 'direction': 1},
        },
        
        # Tasks and their corresponding transition. 
        # Transition-To-Task = 1. Task-To-Transition = -1.
        # Equivalent to parameter ipits(i, ii) in the GAMS code.
        'TASKS_TRANSITION_TASKS': { 
            },      
        
        #'EST_ST': {
        #    ('UA1', 'TA1') : {'est': 0, 'st': 0,},
        #    ('UA2', 'TA2') : {'est': 0, 'st': 0,},
            
        #    ('UA3', 'TB1') : {'est': 1, 'st': 0,},
        #    ('UA4', 'TB2') : {'est': 1, 'st': 0,},
        #    ('UA5', 'TB3') : {'est': 1, 'st': 0,},
        #    ('UA5', 'TB4') : {'est': 1, 'st': 0,},
            
        #    ('UA6', 'TC1') : {'est': 2, 'st': 0,},
        #    ('UA6', 'TC2') : {'est': 2, 'st': 0,},
        #    ('UA7', 'TC5') : {'est': 2, 'st': 0,},
        #    ('UA7', 'TC6') : {'est': 2, 'st': 0,},
        #    ('UA8', 'TC3') : {'est': 2, 'st': 0,},
        #    ('UA8', 'TC4') : {'est': 2, 'st': 0,},
        #},
    }
    
    # unit data indexed by (unit, task)
    if case == "fast_upstream":
        UNIT_TASKS = {
            ('UA1', 'TA1') : {'tau_min': 4, 'tau_max': 6, 'tau': 1, 'Bmin': 25, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA2', 'TA2') : {'tau_min': 4, 'tau_max': 6, 'tau': 1, 'Bmin': 25, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            
            ('UA3', 'TB1') : {'tau_min': 5, 'tau_max': 7, 'tau': 1, 'Bmin': 15, 'Bmax': 20, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA4', 'TB2') : {'tau_min': 5, 'tau_max': 7, 'tau': 1, 'Bmin': 15, 'Bmax': 20, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TB3') : {'tau_min': 5, 'tau_max': 7, 'tau': 1, 'Bmin': 15, 'Bmax': 20, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TB4') : {'tau_min': 5, 'tau_max': 7, 'tau': 1, 'Bmin': 15, 'Bmax': 20, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            
            ('UA6', 'TC1') : {'tau_min': ceil(5/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 5*beta_factor, 'Bmax': 6*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA6', 'TC2') : {'tau_min': ceil(5/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 5*beta_factor, 'Bmax': 6*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA7', 'TC5') : {'tau_min': ceil(5/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 5*beta_factor, 'Bmax': 6*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA7', 'TC6') : {'tau_min': ceil(5/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 5*beta_factor, 'Bmax': 6*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA8', 'TC3') : {'tau_min': ceil(5/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 5*beta_factor, 'Bmax': 6*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA8', 'TC4') : {'tau_min': ceil(5/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 5*beta_factor, 'Bmax': 6*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
        }
    elif case == "slow_upstream":    
        UNIT_TASKS = {
            ('UA1', 'TA1') : {'tau_min': ceil(5/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 5, 'Bmax': 6*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA2', 'TA2') : {'tau_min': ceil(5/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 5, 'Bmax': 6*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            
            ('UA3', 'TB1') : {'tau_min': 4, 'tau_max': 6, 'tau': 1, 'Bmin': 15, 'Bmax': 20, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA4', 'TB2') : {'tau_min': 4, 'tau_max': 6, 'tau': 1, 'Bmin': 15, 'Bmax': 20, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TB3') : {'tau_min': 4, 'tau_max': 6, 'tau': 1, 'Bmin': 15, 'Bmax': 20, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TB4') : {'tau_min': 4, 'tau_max': 6, 'tau': 1, 'Bmin': 15, 'Bmax': 20, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            
            ('UA6', 'TC1') : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 25, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA6', 'TC2') : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 25, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA7', 'TC5') : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 25, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA7', 'TC6') : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 25, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA8', 'TC3') : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 25, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA8', 'TC4') : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 25, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
        }
    elif case == "uniform":    
        UNIT_TASKS = {
            ('UA1', 'TA1') : {'tau_min': floor(4/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 25/beta_factor, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA2', 'TA2') : {'tau_min': floor(4/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 25/beta_factor, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            
            ('UA3', 'TB1') : {'tau_min': floor(4/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 25/beta_factor, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA4', 'TB2') : {'tau_min': floor(4/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 25/beta_factor, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TB3') : {'tau_min': floor(4/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 25/beta_factor, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TB4') : {'tau_min': floor(4/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 25/beta_factor, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            
            ('UA6', 'TC1') : {'tau_min': floor(4/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 25/beta_factor, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA6', 'TC2') : {'tau_min': floor(4/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 25/beta_factor, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA7', 'TC5') : {'tau_min': floor(4/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 25/beta_factor, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA7', 'TC6') : {'tau_min': floor(4/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 25/beta_factor, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA8', 'TC3') : {'tau_min': floor(4/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 25/beta_factor, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA8', 'TC4') : {'tau_min': floor(4/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 25/beta_factor, 'Bmax': 30, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
        }
        
    STN['UNIT_TASKS'] = UNIT_TASKS    
    
    return STN


def define_stn_network_2(case, tau_factor, beta_factor) -> dict:
    
    STN = {
        # states
        'STATES': {
            'RM'     : {'capacity': 10000, 'initial': 10000, 'price': 0, 'isRM': True, 'isIntermed': False, 'isProd': False},
            
            'IA1'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
            'IA2'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
            'IA3'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
            
            'IB1'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
            'IB2'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
            'IB3'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
            
            'IC1'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
            'IC2'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
            'IC3'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
            
            'ID1'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
            'ID2'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
            'ID3'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
            
            'IE1'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
            'IE2'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
            'IE3'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
            
            'P1'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},       
            'P2'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},       
            'P3'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},       
        },

        'STATES_SHIPMENT': { 
            #('P1', 25) : {'demand':75},        
            #('P2', 25) : {'demand':75},
            #('P3', 25) : {'demand':75},
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
        
        #'EST_ST': {
        #    ('UA1', 'TA1') : {'est': 0, 'st': 15,},
        #    ('UA1', 'TA2') : {'est': 0, 'st': 15,},
        #    ('UA1', 'TA3') : {'est': 0, 'st': 15,},           
            
        #    ('UA2', 'TB1') : {'est': 1, 'st': 18,},
        #    ('UA2', 'TB2') : {'est': 1, 'st': 18,},
        #    ('UA2', 'TB3') : {'est': 1, 'st': 18,},
            
        #    ('UA3', 'TC1') : {'est': 2, 'st': 17,},
        #    ('UA3', 'TC2') : {'est': 2, 'st': 17,},
        #    ('UA3', 'TC3') : {'est': 2, 'st': 17,},
            
        #    ('UA4', 'TD1') : {'est': 3, 'st': 2,},
        #    ('UA4', 'TD2') : {'est': 3, 'st': 2,},
        #    ('UA4', 'TD3') : {'est': 3, 'st': 2,},
            
        #    ('UA5', 'TE1') : {'est': 4, 'st': 1,},
        #    ('UA5', 'TE2') : {'est': 4, 'st': 1,},
        #    ('UA5', 'TE3') : {'est': 4, 'st': 1,},
            
        #    ('UA6', 'TF1') : {'est': 5, 'st': 0,},
        #    ('UA6', 'TF2') : {'est': 5, 'st': 0,},
        #    ('UA6', 'TF3') : {'est': 5, 'st': 0,},
                        
        #},
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
            
            ('UA4', 'TD1') : {'tau_min': 3, 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA4', 'TD2') : {'tau_min': 3, 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA4', 'TD3') : {'tau_min': 3, 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            
            ('UA5', 'TE1') : {'tau_min': 3, 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TE2') : {'tau_min': 3, 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TE3') : {'tau_min': 3, 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            
            ('UA6', 'TF1') : {'tau_min': 3, 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA6', 'TF2') : {'tau_min': 3, 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA6', 'TF3') : {'tau_min': 3, 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
        }
    elif case == "slow_upstream":
        UNIT_TASKS = {
            ('UA1', 'TA1') : {'tau_min': ceil(4/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA1', 'TA2') : {'tau_min': ceil(4/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA1', 'TA3') : {'tau_min': ceil(4/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            
            ('UA2', 'TB1') : {'tau_min': ceil(4/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA2', 'TB2') : {'tau_min': ceil(4/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA2', 'TB3') : {'tau_min': ceil(4/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            
            ('UA3', 'TC1') : {'tau_min': ceil(4/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA3', 'TC2') : {'tau_min': ceil(4/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA3', 'TC3') : {'tau_min': ceil(4/tau_factor), 'tau_max': ceil(7*tau_factor), 'tau': 1, 'Bmin': 9, 'Bmax': 10*beta_factor, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            
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
            ('UA1', 'TA1') : {'tau_min': floor(6/tau_factor), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA1', 'TA2') : {'tau_min': floor(6/tau_factor), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA1', 'TA3') : {'tau_min': floor(6/tau_factor), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            
            ('UA2', 'TB1') : {'tau_min': floor(6/tau_factor), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA2', 'TB2') : {'tau_min': floor(6/tau_factor), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA2', 'TB3') : {'tau_min': floor(6/tau_factor), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            
            ('UA3', 'TC1') : {'tau_min': floor(6/tau_factor), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA3', 'TC2') : {'tau_min': floor(6/tau_factor), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA3', 'TC3') : {'tau_min': floor(6/tau_factor), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            
            ('UA4', 'TD1') : {'tau_min': floor(6/tau_factor), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA4', 'TD2') : {'tau_min': floor(6/tau_factor), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA4', 'TD3') : {'tau_min': floor(6/tau_factor), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            
            ('UA5', 'TE1') : {'tau_min': floor(6/tau_factor), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TE2') : {'tau_min': floor(6/tau_factor), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TE3') : {'tau_min': floor(6/tau_factor), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            
            ('UA6', 'TF1') : {'tau_min': floor(6/tau_factor), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA6', 'TF2') : {'tau_min': floor(6/tau_factor), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA6', 'TF3') : {'tau_min': floor(6/tau_factor), 'tau_max': 14, 'tau': 1, 'Bmin': 65/beta_factor, 'Bmax': 70, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
        }
        
    STN['UNIT_TASKS'] = UNIT_TASKS  
            
    return STN

