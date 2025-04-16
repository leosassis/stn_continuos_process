from pyomo.environ import *
from itertools import product
from numpy import ceil
from src.utils.utils import print_dict

INITIAL_SHIFT = 1  # Initial shift of a consuming task in case the methods calculates that it should start before the start of the producing task
SHIFT_TO_END_RUN = 1  # Shift to reach the end of a consuming task run


def materials_to_be_explored(STN: dict) -> list:
    """ 
    Return an ordered list of materials to be explored.
    """
    
    STATES = STN['STATES']
    intermediate_materials = {k: v for k, v in STATES.items() if v['isIntermed']}
        
    return sorted(intermediate_materials.keys(), key=lambda k: intermediate_materials[k]['order'])


def get_production_relationship(model: ConcreteModel, i_producing: Any, j_producing: Any, ii_consuming: Any, jj_consuming: Any) -> int:
    """ 
    Computes the production relationship between a consuming task ii_consuming and a producing task i_producing.
    """
    
    numerator = model.P_Tau_Min[ii_consuming,jj_consuming] * model.P_Beta_Min[ii_consuming,jj_consuming]
    denominator = model.P_Tau_Max[i_producing, j_producing] * model.P_Beta_Max[i_producing, j_producing]
    
    return numerator/denominator


def get_number_periods(model: ConcreteModel, i_producing: Any, j_producing: Any, ii_consuming: Any, jj_consuming: Any, production_relationship: dict) -> int:
    """ 
    Computes the number of periods necessary for task i_producing to produce enough material to start a run of task ii_consuming.
    """
    
    rel = production_relationship[i_producing, j_producing, ii_consuming, jj_consuming]
    tau_max = model.P_Tau_Max[i_producing,j_producing]
    tau_end = model.P_Tau_End_Task[i_producing]
    
    return ceil(rel * tau_max) + ceil(rel * tau_end) - tau_end


def get_est(model: ConcreteModel, i_producing: Any, j_producing: Any, ii_consuming: Any, jj_consuming: Any, number_periods: dict, est_task: dict) -> int:
    """ 
    Computes the est of consuming task ii_consuming based on the est of the producing task i_producing, the production relationship and the number of periods.
    """
    
    est_prod_task = est_task[j_producing, i_producing]
    num_periods = number_periods[i_producing, j_producing, ii_consuming, jj_consuming]
    tau_min_consuming_task = model.P_Tau_Min[ii_consuming, jj_consuming]
    
    return max(est_prod_task + INITIAL_SHIFT, est_prod_task + num_periods + SHIFT_TO_END_RUN - tau_min_consuming_task)


def compute_est(model: ConcreteModel, STN: dict) -> None:
    """ 
    Computes the est for all tasks in the STN network.
    The while loop goes through the ordered set of intermediate materials and computes the est of the consuming task, assuming as 0 the est of tasks connected to raw materials. 
    Updates the STN dictionary with 'EST_ST', a mapping of (j,i) -> est value.
    """
    
    unit_task = STN['UNIT_TASKS']
    materials_to_explore = materials_to_be_explored(STN)
    
    production_relationship = {}
    number_periods = {}
    est_task = {(j,i): 0 for (j,i) in unit_task} 
    
    while materials_to_explore:
        
        k = materials_to_explore.pop(0)
               
        for i_producing, ii_consuming in product(model.S_I_Producing_K[k], model.S_I_Consuming_K[k]):
                
            j_producing = next(iter(model.S_J_Executing_I[i_producing]))
            jj_consuming = next(iter(model.S_J_Executing_I[ii_consuming]))
            
            key = (i_producing, j_producing, ii_consuming, jj_consuming)
                
            production_relationship[key] = get_production_relationship(model, *key)
            number_periods[key] = get_number_periods(model, *key, production_relationship) 
            est_task[jj_consuming, ii_consuming] = get_est(model, *key, number_periods, est_task) 
    
    STN['EST_ST'] = est_task    
    
    #print_dict(production_relationship)
    #print_dict(number_periods)
    print_dict(est_task)