from pyomo.environ import *
from numpy import floor
from src.utils.utils import print_dict


def compute_upper_bound_x(model: ConcreteModel, STN: dict) -> None:
    """ 
    Computes upper bounds on x variables based on its operational window.
    """
    
    est = STN['EST_ST']
    number_ys = {}
    upper_bound_x = {}
    number_remaining_periods_for_x = {}
    
    S_Time = model.S_Time
    
    for j, i in est:
        
        tau_max = model.P_Tau_Max[i,j]
        tau_min = model.P_Tau_Min[i,j]
        tau_end = model.P_Tau_End_Task[i]
        
        number_ys[j,i] = floor((max(S_Time) + 1 - est[j,i])/(tau_max + tau_end))
        upper_bound_x[j,i] = number_ys[j,i]*tau_max
        number_remaining_periods_for_x[j,i] = max(0, max(S_Time) - est[j,i] - number_ys[j,i]*(tau_max + tau_end))    
    
        for tau in range(int(tau_max) -1, int(tau_min) -1, -1):
            if tau <= number_remaining_periods_for_x[j,i]:
                upper_bound_x[j,i] += tau
                break        
    
    STN['UPPER_BOUND_X'] = upper_bound_x
    