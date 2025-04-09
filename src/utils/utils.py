from pyomo.environ import *

def print_set(model, set):
    print(set.data())


def compute_product_production(model):
    production_values = {k: (sum(model.V_B[i,j,n].value for n in model.S_Time for i in model.S_I_Producing_K[k] for j in model.S_J_Executing_I[i] if (i,j) in model.P_Task_Unit_Network if k in model.S_Final_Products)) for k in model.S_Materials if k in model.S_Final_Products}
    for k, v in production_values.items():
        print(f"Material: {k}, Production: {v}")


def compute_total_production(model):
    total_production = sum(model.V_B[i,j,n].value for n in model.S_Time for k in model.S_Materials for i in model.S_I_Producing_K[k] for j in model.S_J_Executing_I[i] if (i,j) in model.P_Task_Unit_Network if k in model.S_Final_Products)
    return total_production


def get_objective_value(model, STN):
   
   UNIT_TASKS = STN['UNIT_TASKS']
   STATES = STN['STATES']
   
   fix_operational_cost = sum(UNIT_TASKS[(j,i)]['Cost']*model.V_X[i,j,n].value for (i,j) in model.P_Task_Unit_Network for n in model.S_Time)
   variable_operational_cost = sum(UNIT_TASKS[(j,i)]['vCost']*model.V_B[i,j,n].value for (i,j) in model.P_Task_Unit_Network for n in model.S_Time)
   production_revenue = sum(STATES[k]['price']*model.V_B[i,j,n].value for k in model.S_Materials for i in model.S_I_Producing_K[k] for j in model.S_J_Executing_I[i] for n in model.S_Time if k in model.S_Final_Products)
   makespan = sum(n*model.V_X[i,j,n].value for (i,j) in model.P_Task_Unit_Network for n in model.S_Time)
   
   return production_revenue - fix_operational_cost - variable_operational_cost


def print_model_constraints(model):
    
    for con in model.component_map(Constraint).itervalues():
        con.pprint()
        
        
def compute_num_variables_constraints(model):
    
        num_constraints = sum(len(constraint) for constraint in model.component_objects(Constraint, active=True))
        num_total_vars = sum(len(var) for var in model.component_objects(Var, active=True))
        num_binary_vars = sum(1 for v in model.component_objects(Var, active=True) for index in v if v[index].domain == Binary)
        
        return num_total_vars, num_binary_vars, num_constraints
