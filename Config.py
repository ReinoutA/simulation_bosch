from OrderType import OrderType
from Configuration import Configuration
from Method import *
from Schedulers.FCFS import FCFS
from Schedulers.SJF import SJF
from Schedulers.HRRN import HRRN
from Schedulers.PS import PS
from Schedulers.RR import RR
from Schedulers.SDD import SDD
from Schedulers.CR import CR
import numpy as np
import salabim as sim

TIME_LIMIT = 365

# Logging parameters
ENABLE_SIM_TRACE = False
LOG_QUEUES = True
LOG_MACHINES = False
LOG_GENERATOR = False
LOG_DATAFRAMES =  False

# Generator parameters
ORDER_SIZE_MEAN = 10000
ORDER_SIZE_STD = 5000
ORDER_MIN_SIZE = 1000
ORDER_INTERVAL_MEAN = 10000
ORDER_INTERVAL_STD = 3000
DEADLINE_MEAN = 20
DEADLINE_STD = 30
DEADLINE_MIN = 10

# GUI parameters
REFRESH_RATE = 10
shape_param = 4  # Vormparameter (kan worden aangepast)
scale_param = 14  # Schaalparameter (kan worden aangepast)
transitions = [
    {
        (OrderType.HIGH_QUALITY, OrderType.HIGH_QUALITY) : 0,
        (OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY) : sim.Gamma(shape_param, scale_param),
        (OrderType.HIGH_QUALITY, OrderType.LOW_QUALITY) : sim.Gamma(shape_param, scale_param),
        (OrderType.MEDIUM_QUALITY, OrderType.MEDIUM_QUALITY) : 0,
        (OrderType.MEDIUM_QUALITY, OrderType.HIGH_QUALITY) : sim.Gamma(shape_param, scale_param),
        (OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY) : sim.Gamma(shape_param, scale_param),
        (OrderType.LOW_QUALITY, OrderType.LOW_QUALITY) : 0,
        (OrderType.LOW_QUALITY, OrderType.HIGH_QUALITY) : sim.Gamma(shape_param, scale_param),
        (OrderType.LOW_QUALITY, OrderType.MEDIUM_QUALITY) : sim.Gamma(shape_param, scale_param),
    },
    {
        (OrderType.HIGH_QUALITY, OrderType.HIGH_QUALITY) : 0,
        (OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY) : sim.Gamma(shape_param, scale_param),
        (OrderType.HIGH_QUALITY, OrderType.LOW_QUALITY) : sim.Gamma(shape_param, scale_param),
        (OrderType.MEDIUM_QUALITY, OrderType.MEDIUM_QUALITY) : 0,
        (OrderType.MEDIUM_QUALITY, OrderType.HIGH_QUALITY) : sim.Gamma(shape_param, scale_param),
        (OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY) : sim.Gamma(shape_param, scale_param),
        (OrderType.LOW_QUALITY, OrderType.LOW_QUALITY) : 0,
        (OrderType.LOW_QUALITY, OrderType.HIGH_QUALITY) : sim.Gamma(shape_param, scale_param),
        (OrderType.LOW_QUALITY, OrderType.MEDIUM_QUALITY) : sim.Gamma(shape_param, scale_param),
    },
    {
        (OrderType.HIGH_QUALITY, OrderType.HIGH_QUALITY) : 0,
        (OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY) : sim.Gamma(shape_param, scale_param),
        (OrderType.HIGH_QUALITY, OrderType.LOW_QUALITY) : sim.Gamma(shape_param, scale_param),
        (OrderType.MEDIUM_QUALITY, OrderType.MEDIUM_QUALITY) : 0,
        (OrderType.MEDIUM_QUALITY, OrderType.HIGH_QUALITY) : sim.Gamma(shape_param, scale_param),
        (OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY) : sim.Gamma(shape_param, scale_param),
        (OrderType.LOW_QUALITY, OrderType.LOW_QUALITY) : 0,
        (OrderType.LOW_QUALITY, OrderType.HIGH_QUALITY) : sim.Gamma(shape_param, scale_param),
        (OrderType.LOW_QUALITY, OrderType.MEDIUM_QUALITY) : sim.Gamma(shape_param, scale_param),
    },
    {
        (OrderType.HIGH_QUALITY, OrderType.HIGH_QUALITY) : 0,
        (OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY) : sim.Gamma(shape_param, scale_param),
        (OrderType.HIGH_QUALITY, OrderType.LOW_QUALITY) : sim.Gamma(shape_param, scale_param),
        (OrderType.MEDIUM_QUALITY, OrderType.MEDIUM_QUALITY) : 0,
        (OrderType.MEDIUM_QUALITY, OrderType.HIGH_QUALITY) : sim.Gamma(shape_param, scale_param),
        (OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY) : sim.Gamma(shape_param, scale_param),
        (OrderType.LOW_QUALITY, OrderType.LOW_QUALITY) : 0,
        (OrderType.LOW_QUALITY, OrderType.HIGH_QUALITY) : sim.Gamma(shape_param, scale_param),
        (OrderType.LOW_QUALITY, OrderType.MEDIUM_QUALITY) : sim.Gamma(shape_param, scale_param),
    },
    {
        (OrderType.HIGH_QUALITY, OrderType.HIGH_QUALITY) : 0,
        (OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY) : sim.Gamma(shape_param, scale_param),
        (OrderType.HIGH_QUALITY, OrderType.LOW_QUALITY) : sim.Gamma(shape_param, scale_param),
        (OrderType.MEDIUM_QUALITY, OrderType.MEDIUM_QUALITY) : 0,
        (OrderType.MEDIUM_QUALITY, OrderType.HIGH_QUALITY) : sim.Gamma(shape_param, scale_param),
        (OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY) : sim.Gamma(shape_param, scale_param),
        (OrderType.LOW_QUALITY, OrderType.LOW_QUALITY) : 0,
        (OrderType.LOW_QUALITY, OrderType.HIGH_QUALITY) : sim.Gamma(shape_param, scale_param),
        (OrderType.LOW_QUALITY, OrderType.MEDIUM_QUALITY) : sim.Gamma(shape_param, scale_param),
    }
]

runtimes = [
    {
        OrderType.HIGH_QUALITY : 150,
        OrderType.MEDIUM_QUALITY : 300,
        OrderType.LOW_QUALITY : 500,
    },
    {
        OrderType.HIGH_QUALITY : 100,
        OrderType.MEDIUM_QUALITY : 200,
        OrderType.LOW_QUALITY : 250,
    },
    {
        OrderType.HIGH_QUALITY : 200,
        OrderType.MEDIUM_QUALITY : 200,
        OrderType.LOW_QUALITY : 200,
    },
    {
        OrderType.HIGH_QUALITY : 100,
        OrderType.MEDIUM_QUALITY : 200,
        OrderType.LOW_QUALITY : 500,
    },
    {
        OrderType.HIGH_QUALITY : 300,
        OrderType.MEDIUM_QUALITY : 500,
        OrderType.LOW_QUALITY : 700,
    },
]

can_do_lists = [
    [OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY],
    [OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY],
    [OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY],
    [OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY],
    [OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY],
]

priority_lists = [
    [OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY],
    [OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY],
    [OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY],
    [OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY],
    [OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY],
]

configurations = []
for i in range(5):
    configurations.append(Configuration(transitions[i], runtimes[i], can_do_lists[i], priority_lists[i]))
    
order_type_map = {e.name: e for e in OrderType}
order_types = [e for e in OrderType]
order_type_names = [type.name for type in order_types]