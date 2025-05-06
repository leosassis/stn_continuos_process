from pyomo.environ import *


def constraint_set_x_to_zero_est(model: ConcreteModel, i: Any, j: Any) -> Constraint:
    if (i in model.S_I_Production_Tasks) and (j in model.S_J_Executing_I[i]) and ((i,j) in model.P_Task_Unit_Network) and (model.P_EST[i,j] > 0):
        return sum(model.V_X[i,j,n] for n in model.S_Time if (n >= 0 and n <= (model.P_EST[i,j] - 1))) == 0
    else:
        return Constraint.Skip


def constraint_upper_bound_ys(model: ConcreteModel, i: Any, j: Any) -> Constraint:
    if (i in model.S_I_Production_Tasks) and (j in model.S_J_Executing_I[i]) and ((i,j) in model.P_Task_Unit_Network):
        return sum(model.V_Y_Start[i,j,n] for n in model.S_Time if n >= model.P_EST[i,j]) <= model.P_Upper_Bound_YS[i,j]
    else:
        return Constraint.Skip    


def constraint_upper_bound_ys_unit(model: ConcreteModel, j: Any) -> Constraint:
    return sum(model.V_Y_Start[i,j,n] for i in model.S_I_Production_Tasks if (i,j) in model.P_Task_Unit_Network for n in model.S_Time if n >= model.P_EST_Unit[j]) <= model.P_Upper_Bound_YS_Unit[j]
     

def constraint_upper_bound_x(model: ConcreteModel, i: Any, j: Any) -> Constraint:
    if (i in model.S_I_Production_Tasks) and (j in model.S_J_Executing_I[i]) and ((i,j) in model.P_Task_Unit_Network):
        return sum(model.V_X[i,j,n] for n in model.S_Time if n >= model.P_EST[i,j]) <= model.P_Upper_Bound_X[i,j]
    else:
        return Constraint.Skip
        
        
def constraint_upper_bound_x_unit(model: ConcreteModel, j: Any) -> Constraint:
    return sum(model.V_X[i,j,n] for i in model.S_I_Production_Tasks if (i,j) in model.P_Task_Unit_Network for n in model.S_Time if n >= model.P_EST_Unit[j]) <= model.P_Upper_Bound_X_Unit[j]
    
     
def create_constraints_est(model: ConcreteModel) -> None:
    
    model.C_EST_X_To_Zero = Constraint(model.S_Tasks, model.S_Units, rule = constraint_set_x_to_zero_est)
    model.C_EST_Upper_Bound_YS = Constraint(model.S_Tasks, model.S_Units, rule = constraint_upper_bound_ys)
    model.C_EST_Upper_Bound_YS_Unit = Constraint(model.S_Units, rule = constraint_upper_bound_ys_unit)
    model.C_Upper_Bound_X = Constraint(model.S_Tasks, model.S_Units, rule = constraint_upper_bound_x)
    model.C_Upper_Bound_X_Unit = Constraint(model.S_Units, rule = constraint_upper_bound_x_unit)
    