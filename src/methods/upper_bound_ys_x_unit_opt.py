from pyomo.environ import *
from src.models.constraints_est import load_constraints_set_to_zero_x_ys_est
from src.models.parameters import create_basic_parameters
from src.visualization.plot_results import plot_gantt_chart
from src.models.model_solve import solve_model, define_solver
#from src.models.model_build import load_model_sets_parameters_variables, load_basic_model_constraints_objective


def compute_upper_bound_x_unit(model: ConcreteModel, stn_data: dict, planning_horizon: int) -> None:
    """
    From the basic formulation, creates a model considering only constraints for tasks and units, and without material constraints. Here, the objective is to maximize production operations.
    
    Args:
        - stn_data (dict): a dictionary with the state-task network instance data.
        - planning_horizon (int): planning horizon.

    Returns:
        - upper_bound_x_unit (dict): a dictionary with upper bounds on X for each unit.
    """
    
    #model = ConcreteModel()
    
    #load_model_sets_parameters_variables(model, stn_data, planning_horizon)
    #compute_est_subsequent_tasks(model, stn_data)
       
    #load_basic_model_constraints_objective(model, stn_data, planning_horizon, 'bound_production_operations')    
    create_basic_parameters(model, stn_data)
    load_constraints_set_to_zero_x_ys_est(model)
    
    solver = define_solver()
    solve_model(solver, model)
    upper_bound_x_unit = {}
    
    for j in model.S_Units:
        if len(model.S_I_In_J[j]) >= 2:
            upper_bound_x_unit[j] = sum(model.V_X[i,j,n].value for i in model.S_I_Production_Tasks for n in model.S_Time if (i,j) in model.P_Task_Unit_Network)
    
    stn_data['UPPER_BOUND_X_UNIT'] = upper_bound_x_unit  
    
    print(stn_data['UPPER_BOUND_X_UNIT'])
    
    plot_gantt_chart(planning_horizon, model, "X")


def compute_upper_bound_y_unit(model: ConcreteModel, stn_data: dict, planning_horizon: int) -> None:
    """
    From the basic formulation, creates a model considering only constraints for tasks and units, and without material constraints. Here, the objective is to maximize startups.
    
    Args:
        - stn_data (dict): a dictionary with the state-task network instance data.
        - planning_horizon (int): planning horizon.

    Returns:
        - - upper_bound_y_unit (dict): a dictionary with upper bounds on Y_Start for each unit.
    """
    
    #model = ConcreteModel()
    
    #load_model_sets_parameters_variables(model, stn_data, planning_horizon)
    #compute_est_subsequent_tasks(model, stn_data)
       
    #load_basic_model_constraints_objective(model, stn_data, planning_horizon, 'bound_startups')    
    create_basic_parameters(model, stn_data)
    load_constraints_set_to_zero_x_ys_est(model)
    
    solver = define_solver()
    solve_model(solver, model)
    upper_bound_y_unit = {}
    
    for j in model.S_Units:
        if len(model.S_I_In_J[j]) >= 2:
            upper_bound_y_unit[j] = sum(model.V_Y_Start[i,j,n].value for i in model.S_I_Production_Tasks for n in model.S_Time if (i,j) in model.P_Task_Unit_Network)
    
    stn_data['UPPER_BOUND_Y_UNIT'] = upper_bound_y_unit  
    
    print(stn_data['UPPER_BOUND_Y_UNIT'])
    
    plot_gantt_chart(planning_horizon, model, "Y")   