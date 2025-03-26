

def define_stn_network(beta_min_factor, tau_max_factor):
    
    STN = {
        # states
        'STATES': {
            'RM'     : {'capacity': 10000, 'initial': 10000, 'price':  0, 'isRM': True, 'isIntermed': False, 'isProd': False},
            'IA1'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
            'IA2'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
            'IA3'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
            'IB1'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
            'IB2'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
            'P1'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},       
            'P2'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},       
            'P3'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},       
            'P4'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},       
        },

        'STATES_SHIPMENT': { 
        ('P1', 25) : {'demand':25},
        ('P2', 46) : {'demand':25},
        ('P3', 25) : {'demand':25},
        ('P4', 46) : {'demand':25},       
        
        #('P1', 80) : {'demand':25},
        #('P2', 86) : {'demand':25},
        #('P3', 80) : {'demand':25},
        #('P4', 86) : {'demand':25},        
        },
        
        # state-to-task arcs indexed by (state, task)
        'ST_ARCS': {
            ('RM', 'TA1') : {'rho': -1.0, 'direction': -1},
        
            ('RM', 'TA2') : {'rho': -1.0, 'direction': -1},
            
            ('RM', 'TA3')  : {'rho': -1.0, 'direction': -1},
            ('RM', 'ITA3') : {'rho': -0.25, 'direction': -1},
            ('RM', 'TA3I') : {'rho': -0.5, 'direction': -1},
        
            ('IA1', 'TB1')  : {'rho': -1.0, 'direction': -1},
            ('IA2', 'TB1')  : {'rho': -1.0, 'direction': -1},
            ('IA3', 'TB2')  : {'rho': -1.0, 'direction': -1},        
        
            ('IB1', 'TC1')  : {'rho': -1.0, 'direction': -1},
            ('IB1', 'ITC1') : {'rho': -0.25, 'direction': -1},
            ('IB1', 'TC1I') : {'rho': -0.5, 'direction': -1},
            
            ('IB1', 'TC2')  : {'rho': -1.0, 'direction': -1},
            ('IB1', 'ITC2') : {'rho': -0.25, 'direction': -1},
            ('IB1', 'TC2I') : {'rho': -0.5, 'direction': -1},
    
            ('IB1', 'DTC1TC2') : {'rho': -0.25, 'direction': -1},
            ('IB1', 'DTC2TC1') : {'rho': -0.25, 'direction': -1},            
            
            ('IB2', 'TC3')  : {'rho': -1.0, 'direction': -1},
            ('IB2', 'ITC3') : {'rho': -0.25, 'direction': -1},
            ('IB2', 'TC3I') : {'rho': -0.5, 'direction': -1},
            
            ('IB2', 'TC4')  : {'rho': -1.0, 'direction': -1},
            ('IB2', 'ITC4') : {'rho': -0.25, 'direction': -1},
            ('IB2', 'TC4I') : {'rho': -0.5, 'direction': -1},
    
            ('IB2', 'DTC3TC4') : {'rho': -0.25, 'direction': -1},
            ('IB2', 'DTC4TC3') : {'rho': -0.25, 'direction': -1},        
        
        },
        
        # task-to-state arcs indexed by (task, state)
        'TS_ARCS': {
            ('TA1', 'IA1')  : {'rho': 1.0, 'direction': 1},
            ('TA2', 'IA2')  : {'rho': 1.0, 'direction': 1},
            
            ('TA3', 'IA3')  : {'rho': 1.0, 'direction': 1},
            ('ITA3', 'IA3') : {'rho': 0.25, 'direction': 1},
            ('TA3I', 'IA3') : {'rho': 0.5, 'direction': 1},
            
            ('TB1', 'IB1')  : {'rho': 1.0, 'direction': 1},
            ('TB2', 'IB1')  : {'rho': 1.0, 'direction': 1},
            ('TB2', 'IB2')  : {'rho': 1.0, 'direction': 1},
                       
            ('TC1', 'P1')  : {'rho': 1.0, 'direction': 1},
            ('ITC1', 'P1') : {'rho': 0.25, 'direction': 1},
            ('TC1I', 'P1') : {'rho': 0.5, 'direction': 1},
            
            ('TC2', 'P2')  : {'rho': 1.0, 'direction': 1},
            ('ITC2', 'P2') : {'rho': 0.25, 'direction': 1},
            ('TC2I', 'P2') : {'rho': 0.5, 'direction': 1},
    
            ('DTC1TC2', 'P2') : {'rho': 0.125, 'direction': 1},
            ('DTC1TC2', 'P1') : {'rho': 0.125, 'direction': 1},
            ('DTC2TC1', 'P1') : {'rho': 0.125, 'direction': 1},
            ('DTC2TC1', 'P2') : {'rho': 0.125, 'direction': 1},
            
            ('TC3', 'P3')  : {'rho': 1.0, 'direction': 1},
            ('ITC3', 'P3') : {'rho': 0.25, 'direction': 1},
            ('TC3I', 'P3') : {'rho': 0.5, 'direction': 1},
            
            ('TC4', 'P4')  : {'rho': 1.0, 'direction': 1},
            ('ITC4', 'P4') : {'rho': 0.25, 'direction': 1},
            ('TC4I', 'P4') : {'rho': 0.5, 'direction': 1},
    
            ('DTC3TC4', 'P4') : {'rho': 0.125, 'direction': 1},
            ('DTC3TC4', 'P3') : {'rho': 0.125, 'direction': 1},
            ('DTC4TC3', 'P3') : {'rho': 0.125, 'direction': 1},
            ('DTC4TC3', 'P4') : {'rho': 0.125, 'direction': 1},

        },
        
        # Tasks and their corresponding transition. 
        # Transition-To-Task = 1. Task-To-Transition = -1.
        # Equivalent to parameter ipits(i, ii) in the GAMS code.
        'TASKS_TRANSITION_TASKS': { 
            ('TA3', 'ITA3') : {'isSU': True, 'isSD': False, 'isDirect': False, 'direction': 1},
            ('TA3', 'TA3I') : {'isSU': False, 'isSD': True, 'isDirect': False, 'direction': -1},
            
            ('TC1', 'ITC1')   : {'isSU': True, 'isSD': False, 'isDirect': False, 'direction': 1},
            ('TC1', 'TC1I')   : {'isSU': False, 'isSD': True, 'isDirect': False, 'direction': -1},
            
            ('TC2', 'ITC2')   : {'isSU': True, 'isSD': False, 'isDirect': False, 'direction': 1},
            ('TC2', 'TC2I')   : {'isSU': False, 'isSD': True, 'isDirect': False, 'direction': -1},
            
            ('TC1', 'DTC2TC1')   : {'isSU': False, 'isSD': False, 'isDirect': True, 'direction': 1},
            ('TC1', 'DTC1TC2')   : {'isSU': False, 'isSD': False, 'isDirect': True, 'direction': -1},
            
            ('TC2', 'DTC1TC2')   : {'isSU': False, 'isSD': False, 'isDirect': True, 'direction': 1},
            ('TC2', 'DTC2TC1')   : {'isSU': False, 'isSD': False, 'isDirect': True, 'direction': -1},
            
            
            ('TC3', 'ITC3')   : {'isSU': True, 'isSD': False, 'isDirect': False, 'direction': 1},
            ('TC3', 'TC3I')   : {'isSU': False, 'isSD': True, 'isDirect': False, 'direction': -1},
            
            ('TC4', 'ITC4')   : {'isSU': True, 'isSD': False, 'isDirect': False, 'direction': 1},
            ('TC4', 'TC4I')   : {'isSU': False, 'isSD': True, 'isDirect': False, 'direction': -1},
            
            ('TC3', 'DTC4TC3')   : {'isSU': False, 'isSD': False, 'isDirect': True, 'direction': 1},
            ('TC3', 'DTC3TC4')   : {'isSU': False, 'isSD': False, 'isDirect': True, 'direction': -1},
            
            ('TC4', 'DTC3TC4')   : {'isSU': False, 'isSD': False, 'isDirect': True, 'direction': 1},
            ('TC4', 'DTC4TC3')   : {'isSU': False, 'isSD': False, 'isDirect': True, 'direction': -1},
        },
        
        # unit data indexed by (unit, task)
        'UNIT_TASKS': {
            ('UA1', 'TA1') : {'tau_min': 5, 'tau_max': 5*tau_max_factor, 'tau': 1, 'Bmin': 5*beta_min_factor, 'Bmax': 5, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA6', 'TA2') : {'tau_min': 5, 'tau_max': 5*tau_max_factor, 'tau': 1, 'Bmin': 3*beta_min_factor, 'Bmax': 3, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            
            ('UA2', 'TA3')  : {'tau_min': 5, 'tau_max': 5*tau_max_factor, 'tau': 1, 'Bmin': 3*beta_min_factor, 'Bmax': 3, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
            ('UA2', 'ITA3') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 4*beta_min_factor, 'Bmax': 4, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},
            ('UA2', 'TA3I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 3*beta_min_factor, 'Bmax': 2, 'Cost': 3, 'vCost': 1, 'sCost': 0, 'direction': -1,},
            
            ('UA3', 'TB1') : {'tau_min': 4, 'tau_max': 4*tau_max_factor, 'tau': 1, 'Bmin': 5.5*beta_min_factor, 'Bmax': 5.5, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA3', 'TB2') : {'tau_min': 4, 'tau_max': 4*tau_max_factor, 'tau': 1, 'Bmin': 5.5*beta_min_factor, 'Bmax': 5.5, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
           
            ('UA4', 'TB1') : {'tau_min': 5, 'tau_max': 5*tau_max_factor, 'tau': 1, 'Bmin': 3*beta_min_factor, 'Bmax': 3, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA4', 'TB2') : {'tau_min': 5, 'tau_max': 5*tau_max_factor, 'tau': 1, 'Bmin': 3*beta_min_factor, 'Bmax': 3, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
                       
            ('UC5', 'TC1')  : {'tau_min': 5, 'tau_max': 5*tau_max_factor, 'tau': 1, 'Bmin': 3*beta_min_factor, 'Bmax': 3, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
            ('UC5', 'ITC1') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 4*beta_min_factor, 'Bmax': 4, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},
            ('UC5', 'TC1I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 2*beta_min_factor, 'Bmax': 2, 'Cost': 3, 'vCost': 1, 'sCost': 0, 'direction': -1,},
            
            ('UC5', 'TC2')  : {'tau_min': 5, 'tau_max': 5*tau_max_factor, 'tau': 1, 'Bmin': 3*beta_min_factor, 'Bmax': 3, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
            ('UC5', 'ITC2') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 4*beta_min_factor, 'Bmax': 4, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},
            ('UC5', 'TC2I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 2*beta_min_factor, 'Bmax': 2, 'Cost': 3, 'vCost': 1, 'sCost': 0, 'direction': -1,},
            
            ('UC5', 'DTC1TC2') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 6*beta_min_factor, 'Bmax': 6, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},
            ('UC5', 'DTC2TC1') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 6*beta_min_factor, 'Bmax': 6, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},   
            
            ('UC6', 'TC3')  : {'tau_min': 5, 'tau_max': 5*tau_max_factor, 'tau': 1, 'Bmin': 3*beta_min_factor, 'Bmax': 3, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
            ('UC6', 'ITC3') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 4*beta_min_factor, 'Bmax': 4, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},
            ('UC6', 'TC3I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 2*beta_min_factor, 'Bmax': 2, 'Cost': 3, 'vCost': 1, 'sCost': 0, 'direction': -1,},
            
            ('UC6', 'TC4')  : {'tau_min': 5, 'tau_max': 5*tau_max_factor, 'tau': 1, 'Bmin': 3*beta_min_factor, 'Bmax': 3, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
            ('UC6', 'ITC4') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 4*beta_min_factor, 'Bmax': 4, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},
            ('UC6', 'TC4I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 2*beta_min_factor, 'Bmax': 2, 'Cost': 3, 'vCost': 1, 'sCost': 0, 'direction': -1,},
            
            ('UC6', 'DTC3TC4') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 6*beta_min_factor, 'Bmax': 6, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},
            ('UC6', 'DTC4TC3') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 6*beta_min_factor, 'Bmax': 6, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},           
            
        },
    }
    return STN