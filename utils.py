from pyomo.environ import *

def print_set(model, set) -> None:
    print(set.data())