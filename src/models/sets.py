from pyomo.environ import *
import numpy as np 

def init_set_all_tasks(UNIT_TASKS):
    tasks = set()
    keys_unit_task = UNIT_TASKS.keys() 
    for unit, task in keys_unit_task:
        tasks.add(task)        
    return tasks
    
def init_set_all_units(UNIT_TASKS):
    units = set()
    keys_unit_task = UNIT_TASKS.keys() 
    for unit, task in keys_unit_task:
        units.add(unit)        
    return units
    
def init_set_units_executing_task(model, UNIT_TASKS):
    S_J_Executing_I = {task: set() for task in model.S_Tasks}
    keys_unit_task = UNIT_TASKS.keys()
    for unit, task in keys_unit_task:
        S_J_Executing_I[task].add(unit)
    return S_J_Executing_I

def init_set_materials(STATES):
    materials = set()
    keys_materials = STATES.keys()
    for material in keys_materials:
        materials.add(material)
    return materials

def init_task_unit_network(UNIT_TASKS):
    #Equivalent to ij.
    task_unit_network = {(i,j): UNIT_TASKS[(j,i)]['direction'] for (j,i) in UNIT_TASKS} 
    return task_unit_network

def init_task_transitions(TASKS_TRANSITION_TASKS):
    #Equivalent ipits.
    task_transitions = {(i,ii): TASKS_TRANSITION_TASKS[(i,ii)]['direction'] for (i,ii) in TASKS_TRANSITION_TASKS} 
    return task_transitions

def init_task_prod_consump(ST_ARCS, TS_ARCS):
    #Equivalent ik.
    P_TASKS_CONSUMP = {(i,k): -1 for (k,i) in ST_ARCS} 
    P_TASKS_PROD = {(i,k): 1 for (i,k) in TS_ARCS} 
    task_prod_consump = P_TASKS_CONSUMP | P_TASKS_PROD 
    return task_prod_consump

def init_task_transitions_unit(UNIT_TASKS, TASKS_TRANSITION_TASKS):
    #Equivalent to jii.
    P_TASKS_TRANSITIONS = {(i,ii): TASKS_TRANSITION_TASKS[(i,ii)]['direction'] for (i,ii) in TASKS_TRANSITION_TASKS} 
    P_TASK_UNIT = {(i,j): UNIT_TASKS[(j,i)]['direction'] for (j,i) in UNIT_TASKS} 
    task_transitions_unit = {(j,i,ii): P_TASKS_TRANSITIONS[i,ii] for (j,i) in UNIT_TASKS for (j,ii) in UNIT_TASKS if (i,j) in P_TASK_UNIT if (ii,j) in P_TASK_UNIT if (i,ii) in P_TASKS_TRANSITIONS}
    return task_transitions_unit

def init_set_tasks_in_units(model, UNIT_TASKS):
    S_I_In_J = {j: set() for j in model.S_Units}
    keys_unit_task = UNIT_TASKS.keys()
    for (unit,task) in keys_unit_task:
        S_I_In_J[unit].add(task)
    return S_I_In_J

def init_set_continuos_tasks(UNIT_TASKS):
    S_I_Continuos_Tasks = set([i for (j,i) in UNIT_TASKS])
    return S_I_Continuos_Tasks

def init_set_production_tasks(model, UNIT_TASKS, TASKS_TRANSITION_TASKS):
    #Equivalent to ip.
    S_I_Production_Tasks = set([i for (j,i) in UNIT_TASKS if all ((ii,i) not in TASKS_TRANSITION_TASKS for ii in model.S_Tasks)]) 
    return S_I_Production_Tasks

def init_set_tasks_consuming_material(STATES, ST_ARCS):
    S_I_CONSUMING_K = {k: set() for k in STATES}
    for (k,i) in ST_ARCS:
        S_I_CONSUMING_K[k].add(i)
    return S_I_CONSUMING_K

def init_set_tasks_producing_material(STATES, TS_ARCS):
    S_I_PRODUCING_K = {k: set() for k in STATES}
    for (i,k) in TS_ARCS:
        S_I_PRODUCING_K[k].add(i)
    return S_I_PRODUCING_K    

def init_set_materials_produced_task(model, TS_ARCS):
    S_K_PRODUCED_BY_I = {i: set() for i in model.S_Tasks} 
    for (i,k) in TS_ARCS:
        S_K_PRODUCED_BY_I[i].add(k)
    return S_K_PRODUCED_BY_I

def init_set_materials_consumed_task(model, ST_ARCS):
    S_K_CONSUMED_BY_I = {i: set() for i in model.S_Tasks} 
    for (k,i) in ST_ARCS:
        S_K_CONSUMED_BY_I[i].add(k)
    return S_K_CONSUMED_BY_I  

def init_set_production_tasks_with_transitions(TASKS_TRANSITION_TASKS):
    S_I_Production_Tasks_With_Transition = set([i for (i,ii) in TASKS_TRANSITION_TASKS]) 
    return S_I_Production_Tasks_With_Transition

def init_set_all_transitions(TASKS_TRANSITION_TASKS):
    S_I_All_Transition_Tasks = set([ii for (i,ii) in TASKS_TRANSITION_TASKS]) 
    return S_I_All_Transition_Tasks

def init_set_production_tasks_without_transition(model):
    #Equivalent to ictsnt.
    S_I_Production_Tasks_Without_Transition = model.S_Tasks - model.S_I_Production_Tasks_With_Transition - model.S_I_All_Transition_Tasks 
    return S_I_Production_Tasks_Without_Transition

def init_set_direct_transition_tasks(TASKS_TRANSITION_TASKS):
    #Equivalent to i_ts_d.
    S_I_Direct_Transition_Tasks = set([i for (ii,i) in TASKS_TRANSITION_TASKS if (TASKS_TRANSITION_TASKS[(ii,i)]['isDirect'] == True)]) 
    return S_I_Direct_Transition_Tasks

def init_set_indirect_transition_tasks(TASKS_TRANSITION_TASKS):
    #Equivalent to i_ts_i.
    S_I_Indirect_Transition_Tasks = set([i for (ii,i) in TASKS_TRANSITION_TASKS if (TASKS_TRANSITION_TASKS[(ii,i)]['isDirect'] == False)]) 
    return S_I_Indirect_Transition_Tasks

def init_set_startup_tasks(TASKS_TRANSITION_TASKS):
    #Equivalent to i_ts_su.
    S_I_Startup_Tasks = set([i for (ii,i) in TASKS_TRANSITION_TASKS if (TASKS_TRANSITION_TASKS[(ii,i)]['isDirect'] == False and TASKS_TRANSITION_TASKS[(ii,i)]['isSU'] == True) ]) 
    return S_I_Startup_Tasks

def init_set_shutdown_tasks(TASKS_TRANSITION_TASKS):
    #Equivalent to i_ts_su.
    S_I_Shutdown_Tasks = set([i for (ii,i) in TASKS_TRANSITION_TASKS if (TASKS_TRANSITION_TASKS[(ii,i)]['isDirect'] == False and TASKS_TRANSITION_TASKS[(ii,i)]['isSD'] == True) ]) 
    return S_I_Shutdown_Tasks

def init_set_production_tasks_with_direct_transition(TASKS_TRANSITION_TASKS):
    #Equivalent to ip_d.
    S_I_Production_Tasks_With_Direct_Transition = set([i for (i,ii) in TASKS_TRANSITION_TASKS if (TASKS_TRANSITION_TASKS[(i,ii)]['isDirect'] == True)]) 
    return S_I_Production_Tasks_With_Direct_Transition

def init_set_production_tasks_with_indirect_transition(TASKS_TRANSITION_TASKS):
    #Equivalent to ip_i.
    S_I_Production_Tasks_With_Indirect_Transition = set([i for (i,ii) in TASKS_TRANSITION_TASKS if (TASKS_TRANSITION_TASKS[(i,ii)]['isDirect'] == False)]) 
    return S_I_Production_Tasks_With_Indirect_Transition

def init_set_units_with_direct_transition_tasks(model, UNIT_TASKS):
    #Equivalent to j_d.
    S_J_Units_With_Direct_Transition_Tasks = set([j for (j,i) in UNIT_TASKS if i in model.S_I_Production_Tasks_With_Direct_Transition]) 
    return S_J_Units_With_Direct_Transition_Tasks

def init_set_units_with_shutdown_tasks(model, UNIT_TASKS):
    #Equivalent to j_i.
    S_J_Units_With_Shutdown_Tasks = set([j for (j,i) in UNIT_TASKS if i in model.S_I_Indirect_Transition_Tasks]) 
    return S_J_Units_With_Shutdown_Tasks

def init_set_units_without_transition_tasks(model):
    #Equivalent to j_c.
    #S_J_Units_Without_Transition_Tasks = model.S_Units - model.S_J_Units_With_Direct_Transition_Tasks - model.S_J_Units_With_Shutdown_Tasks 
    return (model.S_Units - model.S_J_Units_With_Direct_Transition_Tasks - model.S_J_Units_With_Shutdown_Tasks)

def init_set_raw_material(STATES):
    S_K_RawMaterials = set([k for k in STATES if STATES[k]['isRM'] == True])    
    return S_K_RawMaterials

def init_set_final_products(STATES):
    #Equivalent rmp.
    S_K_Final_Products = set([k for k in STATES if STATES[k]['isProd'] == True])
    return S_K_Final_Products

def init_set_intermidiates(STATES):
    #Equivalent rmi.
    S_K_Intermediates = set([k for k in STATES if STATES[k]['isIntermed'] == True])
    return S_K_Intermediates

def _init_set_utilities(UTILITIES):
    utilities = set()
    keys_utilities = UTILITIES.keys()
    for utility in keys_utilities:
        utilities.add(utility)
    return utilities

def _init_set_tasks_consuming_utilities(UTILITIES, TASKS_UTILITIES):
    S_I_CONSUMING_U = {u: set() for u in UTILITIES}
    for (i,u) in TASKS_UTILITIES:
        S_I_CONSUMING_U[u].add(i)
    return S_I_CONSUMING_U


def create_main_sets_parameters(model, STN, H):
    
    STATES = STN['STATES']
    ST_ARCS = STN['ST_ARCS']
    TS_ARCS = STN['TS_ARCS']
    UNIT_TASKS = STN['UNIT_TASKS']
    TASKS_TRANSITION_TASKS = STN['TASKS_TRANSITION_TASKS']
    UTILITIES = STN['UTILITIES']
    TASKS_UTILITIES = STN['TASKS_UTILITIES']
    
    model.S_Tasks = Set(initialize = init_set_all_tasks(UNIT_TASKS))
    model.S_Units = Set(initialize = init_set_all_units(UNIT_TASKS))
    model.S_Time = Set(initialize = np.array(range(0, H+1)))
    model.S_Materials = Set(initialize = init_set_materials(STATES))    
    model.S_J_Executing_I = Set(model.S_Tasks, initialize = init_set_units_executing_task(model, UNIT_TASKS))
    model.S_I_In_J = Set(model.S_Units, initialize = init_set_tasks_in_units(model, UNIT_TASKS))    
    model.S_I_Continuos_Tasks = Set(initialize = init_set_continuos_tasks(UNIT_TASKS))
    model.S_I_Production_Tasks = Set(initialize = init_set_production_tasks(model, UNIT_TASKS, TASKS_TRANSITION_TASKS))    
    model.S_I_Consuming_K = Set(model.S_Materials, initialize = init_set_tasks_consuming_material(STATES, ST_ARCS))    
    model.S_I_Producing_K = Set(model.S_Materials, initialize = init_set_tasks_producing_material(STATES, TS_ARCS))    
    model.S_K_Produced_I = Set(model.S_Tasks, initialize = init_set_materials_produced_task(model, TS_ARCS))
    model.S_K_Consumed_I = Set(model.S_Tasks, initialize = init_set_materials_consumed_task(model, ST_ARCS))    
    model.S_I_Production_Tasks_With_Transition = Set(initialize = init_set_production_tasks_with_transitions(TASKS_TRANSITION_TASKS))
    model.S_I_Production_Tasks_With_Direct_Transition = Set(initialize = init_set_production_tasks_with_direct_transition(TASKS_TRANSITION_TASKS)) 
    model.S_I_Production_Tasks_With_Indirect_Transition = Set(initialize = init_set_production_tasks_with_indirect_transition(TASKS_TRANSITION_TASKS))
    model.S_I_All_Transition_Tasks = Set(initialize = init_set_all_transitions(TASKS_TRANSITION_TASKS))
    model.S_I_Production_Tasks_Without_Transition = Set(initialize = init_set_production_tasks_without_transition(model))
    model.S_I_Direct_Transition_Tasks = Set(initialize = init_set_direct_transition_tasks(TASKS_TRANSITION_TASKS))
    model.S_I_Indirect_Transition_Tasks = Set(initialize = init_set_indirect_transition_tasks(TASKS_TRANSITION_TASKS))
    model.S_I_Startup_Tasks = Set(initialize = init_set_startup_tasks(TASKS_TRANSITION_TASKS))
    model.S_I_Shutdown_Tasks = Set(initialize = init_set_shutdown_tasks(TASKS_TRANSITION_TASKS))
    
    model.S_J_Units_With_Direct_Transition_Tasks = Set(initialize = init_set_units_with_direct_transition_tasks(model, UNIT_TASKS))  
    model.S_J_Units_With_Shutdown_Tasks = Set(initialize = init_set_units_with_shutdown_tasks(model, UNIT_TASKS))  
    model.S_J_Units_Without_Transition_Tasks = Set(initialize = init_set_units_without_transition_tasks(model))
    model.S_Raw_Materials = Set(initialize = init_set_raw_material(STATES))
    model.S_Final_Products = Set(initialize = init_set_final_products(STATES)) 
    model.S_Intermediates = Set(initialize = init_set_intermidiates(STATES)) 
    
    model.P_Task_Unit_Network = Param(model.S_Tasks, model.S_Units, initialize = init_task_unit_network(UNIT_TASKS))
    model.P_Task_Transitions = Param(model.S_Tasks, model.S_Tasks, initialize = init_task_transitions(TASKS_TRANSITION_TASKS))
    model.P_Task_Production_Comsumption = Param(model.S_Tasks, model.S_Materials, initialize = init_task_prod_consump(ST_ARCS, TS_ARCS))
    model.P_Task_Transitions_Unit = Param(model.S_Units, model.S_Tasks, model.S_Tasks, initialize = init_task_transitions_unit(UNIT_TASKS, TASKS_TRANSITION_TASKS))      

    model.S_Utilities = Set(initialize = _init_set_utilities(UTILITIES))
    model.S_I_Consuming_U = Set(model.S_Utilities, initialize = _init_set_tasks_consuming_utilities(UTILITIES, TASKS_UTILITIES))
    
"""     print(f"S_Tasks: {model.S_Tasks.data()}")
    print(f"S_Units: {model.S_Units.data()}")
    print(f"S_Time: {model.S_Time.data()}")
    print(f"S_Materials: {model.S_Materials.data()}") 
    print(f"S_J_Executing_I: {model.S_J_Executing_I.data()}")
    print(f"S_I_In_J: {model.S_I_In_J.data()}")   
    print(f"S_I_Continuos_Tasks: {model.S_I_Continuos_Tasks.data()}")
    print(f"S_I_Production_Tasks: {model.S_I_Production_Tasks.data()}")    
    print(f"S_I_Consuming_K: {model.S_I_Consuming_K.data()}") 
    print(f"S_I_Producing_K: {model.S_I_Producing_K.data()}") 
    print(f"S_K_Produced_I: {model.S_K_Produced_I.data()}")
    print(f"S_K_Consumed_I: {model.S_K_Consumed_I.data()}")
    print(f"S_I_Production_Tasks_With_Transition: {model.S_I_Production_Tasks_With_Transition.data()}")
    print(f"S_I_Production_Tasks_With_Direct_Transition: {model.S_I_Production_Tasks_With_Direct_Transition.data()}") 
    print(f"S_I_Production_Tasks_With_Indirect_Transition: {model.S_I_Production_Tasks_With_Indirect_Transition.data()}")
    print(f"S_I_All_Transition_Tasks: {model.S_I_All_Transition_Tasks.data()}")
    print(f"S_I_Production_Tasks_Without_Transition: {model.S_I_Production_Tasks_Without_Transition.data()}")
    print(f"S_I_Direct_Transition_Tasks: {model.S_I_Direct_Transition_Tasks.data()}")
    print(f"S_I_Indirect_Transition_Tasks: {model.S_I_Indirect_Transition_Tasks.data()}")
    print(f"S_I_Startup_Tasks: {model.S_I_Startup_Tasks.data()}")
    print(f"S_I_Shutdown_Tasks: {model.S_I_Shutdown_Tasks.data()}")
    print(f"S_J_Units_With_Direct_Transition_Tasks: {model.S_J_Units_With_Direct_Transition_Tasks.data()}") 
    print(f"S_J_Units_With_Shutdown_Tasks: {model.S_J_Units_With_Shutdown_Tasks.data()}") 
    print(f"S_J_Units_Without_Transition_Tasks: {model.S_J_Units_Without_Transition_Tasks.data()}")
    print(f"S_Raw_Materials: {model.S_Raw_Materials.data()}")
    print(f"S_Final_Products: {model.S_Final_Products.data()}") 
    print(f"S_Intermediates: {model.S_Intermediates.data()}")
    print(f"S_Utilities: {model.S_Utilities.data()}") 
    print(f"S_I_Consuming_U: {model.S_I_Consuming_U.data()}")
    
    model.P_Task_Unit_Network.pprint()
    model.P_Task_Transitions.pprint()
    model.P_Task_Production_Comsumption.pprint() 
    model.P_Task_Transitions_Unit.pprint() """ 