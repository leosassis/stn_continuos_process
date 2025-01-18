from pyomo.environ import *


#def initialize_variables(model):
    # V_X[i,j,n] = 1 if unit j processes (sub)task i at time point n.
#    model.V_X = Var(S_TASKS, S_UNITS, S_TIME, bounds = (0, 1), domain = Boolean)

    # V_Y_End[i,j,n] = 1 if a run of a continuous task in unit j ends at time point n.
#    model.V_Y_End = Var(S_TASKS, S_UNITS, S_TIME, bounds = (0, 1), domain = Boolean)

    # V_Y_Start[i,j,n] = 1 if a run of a continuous task in unit j starts at time point n.
#    model.V_Y_Start = Var(S_TASKS, S_UNITS, S_TIME, bounds = (0, 1), domain = Boolean)

    # V_B[i,j,n] is the batch size assigned to task i in unit j at time n.
 #   model.V_B = Var(S_TASKS, S_UNITS, S_TIME, domain = NonNegativeReals)

    # V_S[k,n] is the inventory of material k in time n.
  #  model.V_S = Var(S_MATERIALS, S_TIME, domain = NonNegativeReals)

    # V_X_Hat[i,j,n] is 1 if unit j is in task mode i (ready to execute batch subtaks i_SB(i)) at time point n.
   # model.V_X_Hat = Var(S_TASKS, S_UNITS, S_TIME, bounds = (0, 1), domain = Boolean)

    # V_X_Hat_Idle[j,n] is 1 if unit j is in idle mode at time point n.
    #model.V_X_Hat_Idle = Var(S_UNITS, S_TIME, bounds = (0, 1), domain = Boolean)

#    model.V_N_Unit = Var(S_UNITS, domain = Integers)
