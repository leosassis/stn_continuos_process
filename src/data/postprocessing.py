from src.utils.utils import compute_num_variables_constraints
from pyomo.environ import *


def initialize_results_dict(network: str, case: str, H: int, tau_factor: int, beta_factor: int) -> dict:
    
    instance_name = f"{network}_{case}_{H}_{tau_factor}_{beta_factor}"
    
    return {
            #"Network": network,
            #"Case": case,
            #"Horizon": H,
            #"Tau_Factor": tau_factor,
            #"Beta_Factor": beta_factor,
            "Instance": instance_name,
            "MILP Objective": None,
            "Upper Bound": None,
            "MILP Time": None,
            "MILP Status": None,
            "MILP Term. Condition": None,
            "LP Relaxation": None,
            "Num. Binary Var.": None,
            "Total Num. Var.": None,
            "Num. Constraints": None,
            
            "MILP+est Objective": None,
            "Upper Bound est": None,
            "MILP+est Time": None,
            "MILP+est Status": None,
            "MILP+est Term. Condition": None,
            "LP+est Relaxation": None,
            "Num. Binary Var. est": None,
            "Total Num. Var. est": None,
            "Num. Constraints est": None,
            }
    
def create_dict_result(result: dict, model_analytics_milp: list, results_milp: Any, results_lp: ConcreteModel, model_analytics_milp_est: list, results_milp_est: Any, results_est_lp: ConcreteModel) -> dict:
    
    if results_milp.solver.status == 'ok' and results_milp_est.solver.status == 'ok':  
    
        result['MILP Objective'] = round(results_milp.problem.lower_bound, 2)
        result['Upper Bound'] = round(results_milp.problem.upper_bound, 2)
        result['MILP Time'] = round(results_milp.solver.time, 2)
        result['MILP Status'] = str(results_milp.solver.status)
        result['MILP Term. Condition'] = str(results_milp.solver.termination_condition)
        result['LP Relaxation'] = round(results_lp.problem.lower_bound, 2)
        result['Num. Binary Var.'] = model_analytics_milp[1]
        result['Total Num. Var.'] = model_analytics_milp[0]
        result['Num. Constraints'] = model_analytics_milp[2]
        
        result['MILP+est Objective'] = round(results_milp_est.problem.lower_bound, 2)
        result['Upper Bound est'] = round(results_milp_est.problem.upper_bound, 2)
        result['MILP+est Time'] = round(results_milp_est.solver.time, 2)
        result['MILP+est Status'] = str(results_milp_est.solver.status)
        result['MILP+est Term. Condition'] = str(results_milp_est.solver.termination_condition)
        result['LP+est Relaxation'] = round(results_est_lp.problem.lower_bound, 2)
        result['Num. Binary Var. est'] = model_analytics_milp_est[1]
        result['Total Num. Var. est'] = model_analytics_milp_est[0]
        result['Num. Constraints est'] = model_analytics_milp_est[2]
    
    return result