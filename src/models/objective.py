from pyomo.environ import *


def _define_objective(model: ConcreteModel, stn_data: dict, model_type: str) -> Any:
   """
   Internal helper function to define the objective function.
   Maximizes the profit: revenue - fixed cost - variable cost.
   
   Args:
      - model: a Pyomo ConcreteModel object.
      - stn_data: dictionary containing STN data (STATES, UNIT_TASKS, etc.).
      - model_type: a string indicating what to maximize (e.g., 'base_model', 'bound_production_operations', 'bound_startups').
   """
   
   
   states = stn_data['STATES']
   unit_tasks = stn_data['UNIT_TASKS']
   
   fix_operational_cost = sum(
      unit_tasks[(j,i)]['Cost'] * model.V_X[i,j,n] 
      for (i,j) in model.P_Task_Unit_Network 
      for n in model.S_Time
   )
   
   variable_operational_cost = sum(
      unit_tasks[(j,i)]['vCost'] * model.V_B[i,j,n] 
      for (i,j) in model.P_Task_Unit_Network 
      for n in model.S_Time
   )
   
   production_revenue = sum(
      states[k]['price'] * model.V_B[i,j,n] 
      for k in model.S_Materials 
      for i in model.S_I_Producing_K[k] 
      for j in model.S_J_Executing_I[i] 
      for n in model.S_Time 
      if k in model.S_Final_Products
   )
   
   makespan = sum(
      n * model.V_X[i,j,n] 
      for (i,j) in model.P_Task_Unit_Network 
      for n in model.S_Time
   )
   
   lateness = sum(
      n * model.V_X[i,j,n] 
      for (i,j) in model.P_Task_Unit_Network 
      for n in model.S_Time
   )
   
   startups = sum(
      model.V_Y_Start[i,j,n] 
      for (i,j) in model.P_Task_Unit_Network
      for n in model.S_Time
   )
   
   production_operations = sum(
      model.V_X[i,j,n] 
      for (i,j) in model.P_Task_Unit_Network 
      for n in model.S_Time      
   )
      
   if model_type == 'base_model':
   
      return production_revenue - fix_operational_cost - variable_operational_cost
   
   elif model_type == 'bound_production_operations':
   
      return production_operations
   
   elif model_type == 'bound_startups':
   
      return startups      
      
   
def create_objective_function(model: ConcreteModel, stn_data: dict, model_type: str) -> None:
   """
   Attaches a profit-maximizing objective function to the Pyomo model.
    
   Args:
      - model: a Pyomo ConcreteModel object.
      - stn_data: dictionary containing STN data (STATES, UNIT_TASKS, etc.).
      - model_type: a string indicating what to maximize (e.g., 'base_model', 'bound_production_operations', 'bound_startups').
   """
    
    
   model.C_Objective = Objective(expr = _define_objective(model, stn_data, model_type), sense = maximize)