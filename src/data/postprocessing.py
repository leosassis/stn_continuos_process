
""" results_list = []
    if (results.solver.termination_condition != TerminationCondition.infeasible):
                    
            num_total_vars, num_binary_vars, num_constraints = compute_num_variables_constraints(model)
            objective_value = get_objective_value(model, STN)
            termination_condition = results.solver.termination_condition
            total_production = compute_total_production(model)
            
            #Solve LP relaxation.
            solver = SolverFactory('gurobi')
            set_solver_options_relaxation(solver, model)
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