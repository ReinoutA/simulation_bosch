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

TIME_LIMIT = 365

# Logging parameters
ENABLE_SIM_TRACE = False
LOG_QUEUES = True
LOG_MACHINES = False
LOG_GENERATOR = False
LOG_DATAFRAMES =  False

# Generator parameters
ORDER_SIZE_MEAN = 100000
ORDER_SIZE_STD = 50000
ORDER_MIN_SIZE = 1000
ORDER_INTERVAL_MEAN = 7
ORDER_INTERVAL_STD = 2
DEADLINE_MEAN = 20
DEADLINE_STD = 30
DEADLINE_MIN = 10

# GUI parameters
REFRESH_RATE = 10

transitions = [
    {
        (OrderType.HIGH_QUALITY, OrderType.HIGH_QUALITY) : 0,
        (OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY) : 30,
        (OrderType.HIGH_QUALITY, OrderType.LOW_QUALITY) : 30,
        (OrderType.MEDIUM_QUALITY, OrderType.MEDIUM_QUALITY) : 0,
        (OrderType.MEDIUM_QUALITY, OrderType.HIGH_QUALITY) : 60,
        (OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY) : 30,
        (OrderType.LOW_QUALITY, OrderType.LOW_QUALITY) : 0,
        (OrderType.LOW_QUALITY, OrderType.HIGH_QUALITY) : 60,
        (OrderType.LOW_QUALITY, OrderType.MEDIUM_QUALITY) : 30,
    },
    {
        (OrderType.HIGH_QUALITY, OrderType.HIGH_QUALITY) : 0,
        (OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY) : 30,
        (OrderType.HIGH_QUALITY, OrderType.LOW_QUALITY) : 30,
        (OrderType.MEDIUM_QUALITY, OrderType.MEDIUM_QUALITY) : 0,
        (OrderType.MEDIUM_QUALITY, OrderType.HIGH_QUALITY) : 60,
        (OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY) : 30,
        (OrderType.LOW_QUALITY, OrderType.LOW_QUALITY) : 0,
        (OrderType.LOW_QUALITY, OrderType.HIGH_QUALITY) : 60,
        (OrderType.LOW_QUALITY, OrderType.MEDIUM_QUALITY) : 30,
    },
    {
        (OrderType.HIGH_QUALITY, OrderType.HIGH_QUALITY) : 0,
        (OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY) : 30,
        (OrderType.HIGH_QUALITY, OrderType.LOW_QUALITY) : 30,
        (OrderType.MEDIUM_QUALITY, OrderType.MEDIUM_QUALITY) : 0,
        (OrderType.MEDIUM_QUALITY, OrderType.HIGH_QUALITY) : 60,
        (OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY) : 30,
        (OrderType.LOW_QUALITY, OrderType.LOW_QUALITY) : 0,
        (OrderType.LOW_QUALITY, OrderType.HIGH_QUALITY) : 60,
        (OrderType.LOW_QUALITY, OrderType.MEDIUM_QUALITY) : 30,
    },
    {
        (OrderType.HIGH_QUALITY, OrderType.HIGH_QUALITY) : 0,
        (OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY) : 30,
        (OrderType.HIGH_QUALITY, OrderType.LOW_QUALITY) : 30,
        (OrderType.MEDIUM_QUALITY, OrderType.MEDIUM_QUALITY) : 0,
        (OrderType.MEDIUM_QUALITY, OrderType.HIGH_QUALITY) : 60,
        (OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY) : 30,
        (OrderType.LOW_QUALITY, OrderType.LOW_QUALITY) : 0,
        (OrderType.LOW_QUALITY, OrderType.HIGH_QUALITY) : 60,
        (OrderType.LOW_QUALITY, OrderType.MEDIUM_QUALITY) : 30,
    },
    {
        (OrderType.HIGH_QUALITY, OrderType.HIGH_QUALITY) : 0,
        (OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY) : 30,
        (OrderType.HIGH_QUALITY, OrderType.LOW_QUALITY) : 30,
        (OrderType.MEDIUM_QUALITY, OrderType.MEDIUM_QUALITY) : 0,
        (OrderType.MEDIUM_QUALITY, OrderType.HIGH_QUALITY) : 60,
        (OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY) : 30,
        (OrderType.LOW_QUALITY, OrderType.LOW_QUALITY) : 0,
        (OrderType.LOW_QUALITY, OrderType.HIGH_QUALITY) : 60,
        (OrderType.LOW_QUALITY, OrderType.MEDIUM_QUALITY) : 30,
    },
]

runtimes = [
    {
        OrderType.HIGH_QUALITY : 3000,
        OrderType.MEDIUM_QUALITY : 5000,
        OrderType.LOW_QUALITY : 10000,
    },
    {
        OrderType.HIGH_QUALITY : 2000,
        OrderType.MEDIUM_QUALITY : 4000,
        OrderType.LOW_QUALITY : 5000,
    },
    {
        OrderType.HIGH_QUALITY : 1000,
        OrderType.MEDIUM_QUALITY : 2000,
        OrderType.LOW_QUALITY : 3000,
    },
    {
        OrderType.HIGH_QUALITY : 10000,
        OrderType.MEDIUM_QUALITY : 20000,
        OrderType.LOW_QUALITY : 20000,
    },
    {
        OrderType.HIGH_QUALITY : 3000,
        OrderType.MEDIUM_QUALITY : 5000,
        OrderType.LOW_QUALITY : 7000,
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