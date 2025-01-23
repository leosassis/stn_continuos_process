STN = {
    # states
    'STATES': {
        'RM'     : {'capacity': 10000, 'initial': 10000, 'price':  0, 'isRM': True, 'isIntermed': False, 'isProd': False},
        'IA1'    : {'capacity': 10000, 'initial': 0, 'price': 10, 'isRM': False, 'isIntermed': True, 'isProd': False},                
        'P1'     : {'capacity': 10000, 'initial': 0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},       
    },

    'STATES_SHIPMENT': {
        #('P1', 8) : {'demand':10},        
        #('P1', 10) : {'demand':25},        
    },
    
    # state-to-task arcs indexed by (state, task)
    'ST_ARCS': {
        ('RM', 'TA1') : {'rho': -1.0, 'direction': -1},
        ('IA1', 'TC1')  : {'rho': -1.0, 'direction': -1},
    },
    
    # task-to-state arcs indexed by (task, state)
    'TS_ARCS': {
        ('TA1', 'IA1')  : {'rho': 1.0, 'direction': 1},      
        ('TC1', 'P1')  : {'rho': 1.0, 'direction': 1},      
    },
    
    # Tasks and their corresponding transition. 
    # Transition-To-Task = 1. Task-To-Transition = -1.
    # Equivalent to parameter ipits(i, ii) in the GAMS code.
    'TASKS_TRANSITION_TASKS': {         
    },
    
    # unit data indexed by (unit, task)
    'UNIT_TASKS': {
        ('UA1', 'TA1') : {'tau_min': 6, 'tau_max': 6, 'tau': 1, 'Bmin': 0.5, 'Bmax': 0.5, 'Cost': 4, 'vCost': 1, 'sCost': 40.5, 'direction': 1,},
        ('UA2', 'TA1') : {'tau_min': 5, 'tau_max': 5, 'tau': 1, 'Bmin': 0.5, 'Bmax': 0.5, 'Cost': 4, 'vCost': 1, 'sCost': 40.5, 'direction': 1,},              
        ('UC5', 'TC1')  : {'tau_min': 6, 'tau_max': 6, 'tau': 1, 'Bmin': 2, 'Bmax': 3, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},       
    },
}