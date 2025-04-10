from pyomo.environ import *

def if_start_end(model, i, j, n):
    if (i in model.S_I_Production_Tasks) and j in model.S_J_Executing_I[i] and (n <= (len(model.S_Time) - 1) - model.P_Tau_Max[i,j]):
        return sum(model.V_Y_End[i,j,nprime] for nprime in model.S_Time if nprime >= n + model.P_Tau_Min[i,j] and nprime <= n + model.P_Tau_Max[i,j]) >= model.V_Y_Start[i,j,n]
    else:
        return Constraint.Skip


def max_lenght_run_eq19_reformulation_YS(model, i, j, n):
    if (i,j) in model.P_Task_Unit_Network and i in model.S_I_Production_Tasks:
        return model.V_X[i,j,n] <= sum(model.V_Y_Start[i,j,nprime] for nprime in model.S_Time if ( (nprime >= n - model.P_Tau_Max[i,j] + 1) and (nprime <= n) )) 
    else:
        return Constraint.Skip


def max_lenght_run_eq19_reformulation_YE(model, i, j, n):
    if (i,j) in model.P_Task_Unit_Network and i in model.S_I_Production_Tasks:
        return model.V_X[i,j,n] <= sum(model.V_Y_End[i,j,nprime] for nprime in model.S_Time if ( (nprime >= n + 1) and (nprime <= n + model.P_Tau_Max[i,j]) )) 
    else:
        return Constraint.Skip


def forward_propagation_inequality(model, i):
    if (i in model.S_I_Production_Tasks): 
        return sum(model.V_B[i,j,n] for n in model.S_Time for j in model.S_J_Executing_I[i] if (i,j) in model.P_Task_Unit_Network) <= model.mu_adjusted[i]        
    else:
        return Constraint.Skip


def est_constraint_x_to_zero(model, i, j):
    if (i in model.S_I_Production_Tasks) and (j in model.S_J_Executing_I[i]) and ((i,j) in model.P_Task_Unit_Network) and (model.P_EST[i,j] > 0):
        return sum(model.V_X[i,j,n] for n in model.S_Time if (n >= 0 and n <= (model.P_EST[i,j] - 1))) == 0
    else:
        return Constraint.Skip


def st_constraint_x_to_zero(model, i, j):
    if (i in model.S_I_Production_Tasks) and (j in model.S_J_Executing_I[i]) and ((i,j) in model.P_Task_Unit_Network) and (model.P_ST[i,j] > 0):
        return sum(model.V_X[i,j,n] for n in model.S_Time if (n >= max(model.S_Time) - model.P_ST[i,j] and n <= max(model.S_Time))) == 0
    else:
        return Constraint.Skip


def est_constraint_upper_bound_number_of_runs(model, i, j):
    if (i in model.S_I_Production_Tasks) and (j in model.S_J_Executing_I[i]) and ((i,j) in model.P_Task_Unit_Network):
        return sum(model.V_Y_Start[i,j,n] for n in model.S_Time) <= floor((max(model.S_Time) + 1 - model.P_EST[i,j] - model.P_ST[i,j])/(model.P_Tau_Min[i,j] + model.P_Tau_End_Task[i]))
    else:
        return Constraint.Skip    


def est_constraint_upper_bound_number_of_runs_unit(model, j):
    return sum(model.V_Y_Start[i,j,n] for i in model.S_I_Production_Tasks if (i,j) in model.P_Task_Unit_Network for n in model.S_Time) <= floor((max(model.S_Time) + 1 - model.P_EST_Unit[j] - model.P_ST_Unit[j])/(min(model.P_Tau_Min[i,j] for i in model.S_I_Production_Tasks if (i,j) in model.P_Task_Unit_Network) + model.P_Tau_End_Unit[j]))
     
     
def lower_bound_est_variables(model, i, j):
    if (i in model.S_I_Production_Tasks) and (j in model.S_J_Executing_I[i]) and ((i,j) in model.P_Task_Unit_Network) and ((i,j) in model.P_EST):
        return model.V_EST[i,j] >= model.P_EST[i,j]     
    else:
        return Constraint.Skip


def lower_bound_st_variables(model, i, j):
    if (i in model.S_I_Production_Tasks) and (j in model.S_J_Executing_I[i]) and ((i,j) in model.P_Task_Unit_Network) and ((i,j) in model.P_ST):
        return model.V_ST[i,j] >= model.P_ST[i,j]     
    else:
        return Constraint.Skip
    

def est_constraint_upper_bound_number_of_runs_dynamic_est(model, i, j):
    if (i in model.S_I_Production_Tasks) and (j in model.S_J_Executing_I[i]) and ((i,j) in model.P_Task_Unit_Network) and ((i,j) in model.P_EST):
        return sum(model.V_Y_Start[i,j,n] for n in model.S_Time) <= ((max(model.S_Time) + 1 - model.V_EST[i,j])/(model.P_Tau_Min[i,j] - model.P_Tau_End_Task[i]))
    else:
        return Constraint.Skip    


def subsequent_tasks_dynamic_est(model, i, ii, j, jj, k):
    if ((i in model.S_I_Production_Tasks) and (j in model.S_J_Executing_I[i]) and ((i,j) in model.P_Task_Unit_Network) 
    and (ii in model.S_I_Production_Tasks) and (jj in model.S_J_Executing_I[ii]) and ((ii,jj) in model.P_Task_Unit_Network) and (len(model.S_J_Executing_I[ii]) == 1)
    and (k in (model.S_K_Consumed_I[i] & model.S_K_Produced_I[ii])) and (len(model.S_I_Producing_K[k]) == 1)): 
        return model.V_EST[i,j] >= model.V_EST[ii,jj] + max(1, 
                                                              (  ceil( model.P_Tau_Max[ii,jj] * (model.P_Tau_Min[i,j]*model.P_Beta_Min[i,j]) / (model.P_Tau_Max[ii,jj] * model.P_Beta_Max[ii,jj]) ) 
                                                               + ceil( model.P_Tau_End_Task[ii] * (model.P_Tau_Min[i,j]*model.P_Beta_Min[i,j]) / (model.P_Tau_Max[ii,jj] * model.P_Beta_Max[ii,jj]) ) 
                                                               - model.P_Tau_End_Task[ii] + 1 - model.P_Tau_Min[i,j] ) )
    else:
        return Constraint.Skip
    

def create_tightening_constraints(model, STN, H):
   
    STATES = STN['STATES']
    STATES_SHIPMENT = STN['STATES_SHIPMENT']
    ST_ARCS = STN['ST_ARCS']
    TS_ARCS = STN['TS_ARCS']
    UNIT_TASKS = STN['UNIT_TASKS']
    #TIME = STN['TIME']
    TASKS_TRANSITION_TASKS = STN['TASKS_TRANSITION_TASKS']
    H = H

    #model.If_Start_End = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = if_start_end)
    #model.C_Max_Lenght_Run_Reformulation_YS_Eq19 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = max_lenght_run_eq19_reformulation_YS) 
    #model.C_Max_Lenght_Run_Reformulation_YE_Eq19 = Constraint(model.S_Tasks, model.S_Units, model.S_Time, rule = max_lenght_run_eq19_reformulation_YE) 

    #Tightening Constraints EST - Static
    #model.C_EST_X_To_Zero = Constraint(model.S_Tasks, model.S_Units, rule = est_constraint_x_to_zero)
    #model.C_ST_X_To_Zero = Constraint(model.S_Tasks, model.S_Units, rule = st_constraint_x_to_zero)
    #model.C_EST_Upper_Bound_Number_Runs = Constraint(model.S_Tasks, model.S_Units, rule = est_constraint_upper_bound_number_of_runs)
    #model.C_EST_Upper_Bound_Number_Runs_Unit = Constraint(model.S_Units, rule = est_constraint_upper_bound_number_of_runs_unit)
    
    #Tightening Constraints EST - Dynamic
    #model.C_Lower_Bound_EST_Dynamic = Constraint(model.S_Tasks, model.S_Units, rule = lower_bound_est_variables)
    #model.C_Lower_Bound_ST_Dynamic = Constraint(model.S_Tasks, model.S_Units, rule = lower_bound_st_variables)
    #model.C_Upper_Bound_Number_Runs_EST_Dynamic = Constraint(model.S_Tasks, model.S_Units, rule = est_constraint_upper_bound_number_of_runs_dynamic_est)
    
    #Tightening Constraints EST - Dynamic - Subsequent Tasks
    #model.C_Subsequent_Tasks_Dynamic_EST = Constraint(model.S_Tasks, model.S_Tasks, model.S_Units, model.S_Units, model.S_Materials, rule = subsequent_tasks_dynamic_est)
    
    #############################################
    #  network_8_fast_upstream_slow_downstream  #
    #############################################
    
    #Tightening Constraints EST - Dynamic - Same Material - network_8_fast_upstream_slow_downstream
    #model.EST_Same_Material_1 = Constraint(expr = model.V_EST['TB1','UA3'] + model.V_EST['TB2','UA3'] >= 2*model.V_EST['TA1','UA1'] + 4)
    #model.EST_Same_Material_2 = Constraint(expr = model.V_EST['TB3','UA4'] + model.V_EST['TB4','UA4'] >= 2*model.V_EST['TA2','UA2'] + 4)
    #model.EST_Same_Material_3 = Constraint(expr = model.V_EST['TC3','UA6'] + model.V_EST['TC4','UA6'] >= 2*model.V_EST['TB4','UA4'] + 3)
    #model.EST_Same_Material_4 = Constraint(expr = model.V_EST['TC1','UA7'] + model.V_EST['TC2','UA7'] >= 2*model.V_EST['TB1','UA3'] + 3)
    
    #Tightening Constraints EST - Dynamic - Same Unit - network_8_fast_upstream_slow_downstream
    #model.EST_Same_Unit_1 = Constraint(expr = model.V_EST['TB1','UA3'] + model.V_EST['TB2','UA3'] >= 2*model.V_EST['TA1','UA1'] + 2 + 6)    
    #model.EST_Same_Unit_2 = Constraint(expr = model.V_EST['TB3','UA4'] + model.V_EST['TB4','UA4'] >= 2*model.V_EST['TA2','UA2'] + 2 + 6)    
    #model.EST_Same_Unit_3 = Constraint(expr = model.V_EST['TC1','UA7'] + model.V_EST['TC2','UA7'] >= 2*model.V_EST['TB1','UA3'] + 2 + 7)    
    #model.EST_Same_Unit_4 = Constraint(expr = model.V_EST['TC3','UA6'] + model.V_EST['TC4','UA6'] >= 2*model.V_EST['TB4','UA4'] + 2 + 7)    
    #model.EST_Same_Unit_5 = Constraint(expr = model.V_EST['TC5','UA5'] + model.V_EST['TC6','UA5'] >= model.V_EST['TB2','UA3'] + model.V_EST['TB3','UA4'] + 2 + 7)    
    
    #############################################
    #              network_10_dow               #
    #############################################   
    
    #Tightening Constraints EST - Dynamic - Same Unit - network_10_dow
    #model.EST_Same_Unit_1 = Constraint(expr = model.V_EST['TA1','UA1'] + model.V_EST['TA2','UA1'] + model.V_EST['TA3','UA1'] >= 21)    
    #model.EST_Same_Unit_2 = Constraint(expr = model.V_EST['TB1','UA2'] + model.V_EST['TB2','UA2'] + model.V_EST['TB3','UA2'] >= model.V_EST['TA1','UA1'] + model.V_EST['TA2','UA1'] + model.V_EST['TA3','UA1'] + 3)    
    #model.EST_Same_Unit_3 = Constraint(expr = model.V_EST['TC1','UA3'] + model.V_EST['TC2','UA3'] + model.V_EST['TC3','UA3'] >= model.V_EST['TB1','UA2'] + model.V_EST['TB2','UA2'] + model.V_EST['TB3','UA2'] + 3)
    #model.EST_Same_Unit_4 = Constraint(expr = model.V_EST['TD1','UA4'] + model.V_EST['TD2','UA4'] + model.V_EST['TD3','UA4'] >= model.V_EST['TC1','UA3'] + model.V_EST['TC2','UA3'] + model.V_EST['TC3','UA3'] + 3)
    #model.EST_Same_Unit_5 = Constraint(expr = model.V_EST['TE1','UA5'] + model.V_EST['TE2','UA5'] + model.V_EST['TE3','UA5'] >= model.V_EST['TD1','UA4'] + model.V_EST['TD2','UA4'] + model.V_EST['TD3','UA4'] + 3)
    #model.EST_Same_Unit_6 = Constraint(expr = model.V_EST['TF1','UA6'] + model.V_EST['TF2','UA6'] + model.V_EST['TF3','UA6'] >= model.V_EST['TE1','UA5'] + model.V_EST['TE2','UA5'] + model.V_EST['TE3','UA5'] + 3)
    
    #model.ST_Same_Unit_1 = Constraint(expr = model.V_ST['TA1','UA1'] + model.V_ST['TA2','UA1'] + model.V_ST['TA3','UA1'] >= 21+15)    
    #model.ST_Same_Unit_2 = Constraint(expr = model.V_ST['TB1','UA2'] + model.V_ST['TB2','UA2'] + model.V_ST['TB3','UA2'] >= 9+12)    
    #model.ST_Same_Unit_3 = Constraint(expr = model.V_ST['TC1','UA3'] + model.V_ST['TC2','UA3'] + model.V_ST['TC3','UA3'] >= 9+9)
    #model.ST_Same_Unit_4 = Constraint(expr = model.V_ST['TD1','UA4'] + model.V_ST['TD2','UA4'] + model.V_ST['TD3','UA4'] >= 9+6)
    #model.ST_Same_Unit_5 = Constraint(expr = model.V_ST['TE1','UA5'] + model.V_ST['TE2','UA5'] + model.V_ST['TE3','UA5'] >= 9+3)
    #model.ST_Same_Unit_6 = Constraint(expr = model.V_ST['TF1','UA6'] + model.V_ST['TF2','UA6'] + model.V_ST['TF3','UA6'] >= 9)
    
    #model.ST_Same_Unit_1 = Constraint(expr = sum(model.V_Y_Start['TA1','UA1',n] for n in model.S_Time) + sum(model.V_Y_Start['TA2','UA1',n] for n in model.S_Time) + sum(model.V_Y_Start['TA3','UA1',n] for n in model.S_Time) <= floor((max(model.S_Time)+1-5)/7))    
    #model.ST_Same_Unit_2 = Constraint(expr = sum(model.V_Y_Start['TB1','UA2',n] for n in model.S_Time) + sum(model.V_Y_Start['TB2','UA2',n] for n in model.S_Time) + sum(model.V_Y_Start['TB3','UA2',n] for n in model.S_Time) <= floor((max(model.S_Time)+1-1-4)/3))    
    #model.ST_Same_Unit_3 = Constraint(expr = sum(model.V_Y_Start['TC1','UA3',n] for n in model.S_Time) + sum(model.V_Y_Start['TC2','UA3',n] for n in model.S_Time) + sum(model.V_Y_Start['TC3','UA3',n] for n in model.S_Time) <= floor((max(model.S_Time)+1-2-3)/3))
    #model.ST_Same_Unit_4 = Constraint(expr = sum(model.V_Y_Start['TD1','UA4',n] for n in model.S_Time) + sum(model.V_Y_Start['TD2','UA4',n] for n in model.S_Time) + sum(model.V_Y_Start['TD3','UA4',n] for n in model.S_Time) <= floor((max(model.S_Time)+1-3-2)/3))
    #model.ST_Same_Unit_5 = Constraint(expr = sum(model.V_Y_Start['TE1','UA5',n] for n in model.S_Time) + sum(model.V_Y_Start['TE2','UA5',n] for n in model.S_Time) + sum(model.V_Y_Start['TE3','UA5',n] for n in model.S_Time) <= floor((max(model.S_Time)+1-4-1)/3))
    #model.ST_Same_Unit_6 = Constraint(expr = sum(model.V_Y_Start['TF1','UA6',n] for n in model.S_Time) + sum(model.V_Y_Start['TF2','UA6',n] for n in model.S_Time) + sum(model.V_Y_Start['TF3','UA6',n] for n in model.S_Time) <= floor((max(model.S_Time)+1-5)/3))
    
    #model.Max_Prod_1_TA1 = Constraint(expr = sum(model.V_B['TA1','UA1',n] for n in model.S_Time) <= 480)
    #model.Max_Prod_1_TA2 = Constraint(expr = sum(model.V_B['TA2','UA1',n] for n in model.S_Time) <= 480)
    #model.Max_Prod_1_TA3 = Constraint(expr = sum(model.V_B['TA3','UA1',n] for n in model.S_Time) <= 480)
    
    #model.Max_Prod_1_TB1 = Constraint(expr = sum(model.V_B['TB1','UA2',n] for n in model.S_Time) <= 480)
    #model.Max_Prod_1_TB2 = Constraint(expr = sum(model.V_B['TB2','UA2',n] for n in model.S_Time) <= 480)
    #model.Max_Prod_1_TB3 = Constraint(expr = sum(model.V_B['TB3','UA2',n] for n in model.S_Time) <= 480)
    
    #model.Max_Prod_1_TC1 = Constraint(expr = sum(model.V_B['TC1','UA3',n] for n in model.S_Time) <= 480)
    #model.Max_Prod_1_TC2 = Constraint(expr = sum(model.V_B['TC2','UA3',n] for n in model.S_Time) <= 480)
    #model.Max_Prod_1_TC3 = Constraint(expr = sum(model.V_B['TC3','UA3',n] for n in model.S_Time) <= 480)
    
    #model.Max_Prod_1_TD1 = Constraint(expr = sum(model.V_B['TD1','UA4',n] for n in model.S_Time) <= 480)
    #model.Max_Prod_1_TD2 = Constraint(expr = sum(model.V_B['TD2','UA4',n] for n in model.S_Time) <= 480)
    #model.Max_Prod_1_TD3 = Constraint(expr = sum(model.V_B['TD3','UA4',n] for n in model.S_Time) <= 480)
    
    #model.Max_Prod_1_TE1 = Constraint(expr = sum(model.V_B['TE1','UA5',n] for n in model.S_Time) <= 480)
    #model.Max_Prod_1_TE2 = Constraint(expr = sum(model.V_B['TE2','UA5',n] for n in model.S_Time) <= 480)
    #model.Max_Prod_1_TE3 = Constraint(expr = sum(model.V_B['TE3','UA5',n] for n in model.S_Time) <= 480)
    
    #model.Max_Prod_1_TF1 = Constraint(expr = sum(model.V_B['TF1','UA6',n] for n in model.S_Time) <= 480)
    #model.Max_Prod_1_TF2 = Constraint(expr = sum(model.V_B['TF2','UA6',n] for n in model.S_Time) <= 480)
    #model.Max_Prod_1_TF3 = Constraint(expr = sum(model.V_B['TF3','UA6',n] for n in model.S_Time) <= 480)
    