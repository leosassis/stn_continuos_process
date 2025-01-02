H_Network_0 = 12

Network_0 = {
    # time grid
    'TIME':  range(0, H_Network_0+1),
    
    # states
    'STATES': {
        'RM'     : {'capacity': 450, 'initial': 400, 'price':  0, 'isRM': True, 'isIntermed': False, 'isProd': False},
        'IA1'    : {'capacity': 450, 'initial': 0, 'price': 10, 'isRM': False, 'isIntermed': True, 'isProd': False},       
        'P1'     : {'capacity': 450, 'initial': 0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},       
    },

    'STATES_SHIPMENT': {
        ('P1', 8) : {'demand':10},        
    },
    
    # state-to-task arcs indexed by (state, task)
    'ST_ARCS': {
        ('RM', 'TA1') : {'rho': -1.0, 'direction': -1},
        ('RM', 'TA2') : {'rho': -1.0, 'direction': -1},
        
        ('RM', 'TA3')  : {'rho': -1.0, 'direction': -1},
        ('RM', 'ITA3') : {'rho': -0.25, 'direction': -1},
        ('RM', 'TA3I') : {'rho': -0.5, 'direction': -1},
        
        ('IA1', 'TC1')  : {'rho': -1.0, 'direction': -1},
        ('IA1', 'ITC1') : {'rho': -0.25, 'direction': -1},
        ('IA1', 'TC1I') : {'rho': -0.5, 'direction': -1},
    },
    
    # task-to-state arcs indexed by (task, state)
    'TS_ARCS': {
        ('TA1', 'IA1')  : {'rho': 1.0, 'direction': 1},
        ('TA2', 'IA1')  : {'rho': 1.0, 'direction': 1},
        ('TA3', 'IA1')  : {'rho': 1.0, 'direction': 1},
        ('ITA3', 'IA1') : {'rho': 0.25, 'direction': 1},
        ('TA3I', 'IA1') : {'rho': 0.5, 'direction': 1},
        
        ('TC1', 'P1')  : {'rho': 1.0, 'direction': 1},
        ('ITC1', 'P1') : {'rho': 0.25, 'direction': 1},
        ('TC1I', 'P1') : {'rho': 0.5, 'direction': 1},
        
    },
    
    # Tasks and their corresponding transition. 
    # Transition-To-Task = 1. Task-To-Transition = -1.
    # Equivalent to parameter ipits(i, ii) in the GAMS code.
    'TASKS_TRANSITION_TASKS': { 
        ('TA3', 'ITA3') : {'isSU': True, 'isSD': False, 'isDirect': False, 'direction': 1},
        ('TA3', 'TA3I') : {'isSU': False, 'isSD': True, 'isDirect': False, 'direction': -1},
        
        ('TC1', 'ITC1')   : {'isSU': True, 'isSD': False, 'isDirect': False, 'direction': 1},
        ('TC1', 'TC1I')   : {'isSU': False, 'isSD': True, 'isDirect': False, 'direction': -1},
    },
    
    # unit data indexed by (unit, task)
    'UNIT_TASKS': {
        ('UA1', 'TA1') : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 3.5, 'Bmax': 5, 'Cost': 4, 'vCost': 1, 'sCost': 40.5, 'direction': 1,},
        ('UA2', 'TA2') : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 2.1, 'Bmax': 3, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
        
        ('UA2', 'TA3')  : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 2.1, 'Bmax': 3, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
        ('UA2', 'ITA3') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 2.8, 'Bmax': 4, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},
        ('UA2', 'TA3I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 1.4, 'Bmax': 2, 'Cost': 3, 'vCost': 1, 'sCost': 0, 'direction': -1,},
        
        ('UC5', 'TC1')  : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 8, 'Bmax': 8, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
        ('UC5', 'ITC1') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 4, 'Bmax': 4, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},
        ('UC5', 'TC1I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 2, 'Bmax': 2, 'Cost': 3, 'vCost': 1, 'sCost': 0, 'direction': -1,},
    },
}

H_Network_1 = 50

Network_1 = {
    # time grid
    'TIME':  range(0, H_Network_1+1),
    
    # states
    'STATES': {
        'RM'     : {'capacity': 450, 'initial': 400, 'price':  0, 'isRM': True, 'isIntermed': False, 'isProd': False},
        'IA1'    : {'capacity': 450, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': True, 'isProd': False},       
        'P1'     : {'capacity': 450, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},       
        'P2'     : {'capacity': 450, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},       
    },

    'STATES_SHIPMENT': {
        ('P1', 10) : {'demand':15},
        ('P2', 14) : {'demand':10},
        ('P1', 25) : {'demand':15},
        ('P2', 26) : {'demand':10},
        ('P1', 33) : {'demand':15},
        ('P2', 38) : {'demand':10},
        ('P1', 44) : {'demand':15},
        ('P2', 48) : {'demand':10},
    },
    
    # state-to-task arcs indexed by (state, task)
    'ST_ARCS': {
        ('RM', 'TA1') : {'rho': -1.0, 'direction': -1},
        ('RM', 'TA2') : {'rho': -1.0, 'direction': -1},
        
        ('RM', 'TA3')  : {'rho': -1.0, 'direction': -1},
        ('RM', 'ITA3') : {'rho': -0.25, 'direction': -1},
        ('RM', 'TA3I') : {'rho': -0.5, 'direction': -1},
    
		('IA1', 'TC1')  : {'rho': -1.0, 'direction': -1},
        ('IA1', 'ITC1') : {'rho': -0.25, 'direction': -1},
        ('IA1', 'TC1I') : {'rho': -0.5, 'direction': -1},
		
		('IA1', 'TC2')  : {'rho': -1.0, 'direction': -1},
        ('IA1', 'ITC2') : {'rho': -0.25, 'direction': -1},
        ('IA1', 'TC2I') : {'rho': -0.5, 'direction': -1},
   
        ('IA1', 'DTC1TC2') : {'rho': -0.25, 'direction': -1},
        ('IA1', 'DTC2TC1') : {'rho': -0.25, 'direction': -1},
    },
    
    # task-to-state arcs indexed by (task, state)
    'TS_ARCS': {
        ('TA1', 'IA1')  : {'rho': 1.0, 'direction': 1},
        ('TA2', 'IA1')  : {'rho': 1.0, 'direction': 1},
        ('TA3', 'IA1')  : {'rho': 1.0, 'direction': 1},
        ('ITA3', 'IA1') : {'rho': 0.25, 'direction': 1},
        ('TA3I', 'IA1') : {'rho': 0.5, 'direction': 1},
        
		('TC1', 'P1')  : {'rho': 1.0, 'direction': 1},
        ('ITC1', 'P1') : {'rho': 0.25, 'direction': 1},
        ('TC1I', 'P1') : {'rho': 0.5, 'direction': 1},
		
		('TC2', 'P2')  : {'rho': 1.0, 'direction': 1},
        ('ITC2', 'P2') : {'rho': 0.25, 'direction': 1},
        ('TC2I', 'P2') : {'rho': 0.5, 'direction': 1},
   
        ('DTC1TC2', 'P2') : {'rho': 0.25, 'direction': 1},
        ('DTC2TC1', 'P1') : {'rho': 0.25, 'direction': 1},

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
    },
    
    # unit data indexed by (unit, task)
    'UNIT_TASKS': {
        ('UA1', 'TA1') : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 3.5, 'Bmax': 5, 'Cost': 4, 'vCost': 1, 'sCost': 40.5, 'direction': 1,},
        ('UA2', 'TA2') : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 2.1, 'Bmax': 3, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
        
        ('UA2', 'TA3')  : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 2.1, 'Bmax': 3, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
        ('UA2', 'ITA3') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 2.8, 'Bmax': 4, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},
        ('UA2', 'TA3I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 1.4, 'Bmax': 2, 'Cost': 3, 'vCost': 1, 'sCost': 0, 'direction': -1,},
        
        ('UC5', 'TC1')  : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 3, 'Bmax': 3, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
        ('UC5', 'ITC1') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 4, 'Bmax': 4, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},
        ('UC5', 'TC1I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 2, 'Bmax': 2, 'Cost': 3, 'vCost': 1, 'sCost': 0, 'direction': -1,},
        
		('UC5', 'TC2')  : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 3, 'Bmax': 3, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
        ('UC5', 'ITC2') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 4, 'Bmax': 4, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},
        ('UC5', 'TC2I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 2, 'Bmax': 2, 'Cost': 3, 'vCost': 1, 'sCost': 0, 'direction': -1,},
		
		('UC5', 'DTC1TC2') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 6, 'Bmax': 6, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},
        ('UC5', 'DTC2TC1') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 6, 'Bmax': 6, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},   
    },
}

H_Network_2 = 200

Network_2 = {
    # time grid
    'TIME':  range(0, H_Network_2+1),
    
    # states
    'STATES': {
        'RM'     : {'capacity': 450, 'initial': 400, 'price':  0, 'isRM': True, 'isIntermed': False, 'isProd': False},
        'IA1'    : {'capacity': 450, 'initial': 0, 'price': 10, 'isRM': False, 'isIntermed': True, 'isProd': False},       
        'P1'     : {'capacity': 450, 'initial': 0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},       
    },

    'STATES_SHIPMENT': {
        ('P1', 8) : {'demand':10},
        ('P1', 20) : {'demand':25},
        ('P1', 25) : {'demand':35},
        ('P1', 40) : {'demand':50},
        ('P1', 55) : {'demand':25},
        ('P1', 60) : {'demand':35},
        ('P1', 75) : {'demand':50},
        ('P1', 83) : {'demand':25},
        ('P1', 95) : {'demand':35},
        ('P1', 105) : {'demand':10},
        ('P1', 120) : {'demand':25},
        ('P1', 125) : {'demand':35},
        ('P1', 140) : {'demand':50},
        ('P1', 155) : {'demand':25},
        ('P1', 160) : {'demand':35},
        ('P1', 175) : {'demand':50},
        ('P1', 183) : {'demand':25},
        ('P1', 195) : {'demand':35},
    },
    
    # state-to-task arcs indexed by (state, task)
    'ST_ARCS': {
        ('RM', 'TA1') : {'rho': -1.0, 'direction': -1},
        ('RM', 'TA2') : {'rho': -1.0, 'direction': -1},
        
        ('RM', 'TA3')  : {'rho': -1.0, 'direction': -1},
        ('RM', 'ITA3') : {'rho': -0.25, 'direction': -1},
        ('RM', 'TA3I') : {'rho': -0.5, 'direction': -1},
        
        ('IA1', 'TC1')  : {'rho': -1.0, 'direction': -1},
        ('IA1', 'ITC1') : {'rho': -0.25, 'direction': -1},
        ('IA1', 'TC1I') : {'rho': -0.5, 'direction': -1},
    },
    
    # task-to-state arcs indexed by (task, state)
    'TS_ARCS': {
        ('TA1', 'IA1')  : {'rho': 1.0, 'direction': 1},
        ('TA2', 'IA1')  : {'rho': 1.0, 'direction': 1},
        ('TA3', 'IA1')  : {'rho': 1.0, 'direction': 1},
        ('ITA3', 'IA1') : {'rho': 0.25, 'direction': 1},
        ('TA3I', 'IA1') : {'rho': 0.5, 'direction': 1},
        
        ('TC1', 'P1')  : {'rho': 1.0, 'direction': 1},
        ('ITC1', 'P1') : {'rho': 0.25, 'direction': 1},
        ('TC1I', 'P1') : {'rho': 0.5, 'direction': 1},
        
    },
    
    # Tasks and their corresponding transition. 
    # Transition-To-Task = 1. Task-To-Transition = -1.
    # Equivalent to parameter ipits(i, ii) in the GAMS code.
    'TASKS_TRANSITION_TASKS': { 
        ('TA3', 'ITA3') : {'isSU': True, 'isSD': False, 'isDirect': False, 'direction': 1},
        ('TA3', 'TA3I') : {'isSU': False, 'isSD': True, 'isDirect': False, 'direction': -1},
        
        ('TC1', 'ITC1')   : {'isSU': True, 'isSD': False, 'isDirect': False, 'direction': 1},
        ('TC1', 'TC1I')   : {'isSU': False, 'isSD': True, 'isDirect': False, 'direction': -1},
    },
    
    # unit data indexed by (unit, task)
    'UNIT_TASKS': {
        ('UA1', 'TA1') : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 3.5, 'Bmax': 5, 'Cost': 4, 'vCost': 1, 'sCost': 40.5, 'direction': 1,},
        ('UA2', 'TA2') : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 2.1, 'Bmax': 3, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
        
        ('UA2', 'TA3')  : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 2.1, 'Bmax': 3, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
        ('UA2', 'ITA3') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 2.8, 'Bmax': 4, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},
        ('UA2', 'TA3I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 1.4, 'Bmax': 2, 'Cost': 3, 'vCost': 1, 'sCost': 0, 'direction': -1,},
        
        ('UC5', 'TC1')  : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 4, 'Bmax': 4, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
        ('UC5', 'ITC1') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 4, 'Bmax': 4, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},
        ('UC5', 'TC1I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 2, 'Bmax': 2, 'Cost': 3, 'vCost': 1, 'sCost': 0, 'direction': -1,},
    },
}
