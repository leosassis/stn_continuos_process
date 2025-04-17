from pyomo.environ import *

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

def est_initialization(EST: dict) -> dict:
    est = {(i,j): EST[(j,i)] for (j,i) in EST}
    return est


def est_unit_initialization(model: ConcreteModel, j: Any) -> Any:
    est_unit = min(model.P_EST[i,j] for i in model.S_I_Production_Tasks if (i,j) in model.P_Task_Unit_Network)
    return est_unit


def upper_bound_x_initialization(upper_bound_x: dict) -> dict:
    dict_upper_bound_x = {(i,j): upper_bound_x[(j,i)] for (j,i) in upper_bound_x}
    return dict_upper_bound_x


def upper_bound_x_unit_initialization(model: ConcreteModel, j: Any) -> dict:
    dict_upper_bound_x_unit =  max(model.P_Upper_Bound_X[i,j] for i in model.S_I_Production_Tasks if (i,j) in model.P_Task_Unit_Network)
    return dict_upper_bound_x_unit


def create_parameters(model: ConcreteModel, STN: dict, H: int) -> None:
    
    states = STN['STATES']
    states_shipment = STN['STATES_SHIPMENT']
    st_arcs = STN['ST_ARCS']
    ts_arcs = STN['TS_ARCS']
    unit_tasks = STN['UNIT_TASKS']
    H = H
    
    model.P_Tau = Param(model.S_Tasks, model.S_Units, initialize = init_parameter_tau(unit_tasks))
    model.P_Init_Inventory_Material = Param(model.S_Materials, initialize = init_initial_inventory(states))
    model.P_Chi = Param(model.S_Materials, initialize = init_storage_limits(states))
    model.P_Material_Demand = Param(model.S_Materials, model.S_Time, initialize = init_material_demand(states_shipment, H), default = 0)
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
    
   
def create_est_parameters(model: ConcreteModel, STN: dict) -> None:
    
    est_stn = STN['EST']
    upper_bound_x = STN['UPPER_BOUND_X']
           
    model.P_EST = Param(model.S_Tasks, model.S_Units, initialize = est_initialization(est_stn))
    model.P_EST_Unit = Param(model.S_Units, initialize = est_unit_initialization)
    model.P_Upper_Bound_X = Param(model.S_Tasks, model.S_Units, initialize = upper_bound_x_initialization(upper_bound_x))
    model.P_Upper_Bound_X_Unit = Param(model.S_Units, initialize = upper_bound_x_unit_initialization)
        
    model.P_EST.pprint()
    model.P_EST_Unit.pprint()
    model.P_Upper_Bound_X.pprint()
    model.P_Upper_Bound_X_Unit.pprint()
     