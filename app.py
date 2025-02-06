
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
from constraints import create_constraints, add_fp_constraint, add_if_start_end, add_tau_max_reformulation_YS, add_tau_max_reformulation_YE

#from network_0_v1 import *
#from network_0_v2 import *
#from network_1_v1 import *
#from network_1_v2 import *
#from network_2 import *
#from network_3 import *

#from network_2 import define_stn_network
#from network_4 import define_stn_network
from network_6 import define_stn_network

H = 50
beta_min_factor = 0.75
tau_max_factor = 1
STN = define_stn_network(beta_min_factor, tau_max_factor)

model = ConcreteModel()
create_main_sets_parameters(model, STN, H)
create_variables(model)    
create_parameters(model, STN, H)
init_variables(model, H)
create_constraints(model, STN, H)
create_objective_function(model, STN, maximize, 'production_revenue')

try:
    #forward_propagation(model, H)
    solver = SolverFactory('gurobi')
    set_solver_options(solver, model, model_nature = 'original_model')
    solve_model(solver, model)
    
    print_model_constraints(model)
    for i in model.S_Tasks:
        for j in model.S_J_Executing_I[i]:
            for n in model.S_Time:
                if model.V_B[i,j,n].value != None and model.V_B[i,j,n].value > 0:
                    print(f"{i}-{j}-{n}: {model.V_B[i,j,n].value}")
    plot_gantt_chart(H, model)
    plot_inventory_chart(H, model)
    
    
except:

    print(f"Error")