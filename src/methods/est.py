from pyomo.environ import *
from itertools import product


INITIAL_SHIFT = 1
SHIFT_TO_END_RUN = 1


def materials_to_be_explored(STN: dict) -> set:
    STATES = STN['STATES']
    S_SubSet_Materials = S_SubSet_Materials = {k: v for k, v in STATES.items() if v['isIntermed']}
    S_Material_To_Be_Explored = sorted(S_SubSet_Materials.keys(), key=lambda k: S_SubSet_Materials[k]['order'])
    
    return S_Material_To_Be_Explored


def get_production_relationship(model: ConcreteModel, i_producing: Any, j_producing: Any, ii_consuming: Any, jj_consuming: Any) -> int:
    
    return (model.P_Tau_Min[ii_consuming,jj_consuming]*model.P_Beta_Min[ii_consuming,jj_consuming]) / (model.P_Tau_Max[i_producing, j_producing] * model.P_Beta_Max[i_producing, j_producing])


def get_number_periods(model: ConcreteModel, i_producing: Any, j_producing: Any, ii_consuming: Any, jj_consuming: Any, production_relationship: dict) -> int:
    
    return ( ceil(production_relationship[i_producing, j_producing, ii_consuming, jj_consuming] * model.P_Tau_Max[i_producing,j_producing]) 
           + ceil(production_relationship[i_producing, j_producing, ii_consuming, jj_consuming] * model.P_Tau_End_Task[i_producing]) - model.P_Tau_End_Task[i_producing])


def get_est(model: ConcreteModel, i_producing: Any, j_producing: Any, ii_consuming: Any, jj_consuming: Any, number_periods: dict, est_task: dict) -> int:

    return (max(est_task[j_producing, i_producing] + INITIAL_SHIFT, 
                est_task[j_producing, i_producing] + number_periods[i_producing, j_producing, ii_consuming, jj_consuming] + SHIFT_TO_END_RUN - model.P_Tau_Min[ii_consuming, jj_consuming]))


def compute_est_cuts(model: ConcreteModel, STN: dict):
    UNIT_TASKS = STN['UNIT_TASKS']
    S_Material_To_Be_Explored = materials_to_be_explored(STN)
    
    production_relationship = {}
    number_periods = {}
    est_task = {(j,i): 0 for (j,i) in UNIT_TASKS} 
    print(est_task) 
    while S_Material_To_Be_Explored:
        
        k = S_Material_To_Be_Explored.pop(0)
               
        for i_producing, ii_consuming in product(model.S_I_Producing_K[k], model.S_I_Consuming_K[k]):
                
            j_producing = next(iter(model.S_J_Executing_I[i_producing]))
            jj_consuming = next(iter(model.S_J_Executing_I[ii_consuming]))
                
            production_relationship[i_producing, j_producing, ii_consuming, jj_consuming] = get_production_relationship(model, i_producing, j_producing, ii_consuming, jj_consuming)
            number_periods[i_producing, j_producing, ii_consuming, jj_consuming] = get_number_periods(model, i_producing, j_producing, ii_consuming, jj_consuming, production_relationship) 
            est_task[jj_consuming, ii_consuming] = get_est(model, i_producing, j_producing, ii_consuming, jj_consuming, number_periods, est_task) 
        
    print(production_relationship)        
    print(number_periods)   
    print(est_task)     