from pyomo.environ import *


def initialize_results_dict(network: str, startup_cost_factor: int, planning_horizon: int, tau_factor: int, beta_factor: int, formulation_name: str, taskID: int, mip_gap_multiplier: int) -> dict[str, Any]:
    """
    Initializes a dictionary to store results from a single optimization instance.

    Args:
        - network (str): name of the network.
        - startup_cost_factor (int): factor for startup cost parameters.
        - planning_horizon (int): planning horizon.
        - tau_factor (int): factor for tau parameters.
        - beta_factor (int): factor for beta parameters.
        - formulation_name (str): name of the model formulation.
        - taskID (int): id that identifies the data set. It is the number at the end of each json file.
        - mip_gap_multiplier (int): multiplier to increase the mip gap.

    Returns:
        dict[str, Any]: Initialized dictionary with placeholders for results.
    """
    
    instance_name = f"{network}_{startup_cost_factor}_{planning_horizon}_{tau_factor}_{beta_factor}_{mip_gap_multiplier}_{taskID}"
    
    return {
            "Instance": instance_name,
            "Formulation": None,
            "MILP Objective": None,
            "Upper Bound": None,
            "Relative Gap": None,
            "Time (s)": None,
            "MILP Status": None,
            "MILP Term. Condition": None,
            "MIP Gap Mult.": None,
            "LP Relaxation": None,
            "Num. Binary Var.": None,
            "Total Num. Var.": None,
            "Num. Constraints": None,}
    
    
def create_dict_result(result: dict, model_analytics_milp: list, results_milp: Any, results_lp: ConcreteModel, formulation_name: str, mip_gap_multiplier: int) -> dict[str, Any]:
    """
    Updates the result dictionary with actual values from MILP and LP results if results are feasible.

    Args:
        - result (dict[str, Any]): initialized result dictionary.
        - model_analytics_milp (list): [total vars, binary vars, constraints].
        - results_milp (Any): Pyomo solver results object for the MILP model.
        - results_lp (Any): Pyomo solver results object for the LP relaxation.
        - formulation_name (str): Name of the model formulation.

    Returns:
        dict[str, Any]: Updated dictionary with extracted results.
    """
    
    if results_milp.solver.termination_condition != TerminationCondition.infeasible:  
    
        result["Formulation"] = formulation_name
        result['MILP Objective'] = round(results_milp.problem.lower_bound, 2)
        result['Upper Bound'] = round(results_milp.problem.upper_bound, 2)
        result['Relative Gap'] = round( abs((round(results_milp.problem.upper_bound, 6) - round(results_milp.problem.lower_bound, 6))) / abs(round(results_milp.problem.lower_bound, 2)), 6)
        result['Time (s)'] = round(results_milp.solver.time, 2)
        result['MILP Status'] = str(results_milp.solver.status)
        result['MILP Term. Condition'] = str(results_milp.solver.termination_condition)
        result['MIP Gap Mult.'] = mip_gap_multiplier
        result['LP Relaxation'] = round(results_lp.problem.lower_bound, 2)
        result['Num. Binary Var.'] = model_analytics_milp[1]
        result['Total Num. Var.'] = model_analytics_milp[0]
        result['Num. Constraints'] = model_analytics_milp[2]
    
    return result