from pyomo.environ import *
from itertools import product

def forward_propagation(model, H):
    
    model.I_Exp = Set()  # Tasks that have been explored.
    model.K_Exp = Set()  # Material that have been explored.
    model.K_To_Be_Exp = Set()  # Material that have been explored.
    model.I_To_Be_Exp = Set()  # Material that have been explored.
    model.theta = Param(model.S_Tasks, model.S_Units, mutable = True, initialize = H)  # Operational time windown for each (i,j).
    model.omega = Param(model.S_Materials, mutable = True, initialize = -1000)  # Maximum cumulative production.
    model.mu = Param(model.S_Tasks, mutable = True, initialize = 0)  # Total production of task i within a planning horizon.       
    model.mu_tw = Param(model.S_Tasks, mutable = True, initialize = 0)  # Total production of task in a time windown.
    model.mu_adjusted = Param(model.S_Tasks, mutable = True, initialize = 0)  # Adjusted value of mu due to production intervals. 
    model.epsilon_max = Param(model.S_Units, mutable = True, initialize = 0)  # Maximum number of runs in a unit
    
    # Initialize omega with initial inventories and k and i to control elements to be explored.
    print("---------------------------------INITIALIZATION-------------------------------------------")
    print("Initialize omega with initial inventories.")
    print("Initialize sets I_exp and K_exp for materials with initial inventories and tasks that consume them.")
    model.K_To_Be_Exp.set_value(model.S_Materials)
    model.I_To_Be_Exp.set_value(model.S_Tasks & model.S_I_Production_Tasks)
    print(f"K_To_Be_Exp = {model.K_To_Be_Exp.data()}.")
    print(f"I_To_Be_Exp = {model.I_To_Be_Exp.data()}.")      
    
    for k in model.S_Materials:
        
        if model.P_Init_Inventory_Material[k] > 0:
            model.omega[k] = model.P_Init_Inventory_Material[k]
            print(f"Omega[{k}] = {model.omega[k].value}.")         
            model.K_Exp.add(k)   
    
    print(f"K_Exp = {model.K_Exp.data()}.") 
        
    print("----------------------------------------------------------------------------------------------------------\n")

    
    while model.K_Exp != model.S_Materials:
        for k in model.S_Materials: 
            
            # Calculate batch combinations and capacities
            batch_combinations = {}
            combined_capacities = {}
            best_difference = float('inf')
            
            if k in model.K_Exp:
                
                for i in (model.S_I_Consuming_K[k] & model.S_I_Production_Tasks):
                    print(f"\n\n\t------------------------------Mu-Max Cumulative Amount of {k} for {i}----------------------------------------------\n")

                    # To Do: this for tasks without SU, SD, ST. Add them latter
                    # To Do: what if I have less raw material then my production capacity

                    # Since we the floor to have an integer number of runs, this is necessary to catch situation where I can have more runs (and production) considering model.P_Tau_Min.
                    model.mu_tw[i] = min(model.omega[k].value, sum(model.P_Tau_Max[i,j]*model.P_Beta_Max[i,j]*floor(model.theta[i,j].value/(1+model.P_Tau[i,j]*model.P_Tau_Max[i,j])) for j in model.S_J_Executing_I[i]))    
                    model.mu[i] = model.mu_tw[i]

                    print(f"\tMax cumulative amount for {i} in a time windows mu_tw = {model.mu_tw[i].value}")
                    print(f"\tMax cumulative amount for {i} in the planning horizon mu = {model.mu[i].value}")

                    for j in model.S_J_Executing_I[i]:
                        print(f"\n\t\t-------------------Max Number Runs {j}-{i}-------------------")
                            
                        # To Do: define the right denominator (model.P_Tau_Max and/or model.P_Tau_Min)
                        # To Do: this for tasks without SU, SD, ST. Add them latter
                        model.epsilon_max[j] = ceil(model.mu[i] / (model.P_Tau_Max[i,j]*model.P_Beta_Max[i,j]))
                        print(f"\t\tMaximum number of runs of task {i} in unit {j} epsilon_max = {model.epsilon_max[j].value}")

                    print("\n")

                    print(f"\n\n\t------------------------------Checking Production Schemes of {k} for {i}------------------------------\n")
                        
                    max_runs = [range(0, value(model.epsilon_max[j]) + 1) for j in model.S_J_Executing_I[i]]
                    combinations = list(product(*max_runs))
                    batch_combinations[i] = combinations

                    combined_capacities[i] = {
                        combo: {
                            'min_capacity': sum(model.P_Tau_Min[i,j] * model.P_Beta_Min[i,j] * combo[c] for (c,j) in enumerate(model.S_J_Executing_I[i])),
                            'max_capacity': sum(model.P_Tau_Max[i,j] * model.P_Beta_Max[i,j] * combo[c] for (c,j) in enumerate(model.S_J_Executing_I[i]))
                        }
                        for combo in combinations
                    }  
                    
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

                    print(f"\tTask {i} has the following feasible production intervals:")
                    for combo, capacities in combined_capacities[i].items():
                        print(f"\t\tCombination: {combo} -> Min: {capacities['min_capacity']}, Max: {capacities['max_capacity']}")

                    print(f"\tThe calculated mu for task {i} is: {model.mu[i].value}. Its adjusted mu for {i} is: {model.mu_adjusted[i].value}")

                    # Track which tasks i consuming k have been explored
                    model.I_Exp.add(i)
                
                for i in model.I_Exp:
                    for k in model.S_K_Produced_I[i]:
                        model.K_Exp.add(k)
                print(f"K_exp = {model.K_Exp.data()}.")
                
                for k in model.K_Exp:
                    if model.omega[k].value < 0:
                        model.omega[k] = sum(model.mu_adjusted[i].value for i in (model.S_I_Producing_K[k] & model.I_Exp))
                        print(f"The maximum cumulative production (propagate inventory) for material {k} is {model.omega[k].value}.")

    model.omega.pprint()   