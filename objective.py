from pyomo.environ import *

def define_objective(model, STN, objective):
   
   STATES = STN['STATES']
   STATES_SHIPMENT = STN['STATES_SHIPMENT']
   ST_ARCS = STN['ST_ARCS']
   TS_ARCS = STN['TS_ARCS']
   UNIT_TASKS = STN['UNIT_TASKS']
   #TIME = STN['TIME']
   TASKS_TRANSITION_TASKS = STN['TASKS_TRANSITION_TASKS']
   
   fix_operational_cost = sum(UNIT_TASKS[(j,i)]['Cost']*model.V_X[i,j,n] for (i,j) in model.P_Task_Unit_Network for n in model.S_Time)
   variable_operational_cost = sum(UNIT_TASKS[(j,i)]['vCost']*model.V_B[i,j,n] for (i,j) in model.P_Task_Unit_Network for n in model.S_Time)
   production_revenue = sum(STATES[k]['price']*model.V_B[i,j,n] for k in model.S_Materials for i in model.S_I_Producing_K[k] for j in model.S_J_Executing_I[i] for n in model.S_Time if STATES[k]['isProd'] == True)
   makespan = sum(n*model.V_X[i,j,n] for (i,j) in model.P_Task_Unit_Network for n in model.S_Time)
   
   if objective == 'total_cost':
      return fix_operational_cost + variable_operational_cost
   elif objective == 'production_reveue':
      return production_revenue
   elif objective == 'makespan':
      return makespan


def create_objective_function(model, STN, opt_sense, objective):
    
    model.C_Objective = Objective(expr = define_objective(model, STN, objective), sense = opt_sense)
    
def get_objective_value(model, STN):
   
   UNIT_TASKS = STN['UNIT_TASKS']
   
   fix_operational_cost = sum(UNIT_TASKS[(j,i)]['Cost']*model.V_X[i,j,n].value for (i,j) in model.P_Task_Unit_Network for n in model.S_Time)
   variable_operational_cost = sum(UNIT_TASKS[(j,i)]['vCost']*model.V_B[i,j,n].value for (i,j) in model.P_Task_Unit_Network for n in model.S_Time)
      
   return fix_operational_cost + variable_operational_cost