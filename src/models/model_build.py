from pyomo.environ import *
from src.models.sets import create_main_sets_parameters
from src.models.variables import create_variables, init_variables 
from src.models.parameters import create_parameters, create_ppc_parameters, create_base_parameters, create_opt_parameters
from src.models.constraints import load_basic_model_constraints, load_constraints_bounds_x_y_units
from src.models.objective import create_objective_function
from src.models.constraints_est import create_constraints_set_to_zero_x_ys_est, create_constraints_est_f1, create_constraints_est_f2 
from src.methods.est import compute_est_subsequent_tasks
from src.methods.est_group import compute_est_group_tasks
from src.methods.upper_bound_x_task_opt import compute_upper_bound_x_task
from src.models.model_solve import solve_model
from src.models.optimization_config import define_solver
#from src.methods.upper_bound_ys_x_unit_opt import compute_upper_bound_ys_unit, compute_upper_bound_x_unit
from src.visualization.plot_results import plot_gantt_chart


def _load_model_sets_parameters_variables(model: ConcreteModel, stn_data: dict, planning_horizon: int) -> None:
    """
    Initializes base model components: sets, variables and parameters.
    
    Args:
        - model (ConcreteModel): an empty Pyomo model to be configured.
        - stn_data (dict): a dictionary with the state-task network instance data.
        - planning_horizon (int): planning horizon.
    
    Returns:
        - None. modifies the model in-place.    
    """    
    
    
    create_main_sets_parameters(model, stn_data, planning_horizon)
    create_variables(model)    
    create_parameters(model, stn_data, planning_horizon)
    init_variables(model, planning_horizon)
    

def _initialize_model_type(model: ConcreteModel, stn_data: dict, planning_horizon: int, model_type: str) -> None:
    """
    Initializes base model components: sets, variables, parameters, and constraints.
    
    Args:
        - model (ConcreteModel): an empty Pyomo model to be configured.
        - stn_data (dict): a dictionary with the state-task network instance data.
        - planning_horizon (int): planning horizon.
        - model_type (str): a string indicating which base model to load (e.g., 'base_model', 'bound_production_operations', 'bound_startups')

    Returns:
        - None. modifies the model in-place.    
    """
    
    
    if model_type == 'base_model':
        load_basic_model_constraints(model)
        create_objective_function(model, stn_data, 'base_model')
    elif model_type == 'bound_production_operations':
        load_constraints_bounds_x_y_units(model)
        create_objective_function(model, stn_data, 'bound_production_operations')
    elif model_type == 'bound_startups':
        load_constraints_bounds_x_y_units(model)
        create_objective_function(model, stn_data, 'bound_startups')
        

def create_model_f0(stn_data: dict, planning_horizon: int) -> tuple[ConcreteModel, str]:
    """
    Creates the base MILP model.
    
    Args:
        - stn_data (dict): a dictionary with the state-task network instance data.
        - planning_horizon (int): planning horizon.

    Returns:
        - ConcreteModel: returns a Pyomo model.
    """
    
    model = ConcreteModel()
    
    _load_model_sets_parameters_variables(model, stn_data, planning_horizon)
    _initialize_model_type(model, stn_data, planning_horizon, 'base_model')
    formulation_name = "F0"
    
    return model, formulation_name


def create_model_f1(stn_data: dict, planning_horizon: int) -> tuple[ConcreteModel, str]:
    """
    Creates the enhanced MILP model with EST calculations and additional constraints.
    
    Args:
        - stn_data (dict): a dictionary with the state-task network instance data.
        - planning_horizon (int): planning horizon.

    Returns:
        - ConcreteModel: returns a Pyomo model.
    """
    
    model = ConcreteModel()
    
    _load_model_sets_parameters_variables(model, stn_data, planning_horizon)
    _initialize_model_type(model, stn_data, planning_horizon, 'base_model')    
    compute_est_subsequent_tasks(model, stn_data)
    compute_est_group_tasks(model, stn_data)
    create_base_parameters(model, stn_data)
    create_ppc_parameters(model, stn_data)
    create_constraints_set_to_zero_x_ys_est(model)
    create_constraints_est_f1(model)
    formulation_name = "F1"
        
    return model, formulation_name


def create_model_f2(stn_data: dict, planning_horizon: int) -> tuple[ConcreteModel, str]:
    """
    Creates the enhanced MILP model with EST calculations and additional constraints based on solving knapsack problems.
    
    Args:
        - stn_data (dict): a dictionary with the state-task network instance data.
        - planning_horizon (int): planning horizon.

    Returns:
        - ConcreteModel: returns a Pyomo model.
    """
    
    model = ConcreteModel()
    
    _load_model_sets_parameters_variables(model, stn_data, planning_horizon)
    compute_est_subsequent_tasks(model, stn_data)
    compute_est_group_tasks(model, stn_data)
    compute_upper_bound_x_task(model, stn_data)
        
    # Compute upper bounds on X for tasks that share a unit.
    _initialize_model_type(model, stn_data, planning_horizon, 'bound_production_operations')    
    create_base_parameters(model, stn_data)
    create_constraints_set_to_zero_x_ys_est(model)
    
    solver = define_solver()
    solve_model(solver, model)
    upper_bound_x_unit = {}
    
    for j in model.S_Units:
        if len(model.S_I_In_J[j]) >= 2:
            upper_bound_x_unit[j] = sum(model.V_X[i,j,n].value for i in model.S_I_Production_Tasks for n in model.S_Time if (i,j) in model.P_Task_Unit_Network)
    
    stn_data['UPPER_BOUND_X_UNIT'] = upper_bound_x_unit  
    print(stn_data['UPPER_BOUND_X_UNIT'])
    
    plot_gantt_chart(planning_horizon, model, "X")
    
    #compute_upper_bound_x_unit(model, stn_data, planning_horizon)
    #compute_upper_bound_ys_unit(model, stn_data)    
    #_initialize_base_model(model, stn_data, planning_horizon, 'bound_production_operations')    
    #create_ppc_parameters(model, stn_data)
    #create_opt_parameters(model, stn_data)    
    #create_constraints_est_f2(model)
    formulation_name = "F2"
        
    return model, formulation_name


def create_model_f3(stn_data: dict, planning_horizon: int) -> tuple[ConcreteModel, str]:
    """
    Creates the enhanced MILP model with EST calculations and additional constraints based on solving knapsack problems.
    
    Args:
        - stn_data (dict): a dictionary with the state-task network instance data.
        - planning_horizon (int): planning horizon.

    Returns:
        - ConcreteModel: returns a Pyomo model.
    """
    
    model = ConcreteModel()
    
    _load_model_sets_parameters_variables(model, stn_data, planning_horizon)
    compute_est_subsequent_tasks(model, stn_data)
    compute_est_group_tasks(model, stn_data)
    compute_upper_bound_x_task(model, stn_data)
    
    
    print('Upper Bound YS ########################################################################################')
    _initialize_model_type(model, stn_data, planning_horizon, 'bound_startups') 
    create_ppc_parameters(model, stn_data)
    create_constraints_set_to_zero_x_ys_est(model)
    
    #compute_upper_bound_x_unit(model, stn_data, planning_horizon)
    #compute_upper_bound_ys_unit(model, stn_data)    
    #_initialize_base_model(model, stn_data, planning_horizon, 'bound_production_operations')    
    #create_ppc_parameters(model, stn_data)
    #create_opt_parameters(model, stn_data)    
    #create_constraints_est_f2(model)
    formulation_name = "F3"
        
    return model, formulation_name


def compute_upper_bound_x_unit(stn_data: dict, planning_horizon: int) -> None:
    """
    Creates the enhanced MILP model with EST calculations and additional constraints based on solving knapsack problems.
    
    Args:
        - stn_data (dict): a dictionary with the state-task network instance data.
        - planning_horizon (int): planning horizon.

    Returns:
        - ConcreteModel: returns a Pyomo model.
    """
    
    model = ConcreteModel()
    
    _load_model_sets_parameters_variables(model, stn_data, planning_horizon)
    compute_est_subsequent_tasks(model, stn_data)
        
    # Compute upper bounds on X for tasks that share a unit.
    _initialize_model_type(model, stn_data, planning_horizon, 'bound_production_operations')    
    create_base_parameters(model, stn_data)
    create_constraints_set_to_zero_x_ys_est(model)
    
    solver = define_solver()
    solve_model(solver, model)
    upper_bound_x_unit = {}
    
    for j in model.S_Units:
        if len(model.S_I_In_J[j]) >= 2:
            upper_bound_x_unit[j] = sum(model.V_X[i,j,n].value for i in model.S_I_Production_Tasks for n in model.S_Time if (i,j) in model.P_Task_Unit_Network)
    
    stn_data['UPPER_BOUND_X_UNIT'] = upper_bound_x_unit  
    print(stn_data['UPPER_BOUND_X_UNIT'])
    
    plot_gantt_chart(planning_horizon, model, "X")
    

def compute_upper_bound_y_unit(stn_data: dict, planning_horizon: int) -> None:
    """
    Creates the enhanced MILP model with EST calculations and additional constraints based on solving knapsack problems.
    
    Args:
        - stn_data (dict): a dictionary with the state-task network instance data.
        - planning_horizon (int): planning horizon.

    Returns:
        - ConcreteModel: returns a Pyomo model.
    """
    
    model = ConcreteModel()
    
    _load_model_sets_parameters_variables(model, stn_data, planning_horizon)
    compute_est_subsequent_tasks(model, stn_data)
        
    # Compute upper bounds on X for tasks that share a unit.
    _initialize_model_type(model, stn_data, planning_horizon, 'bound_startups')    
    create_base_parameters(model, stn_data)
    create_constraints_set_to_zero_x_ys_est(model)
    
    solver = define_solver()
    solve_model(solver, model)
    upper_bound_y_unit = {}
    
    for j in model.S_Units:
        if len(model.S_I_In_J[j]) >= 2:
            upper_bound_y_unit[j] = sum(model.V_Y_Start[i,j,n].value for i in model.S_I_Production_Tasks for n in model.S_Time if (i,j) in model.P_Task_Unit_Network)
    
    stn_data['UPPER_BOUND_Y_UNIT'] = upper_bound_y_unit  
    print(stn_data['UPPER_BOUND_Y_UNIT'])
    
    plot_gantt_chart(planning_horizon, model, "Y")    