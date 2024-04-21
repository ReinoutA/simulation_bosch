from OrderType import OrderType
from Method import *
from Schedulers.FCFS import FCFS
from Schedulers.SJF import SJF
from Schedulers.HRRN import HRRN
from Schedulers.PS import PS
from Schedulers.RR import RR

TIME_LIMIT = 365

# Logging parameters
ENABLE_SIM_TRACE = False
LOG_QUEUES = False
LOG_MACHINES = False
LOG_GENERATOR = False
LOG_DATAFRAMES =  True

# Generator parameters
ORDER_SIZE_MEAN = 100000
ORDER_SIZE_STD = 50000
ORDER_INTERVAL_MEAN = 7
ORDER_INTERVAL_STD = 1

# GUI parameters
REFRESH_RATE = 10

# methods = ["FCFS", "SJF", "HRRN", "PS" , "RR-7", "RR-14", "RR-28"]
methods = [FCFS(), SJF(), HRRN(), PS(), RR(7), RR(14), RR(28)]
# methods = [FCFS()]

# Priority list for Priority Scheduling
PRIORITY_LIST = [OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY,]

transitions = {
    (OrderType.HIGH_QUALITY, OrderType.HIGH_QUALITY) : 0,
    (OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY) : 30,
    (OrderType.HIGH_QUALITY, OrderType.LOW_QUALITY) : 30,
    (OrderType.MEDIUM_QUALITY, OrderType.MEDIUM_QUALITY) : 0,
    (OrderType.MEDIUM_QUALITY, OrderType.HIGH_QUALITY) : 60,
    (OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY) : 30,
    (OrderType.LOW_QUALITY, OrderType.LOW_QUALITY) : 0,
    (OrderType.LOW_QUALITY, OrderType.HIGH_QUALITY) : 60,
    (OrderType.LOW_QUALITY, OrderType.MEDIUM_QUALITY) : 30,
}

runtime = [
    {
        OrderType.HIGH_QUALITY : ORDER_SIZE_MEAN / 30,
        OrderType.MEDIUM_QUALITY : ORDER_SIZE_MEAN / 20,
        OrderType.LOW_QUALITY : ORDER_SIZE_MEAN / 10,
    },
    {
        OrderType.HIGH_QUALITY : ORDER_SIZE_MEAN / 50,
        OrderType.MEDIUM_QUALITY : ORDER_SIZE_MEAN / 25,
        OrderType.LOW_QUALITY : ORDER_SIZE_MEAN / 20,
    },
    {
        OrderType.HIGH_QUALITY : ORDER_SIZE_MEAN / 100,
        OrderType.MEDIUM_QUALITY : ORDER_SIZE_MEAN / 50,
        OrderType.LOW_QUALITY : ORDER_SIZE_MEAN / 30,
    },
    {
        OrderType.HIGH_QUALITY : ORDER_SIZE_MEAN / 10,
        OrderType.MEDIUM_QUALITY : ORDER_SIZE_MEAN / 5,
        OrderType.LOW_QUALITY : ORDER_SIZE_MEAN / 5,
    },
    {
        OrderType.HIGH_QUALITY : ORDER_SIZE_MEAN / 35,
        OrderType.MEDIUM_QUALITY : ORDER_SIZE_MEAN / 20,
        OrderType.LOW_QUALITY : ORDER_SIZE_MEAN / 15,
    },
]

can_do_lists = [
    [OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY],
    [OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY],
    [OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY],
    [OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY],
    [OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY],
]

gui_running = True
simulation_running = False;