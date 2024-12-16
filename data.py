H_Network_0 = 10

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
        ('P1', 10) : {'demand':12},
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
        ('UA1', 'TA1') : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 3.5, 'Bmax': 5, 'Cost': 4, 'vCost': 1, 'direction': 1,},
        ('UA2', 'TA2') : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 2.1, 'Bmax': 3, 'Cost': 1, 'vCost': 1, 'direction': 1,},
        
        ('UA2', 'TA3')  : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 2.1, 'Bmax': 3, 'Cost': 4, 'vCost': 1, 'direction': 1,},
        ('UA2', 'ITA3') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 2.8, 'Bmax': 4, 'Cost': 6, 'vCost': 1, 'direction': 1,},
        ('UA2', 'TA3I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 1.4, 'Bmax': 2, 'Cost': 3, 'vCost': 1, 'direction': -1,},
        
        ('UC5', 'TC1')  : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 3, 'Bmax': 3, 'Cost': 4, 'vCost': 1, 'direction': 1,},
        ('UC5', 'ITC1') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 4, 'Bmax': 4, 'Cost': 6, 'vCost': 1, 'direction': 1,},
        ('UC5', 'TC1I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 2, 'Bmax': 2, 'Cost': 3, 'vCost': 1, 'direction': -1,},
    },
}

H_Network_1 = 10

Network_1 = {
    # time grid
    'TIME':  range(0, H_Network_1+1),
    
    # states
    'STATES': {
        'RM'     : {'capacity': 450, 'initial': 400, 'price':  0, 'isRM': True, 'isIntermed': False, 'isProd': False},
        'I1'      : {'capacity': 450, 'initial':  30, 'price': 10, 'isRM': False, 'isIntermed': True, 'isProd': False},       
        'P1'      : {'capacity': 450, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},       
        'P2'      : {'capacity': 450, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},       
    },

    'STATES_SHIPMENT': {
        #('P1', 14) : {'demand':30},
        #('P2', 14) : {'demand':10},
    },
    
    # state-to-task arcs indexed by (state, task)
    'ST_ARCS': {
        ('RM', 'TA1_1') : {'rho': -1.0},
        ('RM', 'TB1_1') : {'rho': -1.0},
        ('RM', 'TC1_2') : {'rho': -1.0},
        ('RM', 'TC1I')  : {'rho': -1.0},
        ('RM', 'ITC1')  : {'rho': -1.0},
    
        ('I1', 'TD1_3') : {'rho': -1.0},
        ('I1', 'TD2_3') : {'rho': -1.0},
    
        ('I1', 'TD1I') : {'rho': -1.0},
        ('I1', 'ITD1') : {'rho': -1.0},
    
        ('I1', 'TD2I') : {'rho': -1.0},
        ('I1', 'ITD2') : {'rho': -1.0},
    
        ('I1', 'DTD1TD2') : {'rho': -1.0},
        ('I1', 'DTD2TD1') : {'rho': -1.0},
    },
    
    # task-to-state arcs indexed by (task, state)
    'TS_ARCS': {
        ('TA1_1', 'I1') : {'rho': 1.0, 'prod_consump': 1},
        ('TB1_1', 'I1') : {'rho': 1.0, 'prod_consump': 1},
        ('TC1_2', 'I1') : {'rho': 1.0, 'prod_consump': 1},
        ('ITC1', 'I1')   : {'rho': 0.25, 'prod_consump': 1},
        ('TC1I', 'I1')   : {'rho': 0.5, 'prod_consump': 1},
        
        ('TD1_3', 'P1') : {'rho': 1.0, 'prod_consump': 1},
        ('TD2_3', 'P2') : {'rho': 1.0, 'prod_consump': 1},
        
        ('TD1I', 'P1')   : {'rho': 0.25, 'prod_consump': 1},
        ('ITD1', 'P1')   : {'rho': 0.5, 'prod_consump': 1},
       
        ('TD2I', 'P2') : {'rho': 1.0, 'prod_consump': 1},
        ('ITD2', 'P2') : {'rho': 1.0, 'prod_consump': 1},
        
        ('DTD1TD2', 'P2')   : {'rho': 0.25, 'prod_consump': 1},
        ('DTD2TD1', 'P1')   : {'rho': 0.5, 'prod_consump': 1},

    },
    
    # Tasks and their corresponding transition. 
    # Transition-To-Task = 1. Task-To-Transition = -1.
    # Equivalent to parameter ipits(i, ii) in the GAMS code.
    'TASKS_TRANSITION_TASKS': { 
        ('TC1_2', 'ITC1') : {'isSU': True, 'isSD': False, 'isDirect': False, 'direction': 1},
        ('TC1_2', 'TC1I') : {'isSU': False, 'isSD': True, 'isDirect': False, 'direction': -1},
        
        ('TD1_3', 'ITD1')   : {'isSU': True, 'isSD': False, 'isDirect': False, 'direction': 1},
        ('TD1_3', 'TD1I')   : {'isSU': False, 'isSD': True, 'isDirect': False, 'direction': -1},
        
        ('TD2_3', 'ITD2') : {'isSU': True, 'isSD': False, 'isDirect': False, 'direction': 1},
        ('TD2_3', 'TD2I') : {'isSU': False, 'isSD': True, 'isDirect': False, 'direction': -1},
                
        ('TD1_3', 'DTD2TD1')   : {'isSU': False, 'isSD': False, 'isDirect': True, 'direction': 1},
        ('TD1_3', 'DTD1TD2')   : {'isSU': False, 'isSD': False, 'isDirect': True, 'direction': -1},
        
        ('TD2_3', 'DTD1TD2')   : {'isSU': False, 'isSD': False, 'isDirect': True, 'direction': 1},
        ('TD2_3', 'DTD2TD1')   : {'isSU': False, 'isSD': False, 'isDirect': True, 'direction': -1},
    },
    
    # unit data indexed by (unit, task)
    'UNIT_TASKS': {
        ('U1', 'TA1_1') : {'tau_min': 3, 'tau_max': 4, 'tau': 1, 'Bmin': 10, 'Bmax': 10, 'Cost': 4, 'vCost': 1, 'direction': 1,},
        ('U1', 'TB1_1') : {'tau_min': 3, 'tau_max': 5, 'tau': 1, 'Bmin': 6, 'Bmax': 7, 'Cost': 2, 'vCost': 1, 'direction': 1,},
        ('U2', 'TC1_2') : {'tau_min': 3, 'tau_max': 4, 'tau': 1, 'Bmin': 6, 'Bmax': 6, 'Cost': 1, 'vCost': 1, 'direction': 1,},
        ('U3', 'TD1_3') : {'tau_min': 3, 'tau_max': 5, 'tau': 1, 'Bmin': 6, 'Bmax': 7, 'Cost': 2, 'vCost': 1, 'direction': 1,},
        ('U3', 'TD2_3') : {'tau_min': 3, 'tau_max': 4, 'tau': 1, 'Bmin': 6, 'Bmax': 6, 'Cost': 1, 'vCost': 1, 'direction': 1,},
        
        ('U2', 'ITC1')     : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 2.8, 'Bmax': 2.8, 'Cost': 1, 'vCost': 1, 'direction': 1,},
        ('U2', 'TC1I')     : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 1.4, 'Bmax': 1.4, 'Cost': 1, 'vCost': 1, 'direction': -1,},
    
        ('U3', 'ITD1')     : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 2.8, 'Bmax': 2.8, 'Cost': 1, 'vCost': 1, 'direction': 1,},
        ('U3', 'TD1I')     : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 1.4, 'Bmax': 1.4, 'Cost': 1, 'vCost': 1, 'direction': -1,},
            
        ('U3', 'ITD2')     : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 2.8, 'Bmax': 2.8, 'Cost': 1, 'vCost': 1, 'direction': 1,},
        ('U3', 'TD2I')     : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 1.4, 'Bmax': 1.4, 'Cost': 1, 'vCost': 1, 'direction': -1,},
            
        ('U3', 'DTD1TD2')     : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 2.8, 'Bmax': 2.8, 'Cost': 1, 'vCost': 1, 'direction': 1,},
        ('U3', 'DTD2TD1')     : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 1.4, 'Bmax': 1.4, 'Cost': 1, 'vCost': 1, 'direction': 1,},    
    
    },
}

H_Network_2 = 10

Network_2 = {
    # time grid
    'TIME':  range(0, H_Network_2+1),
    
    # states
    'STATES': {
        'RM'     : {'capacity': 10000, 'initial': 200, 'price':  0, 'isRM': True, 'isIntermed': False, 'isProd': False},
        'IA1'    : {'capacity': 500, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},
        'IA2'    : {'capacity': 500, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},
        'IA3'    : {'capacity': 500, 'initial':   0, 'price': 10, 'isRM': False, 'isIntermed': False, 'isProd': True},
    },

    'STATES_SHIPMENT': {
        ('IA1', 10) : {'demand': 15.0},
    },
    
    # state-to-task arcs indexed by (state, task)
    'ST_ARCS': {
        ('RM', 'TA1') : {'rho': -1.0},
        ('RM', 'TA2') : {'rho': -1.0},
        ('RM', 'TA3') : {'rho': -1.0},
        ('RM', 'TA3I') : {'rho': -1.0},
        ('RM', 'ITA3') : {'rho': -1.0},
    },
    
    # task-to-state arcs indexed by (task, state)
    'TS_ARCS': {
        ('TA1', 'IA1') : {'dur': 1, 'rho': 1.0, 'prod_consump': 1},
        ('TA2', 'IA2') : {'dur': 1, 'rho': 1.0, 'prod_consump': 1},
        ('TA3', 'IA3') : {'dur': 1, 'rho': 1.0, 'prod_consump': 1},
        ('ITA3', 'IA3') : {'dur': 2, 'rho': 0.25, 'prod_consump': 1},
        ('TA3I', 'IA3') : {'dur': 1, 'rho': 0.5, 'prod_consump': 1},
    },
    
    # Tasks and their corresponding transition. 
    # Transition-To-Task = 1. Task-To-Transition = -1.
    # Equivalent to parameter ipits(i, ii) in the GAMS code.
    'TASKS_TRANSITION_TASKS': {
        ('TA3', 'ITA3') : {'isSU': True, 'isSD': False, 'isDirect': False, 'direction': 1},
        ('TA3', 'TA3I') : {'isSU': False, 'isSD': True, 'isDirect': False, 'direction': -1},
    },
    
    # unit data indexed by (unit, task)
    'UNIT_TASKS': {
        ('UA1', 'TA1') : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 3.5, 'Bmax': 3.5, 'Cost': 4, 'vCost': 1, 'direction': 1,},
        ('UA2', 'TA2') : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 2.1, 'Bmax': 2.1, 'Cost': 4, 'vCost': 1, 'direction': 1,},
        ('UA2', 'TA3') : {'tau_min': 5, 'tau_max': 6, 'tau': 1, 'Bmin': 2.1, 'Bmax': 2.1, 'Cost': 4, 'vCost': 1, 'direction': 1,},
        ('UA2', 'ITA3') : {'tau_min': 0, 'tau_max': 0, 'tau': 2, 'Bmin': 2.8, 'Bmax': 2.8, 'Cost': 6, 'vCost': 1, 'direction': 1,},
        ('UA2', 'TA3I') : {'tau_min': 0, 'tau_max': 0, 'tau': 1, 'Bmin': 1.4, 'Bmax': 1.4, 'Cost': 3, 'vCost': 1, 'direction': -1,},
    },
}