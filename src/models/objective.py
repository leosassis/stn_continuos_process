from pyomo.environ import *


def define_objective(model: ConcreteModel, STN: dict) -> Any:
   """ 
   Define profit maximization as the objective function.
   """
   
   STATES = STN['STATES']
   UNIT_TASKS = STN['UNIT_TASKS']
   
   fix_operational_cost = sum(
      UNIT_TASKS[(j,i)]['Cost']*model.V_X[i,j,n] 
      for (i,j) in model.P_Task_Unit_Network 
      for n in model.S_Time
   )
   
   variable_operational_cost = sum(
      UNIT_TASKS[(j,i)]['vCost']*model.V_B[i,j,n] 
      for (i,j) in model.P_Task_Unit_Network 
      for n in model.S_Time
   )
   
   production_revenue = sum(
      STATES[k]['price']*model.V_B[i,j,n] 
      for k in model.S_Materials 
      for i in model.S_I_Producing_K[k] 
      for j in model.S_J_Executing_I[i] 
      for n in model.S_Time 
      if k in model.S_Final_Products
   )
   
   makespan = sum(
      n*model.V_X[i,j,n] 
      for (i,j) in model.P_Task_Unit_Network 
      for n in model.S_Time
   )
   
   lateness = sum(
      n*model.V_X[i,j,n] 
      for (i,j) in model.P_Task_Unit_Network 
      for n in model.S_Time
   )
   
   return production_revenue - fix_operational_cost - variable_operational_cost
   
   
def create_objective_function(model: ConcreteModel, STN: dict) -> None:
   """ 
   Attaches the objective function to the model.
   """
    
   model.C_Objective = Objective(expr = define_objective(model, STN), sense = maximize)