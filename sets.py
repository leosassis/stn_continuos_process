from data import *
from pyomo.environ import *
from utils import print_set

H = H_Network_2
STN = Network_2

STATES = STN['STATES']
STATES_SHIPMENT = STN['STATES_SHIPMENT']
ST_ARCS = STN['ST_ARCS']
TS_ARCS = STN['TS_ARCS']
UNIT_TASKS = STN['UNIT_TASKS']
TIME = STN['TIME']
TASKS_TRANSITION_TASKS = STN['TASKS_TRANSITION_TASKS']

def set_all_tasks(UNIT_TASKS):
    return {key[1] for key in UNIT_TASKS.keys()}

def create_sets(model):
    
    model.S_Tasks = Set(initialize = set_all_tasks(UNIT_TASKS))
    #model.S_Products =Set(initialize = list(df_products['products']))
    print_set(model, model.S_Tasks)
    #print_set(model, model.S_Products)