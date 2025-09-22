from pyomo.environ import *
from itertools import product
from numpy import ceil
from collections import defaultdict
from src.methods.est import _materials_to_be_explored, INITIAL_SHIFT, SHIFT_TO_END_RUN


def _return_set_of_units_consuming_material(model: ConcreteModel, material: Any) -> int:
    """ 
    Creates a set with all units executing the consuming tasks and returns its length.    
    """
    
    set_consuming_units = set()
    
    for i_consuming in model.S_I_Consuming_K[[material]]:
                
        j_consuming = next(iter(model.S_J_Executing_I[i_consuming]))    
                
        set_consuming_units.add(j_consuming)
        
    return len(set_consuming_units)


def _compute_group_production_relationship(model: ConcreteModel, i_producing: Any, j_producing, material: Any) -> int:
    """ 
    Computes the production relationship between a consuming tasks and a producing task i_producing.
    """
    
    numerator = sum(model.P_Tau_Min[ii_consuming,jj_consuming] * model.P_Beta_Min[ii_consuming,jj_consuming] for ii_consuming in model.S_I_Consuming_K[material] for jj_consuming in model.S_J_Executing_I[ii_consuming])
    denominator = model.P_Tau_Max[i_producing, j_producing] * model.P_Beta_Max[i_producing, j_producing]
                
    return numerator/denominator
        
        
def _compute_group_number_periods(model: ConcreteModel, i_producing: Any, j_producing: Any, rel_group: int) -> int:
    """ 
    Computes the number of periods necessary for task i_producing to produce enough material to start runs of all consuming tasks.
    """
    
    tau_max = model.P_Tau_Max[i_producing,j_producing]
    tau_end = model.P_Tau_End_Task[i_producing]
    
    return ceil(rel_group * tau_max) + ceil(rel_group * tau_end) - tau_end


def _compute_est_group(model: ConcreteModel, est_task: dict, j_producing: Any, i_producing: Any, material, number_periods_group: int) -> dict:
    """ 
    Computes the est of each consuming task ii_consuming based on the est of the producing task i_producing, the production relationship and the number of periods.
    """
    
    est_task_group = {}
   
    for ii_consuming in model.S_I_Consuming_K[[material]]:
                    
        jj_consuming = next(iter(model.S_J_Executing_I[ii_consuming]))
                    
        est_prod_task = est_task[j_producing, i_producing]
        tau_min_consuming_task = model.P_Tau_Min[ii_consuming, jj_consuming]
    
        est_task_group[material, jj_consuming, ii_consuming] = max(est_prod_task + INITIAL_SHIFT, est_prod_task + number_periods_group + SHIFT_TO_END_RUN - tau_min_consuming_task) 
    
    return est_task_group


def compute_est_group_tasks(model: ConcreteModel, stn: dict) -> None:
    """ 
    Firt, it identifies groups of tasks consuming material k where all of them are in different units. 
    Then, it computes the groups's est where tasks can operate simultaneously.
    Finally, it stores the value in stn['EST_GROUP'].
    
    """
        
    unit_task = stn['UNIT_TASKS']
    states = stn['STATES']
    materials_to_explore = _materials_to_be_explored(stn)
    est_task = stn['EST']
    
    est_each_task_group = {(k,j,i): 0 for (j,i) in unit_task for k in states} 
    est_group = {(k): 0 for k in states} 
        
    while materials_to_explore:
            
        first_material_list = materials_to_explore.pop(0)
        number_material_producing_tasks = len(model.S_I_Producing_K[first_material_list])
        number_material_consuming_tasks = len(model.S_I_Consuming_K[first_material_list])
        number_material_consuming_units = _return_set_of_units_consuming_material(model, first_material_list)    
        
        if (number_material_producing_tasks == 1 and 
            number_material_consuming_tasks > 1 and            
            number_material_consuming_units == number_material_consuming_tasks):
                
            i_producing = next(iter(model.S_I_Producing_K[first_material_list]))
            j_producing = next(iter(model.S_J_Executing_I[i_producing])) 
                
            rel_group = _compute_group_production_relationship(model, i_producing, j_producing, first_material_list) 
            number_periods_group = _compute_group_number_periods(model, i_producing, j_producing, rel_group)
            est_each_task_group = _compute_est_group(model, est_task, j_producing, i_producing, first_material_list, number_periods_group)
                        
            max_est_group = defaultdict(lambda: float('-inf'))
            
            for (first_material_list, jj_consuming, ii_consuming), value in est_each_task_group.items():
                max_est_group[first_material_list] = max(max_est_group[first_material_list], value)
            
            est_group[first_material_list] = dict(max_est_group)[first_material_list]
    
    stn['EST_GROUP'] = est_group 