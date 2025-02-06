

def define_stn_network(beta_min_factor, tau_max_factor):
    
    STN = {
        # states
        'STATES': {
            'RM'     : {'capacity': 10000, 'initial': 10000, 'price':  0, 'isRM': True, 'isIntermed': False, 'isProd': False},
            'IA1'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
            'IA2'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
            'IB1'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
            'IB2'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
            'IB3'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
            'IB4'    : {'capacity': 10000, 'initial':   0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
            'P1'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},       
            'P2'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},       
            'P3'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},       
            'P4'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},       
            'P5'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},       
            'P6'     : {'capacity': 10000, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},       
        },

        'STATES_SHIPMENT': { 
        #('P2', 46) : {'demand':25},
        #('P4', 92) : {'demand':25},       
        #('P6', 100) : {'demand':25},
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
            ('IB4', 'ITC3') : {'rho': -1.0, 'direction': -1},
            ('IB4', 'TC3I') : {'rho': -1.0, 'direction': -1},
            
            ('IB4', 'TC4')  : {'rho': -1.0, 'direction': -1},
            ('IB4', 'ITC4') : {'rho': -1.0, 'direction': -1},
            ('IB4', 'TC4I') : {'rho': -1.0, 'direction': -1},
    
            ('IB4', 'DTC3TC4') : {'rho': -1.0, 'direction': -1},
            ('IB4', 'DTC4TC3') : {'rho': -1.0, 'direction': -1},        
        
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
            ('ITC3', 'P5') : {'rho': 1.0, 'direction': 1},
            ('TC3I', 'P5') : {'rho': 1.0, 'direction': 1},
            
            ('TC4', 'P6')  : {'rho': 1.0, 'direction': 1},
            ('ITC4', 'P6') : {'rho': 1.0, 'direction': 1},
            ('TC4I', 'P6') : {'rho': 1.0, 'direction': 1},
    
            ('DTC3TC4', 'P6') : {'rho': 1, 'direction': 1},
            #('DTC3TC4', 'P5') : {'rho': 0.5, 'direction': 1},
            
            ('DTC4TC3', 'P5') : {'rho': 1, 'direction': 1},
            #('DTC4TC3', 'P6') : {'rho': 0.5, 'direction': 1},

        },
        
        # Tasks and their corresponding transition. 
        # Transition-To-Task = 1. Task-To-Transition = -1.
        # Equivalent to parameter ipits(i, ii) in the GAMS code.
        'TASKS_TRANSITION_TASKS': { 
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
            
            ('UA2', 'TA2') : {'tau_min': 5, 'tau_max': 5*tau_max_factor, 'tau': 1, 'Bmin': 5*beta_min_factor, 'Bmax': 5, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            
            ('UA3', 'TB1') : {'tau_min': 5, 'tau_max': 5*tau_max_factor, 'tau': 1, 'Bmin': 5*beta_min_factor, 'Bmax': 5, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA3', 'TB2') : {'tau_min': 5, 'tau_max': 5*tau_max_factor, 'tau': 1, 'Bmin': 5*beta_min_factor, 'Bmax': 5, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            
            ('UA4', 'TB3') : {'tau_min': 5, 'tau_max': 5*tau_max_factor, 'tau': 1, 'Bmin': 5*beta_min_factor, 'Bmax': 5, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA4', 'TB4') : {'tau_min': 5, 'tau_max': 5*tau_max_factor, 'tau': 1, 'Bmin': 5*beta_min_factor, 'Bmax': 5, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            
            ('UA7', 'TC1') : {'tau_min': 5, 'tau_max': 5*tau_max_factor, 'tau': 1, 'Bmin': 20*beta_min_factor, 'Bmax': 20, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA7', 'TC2') : {'tau_min': 5, 'tau_max': 5*tau_max_factor, 'tau': 1, 'Bmin': 20*beta_min_factor, 'Bmax': 20, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            
            ('UA5', 'TC5') : {'tau_min': 5, 'tau_max': 5*tau_max_factor, 'tau': 1, 'Bmin': 20*beta_min_factor, 'Bmax': 20, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            ('UA5', 'TC6') : {'tau_min': 5, 'tau_max': 5*tau_max_factor, 'tau': 1, 'Bmin': 20*beta_min_factor, 'Bmax': 20, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
            
            ('UC6', 'TC3')  : {'tau_min': 5, 'tau_max': 5*tau_max_factor, 'tau': 1, 'Bmin': 20*beta_min_factor, 'Bmax': 20, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
            ('UC6', 'ITC3') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 4*beta_min_factor, 'Bmax': 4, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},
            ('UC6', 'TC3I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 2*beta_min_factor, 'Bmax': 2, 'Cost': 3, 'vCost': 1, 'sCost': 0, 'direction': -1,},
            
            ('UC6', 'TC4')  : {'tau_min': 5, 'tau_max': 5*tau_max_factor, 'tau': 1, 'Bmin': 20*beta_min_factor, 'Bmax': 20, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
            ('UC6', 'ITC4') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 4*beta_min_factor, 'Bmax': 4, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},
            ('UC6', 'TC4I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 2*beta_min_factor, 'Bmax': 2, 'Cost': 3, 'vCost': 1, 'sCost': 0, 'direction': -1,},
            
            ('UC6', 'DTC3TC4') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 6*beta_min_factor, 'Bmax': 6, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},
            ('UC6', 'DTC4TC3') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 6*beta_min_factor, 'Bmax': 6, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},           
            
        },
    }
    return STN

