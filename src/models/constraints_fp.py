from pyomo.environ import *


def forward_propagation_inequality(model: ConcreteModel, i: Any) -> Constraint:
    if (i in model.S_I_Production_Tasks): 
        return sum(model.V_B[i,j,n] for n in model.S_Time for j in model.S_J_Executing_I[i] if (i,j) in model.P_Task_Unit_Network) <= model.mu_adjusted[i]        
    else:
        return Constraint.Skip


def create_constraints_fp(model: ConcreteModel) -> None:
   
    model.C_Forward_Propagation = Constraint(model.S_Tasks, rule = forward_propagation_inequality)   