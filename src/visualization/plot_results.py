import matplotlib.pyplot as plt
from pyomo.environ import *


def plot_gantt_chart(H, model):
    
    plt.figure(figsize=(12,6))
    gap = (H+1)/500
    idx = 1
    lbls = []
    ticks = []
    for j in sorted(model.S_Units):
        idx -= 1
        for i in sorted(model.S_I_In_J[j]):
            idx -= 1
            ticks.append(idx)
            lbls.append("{0:s} -> {1:s}".format(j,i))
            plt.plot([0,H+5],[idx,idx],lw=20,alpha=.3,color='y')
            for t in model.S_Time:
                if model.V_X[i,j,t]() > 0.0001:
                    plt.plot([t+gap, t + model.P_Tau[i,j]-gap], [idx,idx],'b', lw=20, solid_capstyle='butt')
                    txt = "{0:.2f}".format(model.V_B[i,j,t]())
                    plt.text(t + model.P_Tau[i,j]/2, idx, txt, color='white', weight='bold', ha='center', va='center')
    plt.xlim(0,H+1)
    plt.gca().set_yticks(ticks)
    plt.gca().set_yticklabels(lbls) 
    plt.tight_layout()
    plt.show(block=True) 

    
def plot_inventory_chart(H, model):
    
    plt.figure(figsize=(10,6))
    for (k,idx) in list(zip(model.S_Materials, range(len(model.S_Materials)))):
        plt.subplot(ceil(len(model.S_Materials)/3),3,idx+1)
        tlast,ylast = 0, model.P_Init_Inventory_Material[k]
        for (t,y) in zip(list(model.S_Time),[model.V_S[k,t]() for t in model.S_Time]):
            plt.plot([tlast,t,t],[ylast,ylast,y],'b')
            tlast,ylast = t,y
        plt.ylim(0,1.1*model.P_Chi[k])
        plt.plot([0,H],[model.P_Chi[k],model.P_Chi[k]],'r--')
        plt.title(k)
    plt.tight_layout()
    plt.show(block=True) 