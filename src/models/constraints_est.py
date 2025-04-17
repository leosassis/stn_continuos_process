from pyomo.environ import *


def est_constraint_x_to_zero(model: ConcreteModel, i: Any, j: Any) -> Constraint:
    if (i in model.S_I_Production_Tasks) and (j in model.S_J_Executing_I[i]) and ((i,j) in model.P_Task_Unit_Network) and (model.P_EST[i,j] > 0):
        return sum(model.V_X[i,j,n] for n in model.S_Time if (n >= 0 and n <= (model.P_EST[i,j] - 1))) == 0
    else:
        return Constraint.Skip


def est_constraint_upper_bound_number_of_runs(model: ConcreteModel, i: Any, j: Any) -> Constraint:
    if (i in model.S_I_Production_Tasks) and (j in model.S_J_Executing_I[i]) and ((i,j) in model.P_Task_Unit_Network):
        return sum(model.V_Y_Start[i,j,n] for n in model.S_Time) <= floor((max(model.S_Time) + 1 - model.P_EST[i,j])/(model.P_Tau_Min[i,j] + model.P_Tau_End_Task[i]))
    else:
        return Constraint.Skip    


def est_constraint_upper_bound_number_of_runs_unit(model: ConcreteModel, j: Any) -> Constraint:
    return sum(model.V_Y_Start[i,j,n] for i in model.S_I_Production_Tasks if (i,j) in model.P_Task_Unit_Network for n in model.S_Time) <= floor((max(model.S_Time) + 1 - model.P_EST_Unit[j])/(min(model.P_Tau_Min[i,j] for i in model.S_I_Production_Tasks if (i,j) in model.P_Task_Unit_Network) + model.P_Tau_End_Unit[j]))
     

def upper_bound_x(model: ConcreteModel, i: Any, j: Any) -> Constraint:
    if (i in model.S_I_Production_Tasks) and (j in model.S_J_Executing_I[i]) and ((i,j) in model.P_Task_Unit_Network):
        return sum(model.V_X[i,j,n] for n in model.S_Time) <= model.P_Upper_Bound_X[i,j]
    else:
        return Constraint.Skip
        
def upper_bound_x_unit(model: ConcreteModel, j: Any) -> Constraint:
    return sum(model.V_X[i,j,n] for i in model.S_I_Production_Tasks if (i,j) in model.P_Task_Unit_Network for n in model.S_Time) <= model.P_Upper_Bound_X_Unit[j]
    
     
def create_constraints_est(model: ConcreteModel) -> None:
    
    model.C_EST_X_To_Zero = Constraint(model.S_Tasks, model.S_Units, rule = est_constraint_x_to_zero)
    model.C_EST_Upper_Bound_Number_Runs = Constraint(model.S_Tasks, model.S_Units, rule = est_constraint_upper_bound_number_of_runs)
    model.C_EST_Upper_Bound_Number_Runs_Unit = Constraint(model.S_Units, rule = est_constraint_upper_bound_number_of_runs_unit)
    model.C_Upper_Bound_X = Constraint(model.S_Tasks, model.S_Units, rule = upper_bound_x)
    model.C_Upper_Bound_X_Units = Constraint(model.S_Units, rule = upper_bound_x_unit)
    