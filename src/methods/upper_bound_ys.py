from pyomo.environ import *
from numpy import floor
from src.models.optimization_config import define_solver

ADD_TIME_PERIOD = 1  # Used for computing the number of time periods
TAU_END_UNIT = 1  # Number of idle periods between two consecutive runs in a unit

