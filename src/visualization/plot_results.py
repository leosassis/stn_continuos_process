import matplotlib.pyplot as plt
from pyomo.environ import *


def plot_gantt_chart(planning_horizon: int, model: ConcreteModel, var: str) -> None:
    """
    Prints differents variables in a Gannt chart. 
    
    Args:
        - planning_horizon (int): planning horizon.
        - model (ConcreteModel): a Pyomo model instance.
        - var (str): defined which variable to print (e.g., X, Y, B)
    """
    
    
    plt.figure(figsize=(12,6))
    gap = (planning_horizon+1)/500
    idx = 1
    lbls = []
    ticks = []
    for j in sorted(model.S_Units):
        idx -= 1
        for i in sorted(model.S_I_In_J[j]):
            idx -= 1
            ticks.append(idx)
            lbls.append("{0:s} -> {1:s}".format(j,i))
            plt.plot([0,planning_horizon+5],[idx,idx],lw=20,alpha=.3,color='y')            
            if var == "X":
                for t in model.S_Time:
                    if model.V_X[i,j,t]() > 0.0001:
                        plt.plot([t+gap, t + model.P_Tau[i,j]-gap], [idx,idx],'b', lw=20, solid_capstyle='butt')
                        txt = "{0:.2f}".format(model.V_X[i,j,t]())
                        plt.text(t + model.P_Tau[i,j]/2, idx, txt, color='white', weight='bold', ha='center', va='center')
            
            elif var == "Y":                
                for t in model.S_Time:
                    val_YS = model.V_Y_Start[i, j, t]()
                    val_YE = model.V_Y_End[i,j,t]()
                    if val_YS is not None and val_YS > 0.0001:
                        plt.plot([t+gap, t + model.P_Tau[i,j]-gap], [idx,idx],'g', lw=20, solid_capstyle='butt')
                        txt = "{0:.2f}".format(model.V_Y_Start[i,j,t]())
                        plt.text(t + model.P_Tau[i,j]/2, idx, txt, color='white', weight='bold', ha='center', va='center')
                    if val_YE is not None and val_YE > 0.0001:
                        plt.plot([t+gap, t + model.P_Tau[i,j]-gap], [idx,idx],'r', lw=20, solid_capstyle='butt')
                        txt = "{0:.2f}".format(model.V_Y_End[i,j,t]())
                        plt.text(t + model.P_Tau[i,j]/2, idx, txt, color='white', weight='bold', ha='center', va='center')  
            
            elif var == "B":
                for t in model.S_Time:
                    if model.V_X[i,j,t]() > 0.0001:
                        plt.plot([t+gap, t + model.P_Tau[i,j]-gap], [idx,idx],'b', lw=20, solid_capstyle='butt')
                        txt = "{0:.2f}".format(model.V_B[i,j,t]())
                        plt.text(t + model.P_Tau[i,j]/2, idx, txt, color='white', weight='bold', ha='center', va='center')
            
    plt.xlim(0,planning_horizon+1)
    plt.gca().set_yticks(ticks)
    plt.gca().set_yticklabels(lbls) 
    plt.tight_layout()
    plt.show(block=True)