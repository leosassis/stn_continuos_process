
##########################################################
#The current model has no utility constraints.           # 
#It assumes unlimited amount of raw materials            #
#It assume no delays: idis, idly, rmi_dly, rmi_n         #
#It assumes no batch units: j_b                          #
#There is no pre-defined tasks for n=0: i_ini            #
##########################################################
import pandas as pd
import time
import numpy as np
from pyomo.environ import *
from optimization import set_solver_options, solve_model, print_model_constraints, compute_num_variables_constraints, create_model
from utils import plot_gantt_chart, plot_inventory_chart, compute_product_production, compute_total_production
from fp import forward_propagation
from objective import get_objective_value

from network_7_slow_upstream_fast_downstream import define_stn_network
#from network_8_fast_upstream_slow_downstream import define_stn_network

results_list = []
H_Values = range(25, 26, 25)

for H in H_Values:
                
    STN = define_stn_network()
            
    model = ConcreteModel()
    create_model(model, STN, H)
                
    #Solve original model.
    solver = SolverFactory('gurobi')
    set_solver_options(solver, model, model_nature = 'original_model')
    start_time = time.time()
    results = solve_model(solver, model)
    end_time = time.time()
        
    """ if (results.solver.termination_condition != TerminationCondition.infeasible):
                
        num_total_vars, num_binary_vars, num_constraints = compute_num_variables_constraints(model)
        objective_value = get_objective_value(model, STN)
        termination_condition = results.solver.termination_condition
        total_production = compute_total_production(model)
        
        #Solve LP relaxation.
        solver = SolverFactory('gurobi')
        set_solver_options(solver, model, model_nature = 'relaxed_model')
        solve_model(solver, model)                
        lp_objective_value = get_objective_value(model, STN)
        total_production_relaxed = compute_total_production(model)
                        
    else:                
        objective_value = 0
        lp_objective_value = 0
        num_total_vars = 0
        num_binary_vars = 0
        num_constraints = 0
        termination_condition = results.solver.termination_condition
                    
    instance_name = f"H{H}"
        
    # Add results as a dictionary
    results_list.append({
        "Instance": instance_name,
        "Objective Function": objective_value,
        "LP Relaxation": lp_objective_value,
        "Gap %": 100*(lp_objective_value - objective_value)/lp_objective_value,
        "Solution Time (s)": end_time - start_time,
        "Termination Condition": termination_condition,
        "Number of Constraints": num_constraints,
        "Total Variables": num_total_vars,
        "Binary Variables": num_binary_vars,
        "Total Production": total_production,
        "Relaxed Production": total_production_relaxed,
        "Production Gap %": 100*(total_production_relaxed - total_production)/total_production_relaxed,
    })
        
    # Convert results list to DataFrame
    results_df = pd.DataFrame(results_list)

    # Save results to Excel
    results_df.to_excel("model_results_fp.xlsx", index=False) """
    
    #print_model_constraints(model)
    plot_gantt_chart(H, model)
    
    for i, j, n, in model.V_X:
        if model.V_X[i,j,n].value == 1:
            print(f"[{i}, {j}, {n}] = 1")