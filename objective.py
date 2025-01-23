from pyomo.environ import *

def define_objective(model, STN):
   
   STATES = STN['STATES']
   STATES_SHIPMENT = STN['STATES_SHIPMENT']
   ST_ARCS = STN['ST_ARCS']
   TS_ARCS = STN['TS_ARCS']
   UNIT_TASKS = STN['UNIT_TASKS']
   #TIME = STN['TIME']
   TASKS_TRANSITION_TASKS = STN['TASKS_TRANSITION_TASKS']
   
   fix_operational_cost = sum(UNIT_TASKS[(j,i)]['Cost']*model.V_X[i,j,n] for (i,j) in model.P_Task_Unit_Network for n in model.S_Time)
   variable_operational_cost = sum(UNIT_TASKS[(j,i)]['vCost']*model.V_B[i,j,n] for (i,j) in model.P_Task_Unit_Network for n in model.S_Time)
   startup_cost = sum(model.V_Y_Start[i,j,n]*model.P_StartUp_Cost[j,i] for (i,j) in model.P_Task_Unit_Network for n in model.S_Time)
   shutdown_cost = sum(model.V_Y_End[i,j,n]*model.P_StartUp_Cost[j,i] for (i,j) in model.P_Task_Unit_Network for n in model.S_Time)
   total_cost = fix_operational_cost + variable_operational_cost + startup_cost + shutdown_cost
   production_revenue = sum(STATES[k]['price']*model.V_B[i,j,n] for k in model.S_Materials for i in model.S_I_Producing_K[k] for j in model.S_J_Executing_I[i] for n in model.S_Time if STATES[k]['isProd'] == True)
   makespan = sum(n*model.V_X[i,j,n] for (i,j) in model.P_Task_Unit_Network for n in model.S_Time)
   
   return (production_revenue)

def create_objective_function(model, STN):
    
    model.C_Objective = Objective(expr = define_objective(model, STN), sense = maximize)