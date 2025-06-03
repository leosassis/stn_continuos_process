from pyomo.environ import *


def create_variables(model: ConcreteModel) -> None:
    """ 
    Creates model variables.
    """
    
    # Binary: V_X[i,j,n] = 1 if unit j processes (sub)task i at time point n.
    model.V_X = Var(model.S_Tasks, model.S_Units, model.S_Time, bounds = (0, 1), domain = Binary)

    # Binary: V_Y_End[i,j,n] = 1 if a run of a continuous task in unit j ends at time point n.
    model.V_Y_End = Var(model.S_Tasks, model.S_Units, model.S_Time, bounds = (0, 1), domain = Binary)

    # Binary: V_Y_Start[i,j,n] = 1 if a run of a continuous task in unit j starts at time point n.
    model.V_Y_Start = Var(model.S_Tasks, model.S_Units, model.S_Time, bounds = (0, 1), domain = Binary)

    # Continuous: V_B[i,j,n] is the batch size assigned to task i in unit j at time n.
    model.V_B = Var(model.S_Tasks, model.S_Units, model.S_Time, domain = NonNegativeReals)

    # Continuous: V_S[k,n] is the inventory of material k in time n.
    model.V_S = Var(model.S_Materials, model.S_Time, domain = NonNegativeReals)

    # Binary: V_X_Hat[i,j,n] is 1 if unit j is in task mode i (ready to execute batch subtaks i_SB(i)) at time point n.
    model.V_X_Hat = Var(model.S_Tasks, model.S_Units, model.S_Time, bounds = (0, 1), domain = Binary)

    # Binary: V_X_Hat_Idle[j,n] is 1 if unit j is in idle mode at time point n.
    model.V_X_Hat_Idle = Var(model.S_Units, model.S_Time, bounds = (0, 1), domain = Binary)
    
    
def init_variables(model: ConcreteModel, H: int) -> None:
    """
    Fix initial values for selected decision variables.
    
    Args:
        - model: a Pyomo ConcreteModel object.
        - H: planning horizon.
    """
    
    
    # Fix task mode to zero before time point H
    [model.V_X_Hat[i,j,n].fix(0) for i in model.S_Tasks for j in model.S_Units for n in model.S_Time if n < H] 
    
    # The last time point n is reserved for Y_End = 1.
    [model.V_X[i,j,n].fix(0) for i in (model.S_Tasks - model.S_I_Shutdown_Tasks) for j in model.S_J_Executing_I[i] for n in model.S_Time if n >= H - model.P_Tau[i,j] + 1] 
        
    # OPTIONAL INITIALIZATION LOGIC (Uncomment as needed):    
        
    # Initial feed task: TA1 starts at n=0
    #[model.V_X['TA1',j,n].fix(1) for j in model.S_Units for n in model.S_Time if n == 0] 
        
    # Prevent task end in first tau_min periods
    #[model.V_Y_End[i,j,n].fix(0) for i in model.S_I_Production_Tasks for j in model.S_J_Executing_I[i] for n in model.S_Time if n < model.P_Tau_Min[i,j]] 
    
    # Prevent task start in last tau_min periods
    #[model.V_Y_Start[i,j,n].fix(0) for i in model.S_I_Production_Tasks for j in model.S_J_Executing_I[i] for n in model.S_Time if n > H - model.P_Tau_Min[i,j]] 
    
    # Prevent production operations during the last tau periods related to transitions
    #[model.V_X[i,j,n].fix(0) for i in (model.S_I_Shutdown_Tasks | model.S_I_Direct_Transition_Tasks) for j in model.S_J_Executing_I[i] for n in model.S_Time if n >= H - model.P_Tau[i,j]] 