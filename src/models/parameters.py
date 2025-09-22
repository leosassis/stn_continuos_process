from pyomo.environ import *
from src.models.variables import RUNS_NEED_TO_FINISH_FLAG

ADD_TIME_POINT = 1  # Used for computing the number of time periods

def init_parameter_tau(UNIT_TASKS):
    P_TAU = {(i,j): UNIT_TASKS[(j,i)]['tau'] for (j,i) in UNIT_TASKS}
    return P_TAU

def init_material_demand(STATES_SHIPMENT, H):
    P_DEMAND = {(k,n): STATES_SHIPMENT[(k,n)]['demand'] for (k,n) in STATES_SHIPMENT if n <= H}
    return P_DEMAND
    
def init_initial_inventory(STATES):        
    P_INITIAL_INVENTORY = {k: STATES[k]['initial'] for k in STATES}
    return P_INITIAL_INVENTORY

def init_storage_limits(STATES):
    P_CHI = {k: STATES[k]['capacity'] for k in STATES}
    return P_CHI

def init_beta_max(UNIT_TASKS):
    P_Bmax = {(i,j): UNIT_TASKS[(j,i)]['Bmax'] for (j,i) in UNIT_TASKS}
    return P_Bmax

def init_beta_min(UNIT_TASKS):
    P_Bmin = {(i,j): UNIT_TASKS[(j,i)]['Bmin'] for (j,i) in UNIT_TASKS}
    return P_Bmin

def init_conversion_rate_consuming(ST_ARCS):
    P_rho_MINUS = {(i,k): ST_ARCS[(k,i)]['rho'] for (k,i) in ST_ARCS}
    return P_rho_MINUS

def init_conversion_rate_production(TS_ARCS):
    P_rho_PLUS = {(i,k): TS_ARCS[(i,k)]['rho'] for (i,k) in TS_ARCS}
    return P_rho_PLUS

def init_tau_min(model, UNIT_TASKS):
    P_Tau_Min = {(i,j): UNIT_TASKS[(j,i)]['tau_min'] for (j,i) in UNIT_TASKS if i in model.S_I_Production_Tasks}
    return P_Tau_Min

def init_tau_max(model, UNIT_TASKS):
    P_Tau_Max = {(i,j): UNIT_TASKS[(j,i)]['tau_max'] for (j,i) in UNIT_TASKS if i in model.S_I_Production_Tasks}
    return P_Tau_Max

def unit_initialization(model):
    P_Unit_Init = {(j): 1 for j in model.S_Units}
    return P_Unit_Init

def start_up_cost(UNIT_TASKS):
    P_StarUp_Cost = {(j,i): UNIT_TASKS[(j,i)]['sCost'] for (j,i) in UNIT_TASKS}
    return P_StarUp_Cost

def est_task_initialization(EST: dict) -> dict:
    est = {(i,j): EST[(j,i)] for (j,i) in EST}
    return est

def est_unit_initialization(model: ConcreteModel, j: Any) -> dict:
    est_unit = min(model.P_EST_Task[i,j] for i in model.S_I_Production_Tasks if (i,j) in model.P_Task_Unit_Network)
    return est_unit

def upper_bound_x_task_initialization(upper_bound_x: dict) -> dict:
    dict_upper_bound_x = {(i,j): upper_bound_x[(j,i)] for (j,i) in upper_bound_x}
    return dict_upper_bound_x

def upper_bound_x_unit_initialization(upper_bound_x_unit: dict) -> dict:
    dict_upper_bound_x_unit =  {j: upper_bound_x_unit[j] for j in upper_bound_x_unit}
    return dict_upper_bound_x_unit

def upper_bound_ys_unit_initialization(upper_bound_ys_unit: dict) -> dict:
    dict_upper_bound_ys_unit =  {j: upper_bound_ys_unit[j] for j in upper_bound_ys_unit}
    return dict_upper_bound_ys_unit

def est_group_initialization(est_group: dict) -> dict:
    dict_est_group = {k: est_group[k] for k in est_group}
    return dict_est_group

def ub_ys_task_initialization(model: ConcreteModel) -> dict:
    """ 
    Populates parameter model.P_UB_YS_Task_PPC to bound YS in the cases where a task run must finish and not at the end of the planning horizon.
    """
    
    num_periods = max(model.S_Time)
    upper_bound_ys_task = {}
    
    for (i,j) in model.P_Task_Unit_Network:
        
        # Skip tasks that are not production tasks
        if i not in model.S_I_Production_Tasks:
            continue
        
        # Import tau_max, tau_min, tau_shutdown and number of time points
        tau_min = model.P_Tau_Min[i,j]
        tau_shutdown = model.P_Tau_End_Task[i]
        tau_startup = 0
        number_time_points = num_periods + ADD_TIME_POINT# - model.P_EST_Task[i,j]
        
        # Import tau for the production tasks with transitions
        for ii in model.S_I_Startup_Tasks:
            if (
                i in model.S_I_Production_Tasks_With_Transition and 
                (j,i,ii) in model.P_Task_Transitions_Unit
            ):
                tau_startup = model.P_Tau[ii,j]
            
        for ii in model.S_I_Shutdown_Tasks:
            if (
                i in model.S_I_Production_Tasks_With_Transition and
                (j,i,ii) in model.P_Task_Transitions_Unit
            ):
                tau_shutdown = model.P_Tau[ii,j]
        
        if RUNS_NEED_TO_FINISH_FLAG == True:
            upper_bound_ys_task[i,j] = floor( number_time_points  / ( tau_min +  tau_startup + tau_shutdown ) )
    
        else:
            upper_bound_ys_task[i,j] = ceil( number_time_points  / ( tau_min +  tau_startup + tau_shutdown ) )
        
        print(f"Production task = {i}, Time Points = {number_time_points}, tau_startup = {tau_startup}, tau_shutdown = {tau_shutdown}, Upper Bound YS = {upper_bound_ys_task[i,j]}, Remaining Time Points = {number_time_points - upper_bound_ys_task[i,j] * ( tau_min +  tau_startup + tau_shutdown )}")
    
    return upper_bound_ys_task        
               
        
def ub_ys_unit_initialization(model: ConcreteModel) -> dict:
    dict_ys_unit = {j: floor( ( max(model.S_Time) + 1 - model.P_EST_Unit[j] ) / ( min( model.P_Tau_Min[i,j] for i in model.S_I_In_J[j] ) + model.P_Tau_End_Unit[j] ) ) for j in model.P_EST_Unit}
    
    return dict_ys_unit
    
def ub_new_ys_unit_initialization(model: ConcreteModel) -> dict:
    dict_new_ys_unit = {j: max(model.S_Time) + 1 - model.P_EST_Unit[j] for j in  model.P_EST_Unit}
    return dict_new_ys_unit

def ub_x_task_initialization(model: ConcreteModel) -> dict:
    dict_x_task = {(i,j): floor( ( model.P_Tau_Max[i,j] * ( max(model.S_Time) + 1 - model.P_EST_Task[i,j] ) ) / ( model.P_Tau_Max[i,j] + model.P_Tau_End_Task[i] ) ) for (i,j) in model.P_EST_Task}
    return dict_x_task

def ub_x_unit_initialization(model: ConcreteModel) -> dict:
    dict_x_unit = {j: floor( ( max( model.P_Tau_Max[i,j] for i in model.S_I_In_J[j] ) * ( max(model.S_Time) + 1 - model.P_EST_Unit[j] ) ) / ( max( model.P_Tau_Max[i,j] for i in model.S_I_In_J[j] ) + model.P_Tau_End_Unit[j] ) ) for j in model.P_EST_Unit}
    return dict_x_unit


def create_basic_parameters(model: ConcreteModel, stn_data: dict, planning_horizon: int) -> None:
    """
    Appends to the model the basic parameters.
    
    Args:
        - model (ConcreteModel): a Pyomo model instance.
        - stn_data (dict): a dictioinary containing the stn data.
        - planning_horizon (int): size of the planning horizon.
    """
        
    states = stn_data['STATES']
    states_shipment = stn_data['STATES_SHIPMENT']
    st_arcs = stn_data['ST_ARCS']
    ts_arcs = stn_data['TS_ARCS']
    unit_tasks = stn_data['UNIT_TASKS']
        
    model.P_Tau = Param(model.S_Tasks, model.S_Units, initialize = init_parameter_tau(unit_tasks))
    model.P_Init_Inventory_Material = Param(model.S_Materials, initialize = init_initial_inventory(states))
    model.P_Chi = Param(model.S_Materials, initialize = init_storage_limits(states))
    model.P_Material_Demand = Param(model.S_Materials, model.S_Time, initialize = init_material_demand(states_shipment, planning_horizon), default = 0)
    model.P_Beta_Max = Param(model.S_Tasks, model.S_Units, initialize = init_beta_max(unit_tasks))
    model.P_Beta_Min = Param(model.S_Tasks, model.S_Units, initialize = init_beta_min(unit_tasks))
    model.P_Rho_Minus = Param(model.S_Tasks, model.S_Materials, initialize = init_conversion_rate_consuming(st_arcs))
    model.P_Rho_Plus = Param(model.S_Tasks, model.S_Materials, initialize = init_conversion_rate_production(ts_arcs))
    model.P_Tau_Min = Param(model.S_Tasks, model.S_Units, initialize = init_tau_min(model, unit_tasks))
    model.P_Tau_Max = Param(model.S_Tasks, model.S_Units, initialize = init_tau_max(model, unit_tasks))
    model.P_Unit_Initialization = Param(model.S_Units, initialize = unit_initialization(model))
    model.P_StartUp_Cost = Param(model.S_Units, model.S_Tasks, initialize =  start_up_cost(unit_tasks))
    model.P_Material_State = Param(model.S_Materials)
    model.P_Product_Production = Param(model.S_Materials, mutable = True, initialize = 0) 
    model.P_Tau_End_Task = Param(model.S_Tasks, default = 1)
    model.P_Tau_End_Unit = Param(model.S_Units, default = 1)
          

def create_parameters_tightening_constraints(model: ConcreteModel, stn_data: dict, formulation_id: str) -> None:
    """
    Appends to the model parameters according to the formulation  with the earliest start time information.
    
    Args:
        - model (ConcreteModel): a Pyomo model instance.
        - stn_data (dict): a dictioinary containing the stn data.
        - formulation_id (str): a string indentifying the formulation (e.g., "", "UB_YS_Task", "UB_YS_Unit", "UB_X_Task", "UB_X_Unit", "EST_Group_K", "All").
    """
    
    est = stn_data['EST']        
        
    model.P_EST_Task = Param(model.S_Tasks, model.S_Units, initialize = est_task_initialization(est))
    model.P_EST_Unit = Param(model.S_Units, initialize = est_unit_initialization)
        
    if formulation_id == "UB_YS_Task":
        
        model.P_UB_YS_Task_PPC = Param(model.S_Tasks, model.S_Units, initialize = ub_ys_task_initialization(model))
    
    elif formulation_id == "UB_YS_Unit":
        upper_bound_ys_unit = stn_data['UPPER_BOUND_Y_UNIT']
    
        model.P_UB_YS_Unit_OPT = Param(model.S_Units, initialize = upper_bound_ys_unit_initialization(upper_bound_ys_unit))
    
    elif formulation_id == "UB_X_Task":
        upper_bound_x_task = stn_data['UPPER_BOUND_X_TASK']
        
        model.P_UB_X_Task_OPT = Param(model.S_Tasks, model.S_Units, initialize = upper_bound_x_task_initialization(upper_bound_x_task))
    
    elif formulation_id == "UB_X_Unit":
        upper_bound_x_unit = stn_data['UPPER_BOUND_X_UNIT']
        
        model.P_UB_X_Unit_OPT = Param(model.S_Units, initialize = upper_bound_x_unit_initialization(upper_bound_x_unit))   
    
    elif formulation_id == "EST_Group_K":
        est_group = stn_data['EST_GROUP']
        
        model.P_EST_Group = Param(model.S_Materials, initialize = est_group_initialization(est_group))  
    
    elif formulation_id == "All":
        upper_bound_x_task = stn_data['UPPER_BOUND_X_TASK']
        upper_bound_x_unit = stn_data['UPPER_BOUND_X_UNIT']
        upper_bound_ys_unit = stn_data['UPPER_BOUND_Y_UNIT']
        est_group = stn_data['EST_GROUP']

        model.P_EST_Group = Param(model.S_Materials, initialize = est_group_initialization(est_group))              
        model.P_UB_YS_Task_PPC = Param(model.S_Tasks, model.S_Units, initialize = ub_ys_task_initialization(model))
        model.P_UB_YS_Unit_OPT = Param(model.S_Units, initialize = upper_bound_ys_unit_initialization(upper_bound_ys_unit))    
        model.P_UB_X_Task_OPT = Param(model.S_Tasks, model.S_Units, initialize = upper_bound_x_task_initialization(upper_bound_x_task))
        model.P_UB_X_Unit_OPT = Param(model.S_Units, initialize = upper_bound_x_unit_initialization(upper_bound_x_unit))     
        