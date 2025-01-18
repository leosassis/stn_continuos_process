
FP_Network_0_Horizon = 30
FP_Network_1_Horizon = 30
H_Network_1 = 50
H_Network_2 = 200
H_Network_2_Max = 200
H_Network_test = 10

FP_Network_0 = {
    # time grid
    'TIME':  range(0, FP_Network_0_Horizon+1),
    
    # states
    'STATES': {
        'RM'     : {'capacity': 45, 'initial': 40, 'price':  0, 'isRM': True, 'isIntermed': False, 'isProd': False},
        'IA1'    : {'capacity': 45, 'initial': 0, 'price': 10, 'isRM': False, 'isIntermed': True, 'isProd': False},       
        'P1'     : {'capacity': 45, 'initial': 0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},       
    },

    'STATES_SHIPMENT': {
        ('P1', 8) : {'demand':10},        
        #('P1', 10) : {'demand':12},        
    },
    
    # state-to-task arcs indexed by (state, task)
    'ST_ARCS': {
        ('RM', 'TA1') : {'rho': -1.0, 'direction': -1},
        
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
        
        ('UA2', 'TA3')  : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 2.1, 'Bmax': 3, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
        ('UA2', 'ITA3') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 2.8, 'Bmax': 4, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},
        ('UA2', 'TA3I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 1.4, 'Bmax': 2, 'Cost': 3, 'vCost': 1, 'sCost': 0, 'direction': -1,},
        
        ('UC5', 'TC1')  : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 3, 'Bmax': 3, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
        ('UC5', 'ITC1') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 4, 'Bmax': 4, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},
        ('UC5', 'TC1I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 2, 'Bmax': 2, 'Cost': 3, 'vCost': 1, 'sCost': 0, 'direction': -1,},
    },
}

FP_Network_1 = {
    # time grid
    'TIME':  range(0, FP_Network_1_Horizon+1),
    
    # states
    'STATES': {
        'RM'     : {'capacity': 450, 'initial': 100, 'price':  0, 'isRM': True, 'isIntermed': False, 'isProd': False},
        'IA1'    : {'capacity': 450, 'initial': 0, 'price': 10, 'isRM': False, 'isIntermed': True, 'isProd': False},       
        'IA2'    : {'capacity': 450, 'initial': 0, 'price': 10, 'isRM': False, 'isIntermed': True, 'isProd': False},       
        'P1'     : {'capacity': 450, 'initial': 0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},       
    },

    'STATES_SHIPMENT': {
        #('P1', 8) : {'demand':10},        
        #('P1', 10) : {'demand':25},        
    },
    
    # state-to-task arcs indexed by (state, task)
    'ST_ARCS': {
        ('RM', 'TA1') : {'rho': -1.0, 'direction': -1},
        
        ('RM', 'TA3')  : {'rho': -1.0, 'direction': -1},
        ('RM', 'ITA3') : {'rho': -0.25, 'direction': -1},
        ('RM', 'TA3I') : {'rho': -0.5, 'direction': -1},
        
        ('IA1', 'TC1')  : {'rho': -1.0, 'direction': -1},
        ('IA1', 'ITC1') : {'rho': -0.25, 'direction': -1},
        ('IA1', 'TC1I') : {'rho': -0.5, 'direction': -1},
        
        ('IA2', 'TC1')  : {'rho': -1.0, 'direction': -1},
        ('IA2', 'ITC1') : {'rho': -0.25, 'direction': -1},
        ('IA2', 'TC1I') : {'rho': -0.5, 'direction': -1},
    },
    
    # task-to-state arcs indexed by (task, state)
    'TS_ARCS': {
        ('TA1', 'IA1')  : {'rho': 1.0, 'direction': 1},
        ('TA3', 'IA2')  : {'rho': 1.0, 'direction': 1},
        ('ITA3', 'IA2') : {'rho': 0.25, 'direction': 1},
        ('TA3I', 'IA2') : {'rho': 0.5, 'direction': 1},
        
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
        ('UA1', 'TA1') : {'tau_min': 4, 'tau_max': 6, 'tau': 1, 'Bmin': 3.5, 'Bmax': 5, 'Cost': 4, 'vCost': 1, 'sCost': 40.5, 'direction': 1,},
        ('UA6', 'TA1') : {'tau_min': 3, 'tau_max': 5, 'tau': 1, 'Bmin': 4, 'Bmax': 6, 'Cost': 4, 'vCost': 1, 'sCost': 40.5, 'direction': 1,},
        
        ('UA2', 'TA3')  : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 2.1, 'Bmax': 3, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
        ('UA2', 'ITA3') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 2.8, 'Bmax': 4, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},
        ('UA2', 'TA3I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 1.4, 'Bmax': 2, 'Cost': 3, 'vCost': 1, 'sCost': 0, 'direction': -1,},
        
        ('UC5', 'TC1')  : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 6, 'Bmax': 8, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
        ('UC5', 'ITC1') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 4, 'Bmax': 4, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},
        ('UC5', 'TC1I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 2, 'Bmax': 2, 'Cost': 3, 'vCost': 1, 'sCost': 0, 'direction': -1,},
    },
}


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
        ('P1', 48) : {'demand':10},
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
        ('UA1', 'TA1') : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 3.5, 'Bmax': 5, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
        ('UA2', 'TA2') : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 2.1, 'Bmax': 3, 'Cost': 4, 'vCost': 1, 'sCost': 25, 'direction': 1,},
        
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
        ('UA1', 'TA1') : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 3.5, 'Bmax': 5, 'Cost': 4, 'vCost': 1, 'sCost': 0, 'direction': 1,},
        ('UA2', 'TA2') : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 2.1, 'Bmax': 3, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
        
        ('UA2', 'TA3')  : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 2.1, 'Bmax': 3, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
        ('UA2', 'ITA3') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 2.8, 'Bmax': 4, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},
        ('UA2', 'TA3I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 1.4, 'Bmax': 2, 'Cost': 3, 'vCost': 1, 'sCost': 0, 'direction': -1,},
        
        ('UC5', 'TC1')  : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 4, 'Bmax': 4, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
        ('UC5', 'ITC1') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 4, 'Bmax': 4, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},
        ('UC5', 'TC1I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 2, 'Bmax': 2, 'Cost': 3, 'vCost': 1, 'sCost': 0, 'direction': -1,},
    },
}



Network_2_Max = {
    # time grid
    'TIME':  range(0, H_Network_2_Max+1),
    
    # states
    'STATES': {
        'RM'     : {'capacity': 450, 'initial': 400, 'price':  0, 'isRM': True, 'isIntermed': False, 'isProd': False},
        'IA1'    : {'capacity': 450, 'initial': 0, 'price': 10, 'isRM': False, 'isIntermed': True, 'isProd': False},       
        'P1'     : {'capacity': 450, 'initial': 0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},       
    },

    'STATES_SHIPMENT': {        
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
        ('UA1', 'TA1') : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 1.5, 'Bmax': 2, 'Cost': 4, 'vCost': 1, 'sCost': 40.5, 'direction': 1,},
        ('UA2', 'TA2') : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 1.1, 'Bmax': 1.1, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
        
        ('UA2', 'TA3')  : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 1.1, 'Bmax': 2, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
        ('UA2', 'ITA3') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 0.8, 'Bmax': 1, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},
        ('UA2', 'TA3I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 0.4, 'Bmax': 1, 'Cost': 3, 'vCost': 1, 'sCost': 0, 'direction': -1,},
        
        ('UC5', 'TC1')  : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 5, 'Bmax': 5, 'Cost': 4, 'vCost': 1, 'sCost': 31.5, 'direction': 1,},
        ('UC5', 'ITC1') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 4, 'Bmax': 4, 'Cost': 6, 'vCost': 1, 'sCost': 0, 'direction': 1,},
        ('UC5', 'TC1I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 2, 'Bmax': 2, 'Cost': 3, 'vCost': 1, 'sCost': 0, 'direction': -1,},
    },
}



Network_test = {
    # time grid
    'TIME':  range(0, H_Network_test+1),
    
    # states
    'STATES': {
        'S1'     : {'capacity': 150, 'initial': 35, 'price':  0, 'isRM': True, 'isIntermed': False, 'isProd': False},
        'S2'     : {'capacity': 150, 'initial': 140, 'price':  0, 'isRM': True, 'isIntermed': False, 'isProd': False},       
        'S3'     : {'capacity': 150, 'initial': 0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
        'S4'     : {'capacity': 150, 'initial': 0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
        'S5'     : {'capacity': 150, 'initial': 0, 'price': 0, 'isRM': False, 'isIntermed': True, 'isProd': False},       
        'S6'     : {'capacity': 150, 'initial': 0, 'price': 1000, 'isRM': False, 'isIntermed': False, 'isProd': True},       
    },

    'STATES_SHIPMENT': {
        #('S3', 10) : {'demand':12},
        ('S6', 10) : {'demand':30},        
    },
    
    # state-to-task arcs indexed by (state, task)
    'ST_ARCS': {
        ('S1', 'T1') : {'rho': -1.0, 'direction': -1},
        ('S2', 'T2') : {'rho': -1.0, 'direction': -1},        
        ('S3', 'T3')  : {'rho': -1.0, 'direction': -1},
        ('S4', 'T4') : {'rho': -0.75, 'direction': -1},
        ('S5', 'T4') : {'rho': -0.25, 'direction': -1},
                
    },
    
    # task-to-state arcs indexed by (task, state)
    'TS_ARCS': {
        ('T1', 'S3')  : {'rho': 1.0, 'direction': 1},
        ('T2', 'S4')  : {'rho': 1.0, 'direction': 1},
        ('T3', 'S5')  : {'rho': 1.0, 'direction': 1},
        ('T4', 'S6')  : {'rho': 1.0, 'direction': 1},
        
    },
    
    # Tasks and their corresponding transition. 
    # Transition-To-Task = 1. Task-To-Transition = -1.
    # Equivalent to parameter ipits(i, ii) in the GAMS code.
    'TASKS_TRANSITION_TASKS': { 
        
    },
    
    # unit data indexed by (unit, task)
    'UNIT_TASKS': {
        ('U1', 'T1') : {'tau_min': 2, 'tau_max': 2, 'tau': 1, 'Bmin': 2.5, 'Bmax': 5, 'Cost': 4, 'vCost': 1, 'sCost': 10, 'direction': 1,},
        ('U2', 'T1') : {'tau_min': 3, 'tau_max': 3, 'tau': 1, 'Bmin': 0, 'Bmax': 1.66, 'Cost': 4, 'vCost': 1, 'sCost': 10, 'direction': 1,},
        ('U3', 'T3') : {'tau_min': 2, 'tau_max': 2, 'tau': 1, 'Bmin': 12.5, 'Bmax': 15, 'Cost': 4, 'vCost': 1, 'sCost': 10, 'direction': 1,},        
        ('U4', 'T2') : {'tau_min': 4, 'tau_max': 4, 'tau': 1, 'Bmin': 3.75, 'Bmax': 6.25, 'Cost': 4, 'vCost': 1, 'sCost': 10, 'direction': 1,},
        ('U4', 'T4') : {'tau_min': 2, 'tau_max': 2, 'tau': 1, 'Bmin': 7.5, 'Bmax': 12.5, 'Cost': 6, 'vCost': 1, 'sCost': 10, 'direction': 1,},
    },
}
