from pyomo.environ import *
from src.models.constraints_est import load_constraint_set_to_zero_x_est, load_constraint_set_to_zero_ys_est
from src.models.parameters import create_parameters_tightening_constraints
from src.visualization.plot_results import plot_gantt_chart
from src.models.model_solve import solve_model, define_solver
from src.models.base_model_build import load_model_sets_parameters_variables, load_basic_model_constraints_objective
from src.methods.est import compute_est_subsequent_tasks

def compute_upper_bound_x_unit(stn_data: dict, planning_horizon: int) -> None:
    """
    From the basic formulation, creates a model considering only constraints for tasks and units, and without material constraints. Here, the objective is to maximize production operations.
    
    Args:
        - stn_data (dict): a dictionary with the state-task network instance data.
        - planning_horizon (int): planning horizon.

    Returns:
        - upper_bound_x_unit (dict): a dictionary with upper bounds on X for each unit.
    """
    
    model_init_max_production_unit = ConcreteModel()
    
    load_model_sets_parameters_variables(model_init_max_production_unit, stn_data, planning_horizon)
    compute_est_subsequent_tasks(model_init_max_production_unit, stn_data)   
    load_basic_model_constraints_objective(model_init_max_production_unit, stn_data, planning_horizon, 'bound_production_operations_x_unit')    
    create_parameters_tightening_constraints(model_init_max_production_unit, stn_data, "")
    load_constraint_set_to_zero_x_est(model_init_max_production_unit)
    load_constraint_set_to_zero_ys_est(model_init_max_production_unit)
    
    solver = define_solver()
    solve_model(solver, model_init_max_production_unit)
    upper_bound_x_unit = {}
    
    for j in model_init_max_production_unit.S_Units:
        upper_bound_x_unit[j] = sum(model_init_max_production_unit.V_X[i,j,n].value for i in model_init_max_production_unit.S_I_Production_Tasks for n in model_init_max_production_unit.S_Time if (i,j) in model_init_max_production_unit.P_Task_Unit_Network)
        print(f'Unit: {j}, Used Time Points = {upper_bound_x_unit[j]}')
    
    stn_data['UPPER_BOUND_X_UNIT'] = upper_bound_x_unit    
    #plot_gantt_chart(planning_horizon, model_init_max_production_unit, "X")


def compute_upper_bound_y_unit(stn_data: dict, planning_horizon: int) -> None:
    """
    From the basic formulation, creates a model considering only constraints for tasks and units, and without material constraints. Here, the objective is to maximize startups.
    
    Args:
        - stn_data (dict): a dictionary with the state-task network instance data.
        - planning_horizon (int): planning horizon.

    Returns:
        - upper_bound_y_unit (dict): a dictionary with upper bounds on Y_Start for each unit.
    """
    
    model_init_max_startups_unit = ConcreteModel()
        
    load_model_sets_parameters_variables(model_init_max_startups_unit, stn_data, planning_horizon)
    compute_est_subsequent_tasks(model_init_max_startups_unit, stn_data)
    load_basic_model_constraints_objective(model_init_max_startups_unit, stn_data, planning_horizon, 'bound_startups_ys_unit')    
    create_parameters_tightening_constraints(model_init_max_startups_unit, stn_data, "")
    load_constraint_set_to_zero_x_est(model_init_max_startups_unit)
    load_constraint_set_to_zero_ys_est(model_init_max_startups_unit)
    
    
    solver = define_solver()
    solve_model(solver, model_init_max_startups_unit)
    upper_bound_y_unit = {}
    
    for j in model_init_max_startups_unit.S_Units:
        upper_bound_y_unit[j] = sum(model_init_max_startups_unit.V_Y_Start[i,j,n].value for i in model_init_max_startups_unit.S_I_Production_Tasks for n in model_init_max_startups_unit.S_Time if (i,j) in model_init_max_startups_unit.P_Task_Unit_Network)
        print(f'Unit: {j}, Number of Startups = {upper_bound_y_unit[j]}')
    
    stn_data['UPPER_BOUND_Y_UNIT'] = upper_bound_y_unit           
    #plot_gantt_chart(planning_horizon, model_init_max_startups_unit, "Y")  