from pyomo.environ import *


def if_start_end(model: ConcreteModel, i: Any, j: Any, n: Any) -> Constraint:
    if (i in model.S_I_Production_Tasks) and j in model.S_J_Executing_I[i] and (n <= (len(model.S_Time) - 1) - model.P_Tau_Max[i,j]):
        return sum(model.V_Y_End[i,j,nprime] for nprime in model.S_Time if nprime >= n + model.P_Tau_Min[i,j] and nprime <= n + model.P_Tau_Max[i,j]) >= model.V_Y_Start[i,j,n]
    else:
        return Constraint.Skip


def max_lenght_run_eq19_reformulation_YS(model: ConcreteModel, i: Any, j: Any, n: Any) -> Constraint:
    if (i,j) in model.P_Task_Unit_Network and i in model.S_I_Production_Tasks:
        return model.V_X[i,j,n] <= sum(model.V_Y_Start[i,j,nprime] for nprime in model.S_Time if ( (nprime >= n - model.P_Tau_Max[i,j] + 1) and (nprime <= n) )) 
    else:
        return Constraint.Skip


def max_lenght_run_eq19_reformulation_YE(model: ConcreteModel, i: Any, j: Any, n: Any) -> Constraint:
    if (i,j) in model.P_Task_Unit_Network and i in model.S_I_Production_Tasks:
        return model.V_X[i,j,n] <= sum(model.V_Y_End[i,j,nprime] for nprime in model.S_Time if ( (nprime >= n + 1) and (nprime <= n + model.P_Tau_Max[i,j]) )) 
    else:
        return Constraint.Skip
    
    
def create_constraints_test(model: ConcreteModel) -> None:
   
    model.If_Start_End = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = if_start_end)
    model.C_Max_Lenght_Run_Reformulation_YS_Eq19 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = max_lenght_run_eq19_reformulation_YS) 
    model.C_Max_Lenght_Run_Reformulation_YE_Eq19 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = max_lenght_run_eq19_reformulation_YE)     