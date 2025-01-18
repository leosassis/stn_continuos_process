from pyomo.environ import *

######################################
#               EST-LT               #
######################################

#model.P_Psi_Maximum_Amount_Material_Available = Param(S_MATERIALS, S_TIME, mutable = True, initialize = 0)
#model.P_Xi_Cumulative_Production_Task_In_Unit = Param(S_I_Production_Tasks, S_UNITS, S_TIME, mutable = True, initialize = 0)
#model.P_Phi_Total_Cumulative_Production_Task = Param(S_I_Production_Tasks, S_TIME, mutable = True, initialize = 0)
#model.P_EST_Task_Unit = Param(S_I_Production_Tasks, S_UNITS, mutable = True, initialize = 0)
#model.P_EST_Unit = Param(S_UNITS, mutable = True, initialize = 0)

#def est_lt(model):
    
#    #This is done to initialize (first P_Tau[i,j] periods) parameters that depend on t-P_Tau[i,j]. 
#    for n in S_TIME:
#        for k in S_MATERIALS:            
#            
#            model.P_Psi_Maximum_Amount_Material_Available[k,n].value = STATES[k]['initial']
#
#            for i in S_I_Production_Tasks:
#                for j in S_UNITS:
#                    if k in S_K_CONSUMED_BY_I[i] and (i,j) in P_TASK_UNIT and n <= P_Tau[i,j] and (STATES[k]['isRM'] == True):
#                        model.P_Xi_Cumulative_Production_Task_In_Unit[i,j,n].value = P_Bmax[i,j]
#                    
#    for n in S_TIME:        
#        for k in S_MATERIALS:            
#                if (n >= min(P_Tau[i,j] for i in S_I_Production_Tasks for j in S_UNITS if (i,j) in P_TASK_UNIT)) and (STATES[k]['isIntermed'] == True or STATES[k]['isProd'] == True):
#                    
#                    model.P_Psi_Maximum_Amount_Material_Available[k,n].value = (sum(P_rho_PLUS[i,k] * min(
#                                                                                                            (sum(model.P_Xi_Cumulative_Production_Task_In_Unit[i,j,n-P_Tau[i,j]].value for j in S_J_Executing_I[i])), 
#                                                                                                            (model.P_Phi_Total_Cumulative_Production_Task[i,n-min(P_Tau[i,j] for j in S_J_Executing_I[i])].value)
#                                                                                                         ) for i in (S_I_PRODUCING_K[k] & S_I_Production_Tasks))
#                                                                                )
#        for i in S_I_Production_Tasks:
#            for j in S_UNITS:
#                if (i,j) in P_TASK_UNIT: 
#                    if n >= P_Tau[i,j]:
#                        
#                        model.P_Xi_Cumulative_Production_Task_In_Unit[i,j,n].value = min( 
#                                                                                            min((-model.P_Psi_Maximum_Amount_Material_Available[k,n].value / P_rho_MINUS[i,k]) for k in S_K_CONSUMED_BY_I[i]), 
#                                                                                            (model.P_Xi_Cumulative_Production_Task_In_Unit[i,j,n-P_Tau[i,j]].value + P_Bmax[i,j])
#                                                                                        )
#                        
#                        model.P_Xi_Cumulative_Production_Task_In_Unit[i,j,n].value = model.P_Xi_Cumulative_Production_Task_In_Unit[i,j,n].value if model.P_Xi_Cumulative_Production_Task_In_Unit[i,j,n].value >= P_Bmin[i,j] else 0
#    
#            model.P_Phi_Total_Cumulative_Production_Task[i,n].value = min( 
#                                                                           min(
#                                                                                (-model.P_Psi_Maximum_Amount_Material_Available[k,n].value / P_rho_MINUS[i,k]) for k in S_K_CONSUMED_BY_I[i]), 
#                                                                                sum(model.P_Xi_Cumulative_Production_Task_In_Unit[i,j,n].value for j in S_J_Executing_I[i]) 
#                                                                         )
#    
#    for i in S_I_Production_Tasks:
#        for j in S_UNITS:
#                for n in S_TIME:
#                    if model.P_Xi_Cumulative_Production_Task_In_Unit[i, j, n].value > 0 and (i,j) in P_TASK_UNIT:
#                        model.P_EST_Task_Unit[i,j].value = n
#                        model.P_EST_Unit[j].value = n
#                        
#                        break
#                    else:
#                        model.P_EST_Task_Unit[i,j].value = None
#                        model.P_EST_Unit[j].value = n



    
#    model.P_Psi_Maximum_Amount_Material_Available.display()
#    model.P_Xi_Cumulative_Production_Task_In_Unit.display()    
#    model.P_Phi_Total_Cumulative_Production_Task.display()
#    model.P_EST_Task_Unit.display()
#    model.P_EST_Unit.display()


#est_lt(model)

""" model.I_Exp = Set()  # Tasks that have been explored.
model.K_Exp = Set()  # Material that have been explored.
model.theta = Param(S_TASKS, S_UNITS, mutable = True, initialize = H)  # Operational time windown for each (i,j).
model.omega = Param(S_MATERIALS, mutable = True, initialize = 0)  # Propagated inventory.
model.mu = Param(S_TASKS, mutable = True, initialize = 0)  # Total production of task i within a planning horizon.       
model.mu_tw = Param(S_TASKS, mutable = True, initialize = 0)  # Total production of task in a time windown.
model.mu_adjusted = Param(S_TASKS, mutable = True, initialize = 0)  # Adjusted value of mu due to production intervals. 
model.epsilon_max = Param(S_UNITS, mutable = True, initialize = 0)  # Maximum number of runs in a unit

 """

""" def foward_propagation(model):
    
    # Initialize omega with initial inventories and k and i to control elements to be explored.
    print("---------------------------------INITIALIZATION-------------------------------------------")
    print("Initialize omega with initial inventories.")
    print("Initialize sets Iexp and Kexp for materials with initial inventories and tasks that consume them.")
    
    for k in S_MATERIALS:
        
        if STATES[k]['initial'] > 0:
            model.omega[k] = STATES[k]['initial']
            print(f"Omega[{k}] = {model.omega[k].value}.")
            model.K_Exp.add(k)
            
            #for i in (S_I_CONSUMING_K[k] & S_I_Production_Tasks):
            #    model.I_Exp.add(i)    

    print(f"K_exp = {model.K_Exp.data()}.")
    print(f"I_exp = {model.I_Exp.data()}.")        
    print("------------------------------------------------------------------------------------------\n")
           
    for k in S_MATERIALS: 
        
        # Calculate batch combinations and capacities
        batch_combinations = {}
        combined_capacities = {}
        best_difference = float('inf')
        
        if k in model.K_Exp:
            
            for i in (S_I_CONSUMING_K[k] & S_I_Production_Tasks):
                print(f"\n\n\t------------------------------Max Prod. {i}-{k}------------------------------\n")

                # To Do: this for tasks without SU, SD, ST. Add them latter
                # To Do: what if I have less raw material then my production capacity

                model.mu_tw[i] = min( (model.omega[k].value), sum(P_rho_MINUS[i,k]*P_Tau_Max[i,j]*P_Bmax[i,j]*floor(model.theta[i,j].value/(P_Tau[i,j]*P_Tau_Max[i,j])) for j in S_J_Executing_I[i]))    
                model.mu[i] = model.mu_tw[i]

                print(f"\tTotal production of {i} in a time windows mu_tw = {model.mu_tw[i].value}")
                print(f"\tTotal production of {i} in the planning horizon mu = {model.mu[i].value}")

                for j in S_J_Executing_I[i]:
                    print(f"\n\t\t-------------------Max Number Runs {j}-{i}-------------------")
                    
                    model.epsilon_max[j] = ceil(model.mu[i] / (P_Tau_Max[i,j]*P_Bmax[i,j]))
                    print(f"\t\t#Maximum number of runs in unit {j} epsilon_max = {model.epsilon_max[j].value}")

                print("\n")

                max_runs = [range(0, value(model.epsilon_max[j]) + 1) for j in S_J_Executing_I[i]]
                combinations = list(product(*max_runs))
                batch_combinations[i] = combinations

                combined_capacities[i] = {
                    combo: {
                        'min_capacity': sum(P_Tau_Min[i,j] * P_Bmin[i,j] * combo[c] for (c,j) in enumerate(S_J_Executing_I[i])),
                        'max_capacity': sum(P_Tau_Max[i,j] * P_Bmax[i,j] * combo[c] for (c,j) in enumerate(S_J_Executing_I[i]))
                    }
                    for combo in combinations
                }  
                
                #for combo in combinations:
                    #for c, j in enumerate(S_J_Executing_I[i]):
                        #print(f"\tTask {i}, c: {c}, j: {j}, production combination = {combo[c]} runs")
                
                for combo, capacities in combined_capacities[i].items():
                    min_capacity = capacities['min_capacity']
                    max_capacity = capacities['max_capacity']
            
                    # Check if mu is within the range
                    if min_capacity <= model.mu[i].value <= max_capacity:
                        model.mu_adjusted[i] = model.mu[i].value  # Return immediately if a match is found
                        #print(f"\tBounded by max capacity = {max_capacity}")
                        break

                    # Otherwise, find the closest max_capacity
                    if abs(max_capacity - model.mu[i].value) < best_difference and max_capacity <= model.mu[i].value:
                        best_difference = abs(max_capacity - model.mu[i].value)
                        model.mu_adjusted[i] = max_capacity
                                        
                print("\n")

                print(f"\tTask {i} has the following production intervals:")
                for combo, capacities in combined_capacities[i].items():
                    print(f"\t\tCombination: {combo} -> Min: {capacities['min_capacity']}, Max: {capacities['max_capacity']}")

                print(f"\tThe calculated mu for task {i} is: {model.mu[i].value}. Its adjusted mu for {i} is: {model.mu_adjusted[i].value}")
            
                model.I_Exp.add(i)  

        for i in model.I_Exp:
            for k in S_K_PRODUCED_BY_I[i]:
                model.K_Exp.add(k)
        print(f"K_exp = {model.K_Exp.data()}.")
        
        for k in model.K_Exp:
            if model.omega[k].value == 0:
                model.omega[k] = min(sum(P_rho_PLUS[i,k] * model.mu_adjusted[i].value for i in (S_I_PRODUCING_K[k] & model.I_Exp)), max(model.mu_adjusted[i].value for i in (S_I_PRODUCING_K[k] & model.I_Exp)))
                print(f"The inventory propagate for material {k} is {model.omega[k].value}.")

        if model.K_Exp == S_MATERIALS and model.I_Exp == (S_I_Production_Tasks):
            print('All materials and tasks have been explored.')
            break


foward_propagation(model) """
