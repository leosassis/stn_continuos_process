
##########################################################
#The current model has no utility constraints.           # 
#It assumes unlimited amount of raw materials            #
#It assume no delays: idis, idly, rmi_dly, rmi_n         #
#It assumes no batch units: j_b                          #
#There is no pre-defined tasks for n=0: i_ini            #
##########################################################

from pyomo.environ import *
from optimization import set_solver_options, solve_model, print_model_constraints
from sets import create_main_sets_parameters
from variables import create_variables, init_variables 
from parameters import create_parameters
from utils import plot_gantt_chart, plot_inventory_chart
from fp import forward_propagation
from objective import create_objective_function
from constraints import create_constraints, add_fp_constraint

#from network_0_v1 import *
#from network_0_v2 import *
from network_1_v1 import *
#from network_1_v2 import *
#from network_2 import *
#from network_3 import *

H = 15
STN = STN
model = ConcreteModel()
create_main_sets_parameters(model, STN, H)
create_variables(model)    
create_parameters(model, STN, H)
init_variables(model, H)
create_constraints(model, STN, H)
create_objective_function(model, STN)

try:
    
    forward_propagation(model, H)
    add_fp_constraint(model)
    solver = SolverFactory('gurobi')
    
    set_solver_options(solver, model, model_nature = 'original_model')
    solve_model(solver, model)
    
    total_production = sum(model.V_B[i,j,n].value for n in model.S_Time for k in model.S_Materials for i in model.S_I_Producing_K[k] for j in model.S_J_Executing_I[i] if (i,j) in model.P_Task_Unit_Network if k in model.S_Final_Products)
    
    #print_model_constraints(model)
    
    set_solver_options(solver, model, model_nature = 'relaxed_model')
    solve_model(solver, model)
    
    total_production_relaxed = sum(model.V_B[i,j,n].value for n in model.S_Time for k in model.S_Materials for i in model.S_I_Producing_K[k] for j in model.S_J_Executing_I[i] if (i,j) in model.P_Task_Unit_Network if k in model.S_Final_Products)
    
    print(f'Total production is = {total_production}')
    print(f'Total relaxed production is = {total_production_relaxed}')    

    #plot_gantt_chart(H, model)
    #plot_inventory_chart(H, model)
 
except:

    print(f"Error")