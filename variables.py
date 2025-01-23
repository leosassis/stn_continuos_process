from pyomo.environ import *

def create_variables(model):
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


def init_variables(model, H):
    [model.V_X_Hat[i,j,n].fix(0) for i in model.S_Tasks for j in model.S_Units for n in model.S_Time if n < H] #Variable model.V_X_Hat seams to have effect on the model.
    [model.V_X[i,j,n].fix(0) for i in model.S_Tasks for j in model.S_Units for n in model.S_Time if n >= H-1] #On the last period it can be maximum Y_End = 0.
    [model.V_X['TA1',j,n].fix(1) for j in model.S_Units for n in model.S_Time if n == 0] #Initialization. TA1 is the first task to reveice feed.
