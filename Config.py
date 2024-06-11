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
ORDER_INTERVAL_MEAN = 500
ORDER_INTERVAL_STD = 50
DEADLINE_MEAN = 10
DEADLINE_STD = 0
DEADLINE_MIN = 0

# GUI parameters
REFRESH_RATE = 10
SHAPE_PARAM = 4  # Vormparameter (kan worden aangepast)
SCALE_PARAM = 14  # Schaalparameter (kan worden aangepast)

materials = ["FX", "ND", "ND", "NU", "RD", "YL"]
order_types = list(OrderType)
order_type_weights = [0.14, 0.14, 0.14, 0.14, 0.14, 0.15, 0.15]

can_do_lists = [
    [OrderType.FX_16m_37xxx, OrderType.NU_20m_80xx, OrderType.NU_22m_68xxx, OrderType.ND_22m_143xxx],
    [OrderType.NU_22m_68xxx, OrderType.ND_22m_143xxx],
    [OrderType.ND_35m_143xxx, OrderType.ND_35m_79xxx, OrderType.ND_40m_143xxx],
]

priority_lists = [
    [OrderType.FX_16m_37xxx, OrderType.ND_22m_143xxx, OrderType.NU_20m_80xx, OrderType.NU_22m_68xxx],
    [OrderType.NU_22m_68xxx, OrderType.ND_22m_143xxx],
    [OrderType.ND_35m_143xxx, OrderType.ND_35m_79xxx, OrderType.ND_40m_143xxx],
]

configurations = []
for i in range(3):
    configurations.append(Configuration(can_do_lists[i], priority_lists[i]))
    
order_type_map = {e.name: e for e in OrderType}
order_types = [e for e in OrderType]
order_type_names = [type.name for type in order_types]