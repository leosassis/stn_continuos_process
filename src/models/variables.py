from pyomo.environ import *


def create_variables(model: ConcreteModel) -> None:
    """ 
    Creates model variables.
    """
    
    # V_X[i,j,n] = 1 if unit j processes (sub)task i at time point n.
    model.V_X = Var(model.S_Tasks, model.S_Units, model.S_Time, bounds = (0, 1), domain = Binary)

    # V_Y_End[i,j,n] = 1 if a run of a continuous task in unit j ends at time point n.
    model.V_Y_End = Var(model.S_Tasks, model.S_Units, model.S_Time, bounds = (0, 1), domain = Binary)

    # V_Y_Start[i,j,n] = 1 if a run of a continuous task in unit j starts at time point n.
    model.V_Y_Start = Var(model.S_Tasks, model.S_Units, model.S_Time, bounds = (0, 1), domain = Binary)

    # V_B[i,j,n] is the batch size assigned to task i in unit j at time n.
    model.V_B = Var(model.S_Tasks, model.S_Units, model.S_Time, domain = NonNegativeReals)

    # V_S[k,n] is the inventory of material k in time n.
    model.V_S = Var(model.S_Materials, model.S_Time, domain = NonNegativeReals)

    # V_X_Hat[i,j,n] is 1 if unit j is in task mode i (ready to execute batch subtaks i_SB(i)) at time point n.
    model.V_X_Hat = Var(model.S_Tasks, model.S_Units, model.S_Time, bounds = (0, 1), domain = Binary)

    # V_X_Hat_Idle[j,n] is 1 if unit j is in idle mode at time point n.
    model.V_X_Hat_Idle = Var(model.S_Units, model.S_Time, bounds = (0, 1), domain = Binary)
    
    # V_EST[i,j] is the variable start time bounded by parameter P_EST[i,j]
    #model.V_EST = Var(model.S_Tasks, model.S_Units, domain = NonNegativeReals)

    # V_ST[i,j] is the variable shortest tail bounded by parameter P_ST[i,j]
    #model.V_ST = Var(model.S_Tasks, model.S_Units, domain = NonNegativeReals)


def init_variables(model: ConcreteModel, H: int) -> None:
    """ 
    Fixes values for variables.
    """
    
    #Variable model.V_X_Hat seams to have effect on the model.
    [model.V_X_Hat[i,j,n].fix(0) for i in model.S_Tasks for j in model.S_Units for n in model.S_Time if n < H] 
    
    #On the last period it can be maximum Y_End = 1.
    #[model.V_X[i,j,n].fix(0) for i in (model.S_Tasks - model.S_I_Shutdown_Tasks) for j in model.S_J_Executing_I[i] for n in model.S_Time if n >= H - model.P_Tau[i,j]] 
    #[model.V_X[i,j,n].fix(0) for i in (model.S_Tasks - model.S_I_Shutdown_Tasks) for j in model.S_J_Executing_I[i] for n in model.S_Time if n >= H - model.P_Tau[i,j] + 1] 
    [model.V_X[i,j,n].fix(0) for i in (model.S_Tasks - model.S_I_Shutdown_Tasks) for j in model.S_J_Executing_I[i] for n in model.S_Time if n >= H - model.P_Tau[i,j] + 1] 
        
    #Initialization. TA1 (no transitions) is the first task to reveice feed.
    #[model.V_X['TA1',j,n].fix(1) for j in model.S_Units for n in model.S_Time if n == 0] 
        
    #Y_End = 0 for the first taumin periods.
    #[model.V_Y_End[i,j,n].fix(0) for i in model.S_I_Production_Tasks for j in model.S_J_Executing_I[i] for n in model.S_Time if n < model.P_Tau_Min[i,j]] 
    
    #Y_Start = 0 for the last taumin periods.
    #[model.V_Y_Start[i,j,n].fix(0) for i in model.S_I_Production_Tasks for j in model.S_J_Executing_I[i] for n in model.S_Time if n > H - model.P_Tau_Min[i,j]] 
    
    #X = 0 for the last tau periods related to transitions.
    #[model.V_X[i,j,n].fix(0) for i in (model.S_I_Shutdown_Tasks | model.S_I_Direct_Transition_Tasks) for j in model.S_J_Executing_I[i] for n in model.S_Time if n >= H - model.P_Tau[i,j]] 

    #Feasibility check
    #[model.V_X[i,j,n].fix(0.1) for i in (model.S_Tasks) for j in model.S_J_Executing_I[i] for n in model.S_Time if i == 'TB1' if j == 'UA3' if n == 3] 
    