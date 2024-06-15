from OrderType import OrderType
from Configuration import Configuration
from Method import *
from Schedulers.FCFS import FCFS
from Schedulers.FCFSO import FCFSO
from Schedulers.SJF import SJF
from Schedulers.HRRN import HRRN
from Schedulers.PS import PS
from Schedulers.RR import RR
from Schedulers.SDD import SDD
from Schedulers.CR import CR
import numpy as np
import salabim as sim

# This file contains all configparamters for the simulation. This is the only file that should be changed in order
# to change the simulation parameters, without changing fundamental logic in the simulation.

# These parameters are not inteded to be changed. Generally you can use this to set delays in terms of days, hours and minutes.
MINUTES_IN_HOUR = 60
HOURS_IN_DAY = 24
DAYS_IN_WEEK = 7

# Logging parameters
ENABLE_SIM_TRACE = False                                                                                # Show live information of the simulation by salabim
LOG_QUEUES = True                                                                                       # Print the queue statistics at the end of the simulation
LOG_MACHINES = False                                                                                    # Print machine statistics at the end of the simulation
LOG_GENERATOR = False                                                                                   # Print generator statistics at the end of the simulation
LOG_DATAFRAMES =  False                                                                                 # Print the data we plot in the log.txt file, mostly for debugging purposes

# Generator parameters
ORDER_INTERVAL_MEAN = DAYS_IN_WEEK * HOURS_IN_DAY * MINUTES_IN_HOUR / 500                               # The mean time that the OrderGenerator waits to generate a new order
ORDER_INTERVAL_STD = 0                                                                                  # The standarddeviation for the time that the OrderGenerator waits to generate a new order
                                                                                                        # We left this on 0 in order to make this a fixed value. This is however a Noram distribution in the code
DEADLINE_MEAN = 2                                                                                       # Deadline mean in weeks
DEADLINE_STD = 0.5                                                                                      # Deadline standard deviation in weeks
DEADLINE_MIN = 1                                                                                        # Minimum deadline in weeks, if the normaldistribution samples a value below this, this will be the new set value

SHAPE_PARAM = 4                                                                                         # Shape parameter for the Gamma-distribution of the transition time
SCALE_PARAM = 14                                                                                        # Schale parameter for the Gamma-distribution of the transition time
# GUI parameters
REFRESH_RATE = 10
SLEEP_FACTOR = 0.0                                                                                      # Determines silumation speed, this is a small delay for which the program
                                                                                                        # halts. In case you sue a lot of orders / week, put this number low since the program has a lot to process.
                                                                                                        # In case  you generate a small amount of orders / week you should put this a little higher, in order to make
                                                                                                        # it possible to see the effects of the simulation. Typical values between 0.0 (faster simulation) and 0.5 (slower simulation)
                                                                                                        # DISCLAIMER: This does not change anything to the results of the ismulation, this is only for graphical purposes
materials = ["FX", "ND", "ND", "NU", "RD", "YL"]
order_types = list(OrderType)
order_type_weights = [0.1187, 0.069, 0.0734, 0.3663, 0.2085, 0.0353, 0.1288]                            # Weights from the pie chart in order to generate the OrderTypes based on frequency in the dataset


line_numbers = [103, 104, 105]                                                                          # Define the line numbers for the machines                                                

can_do_lists = [                                                                                        # Define which machine can do which OrderType     
    [OrderType.FX_16m_37xxx, OrderType.NU_20m_80xx, OrderType.NU_22m_68xxx, OrderType.ND_22m_143xxx],   # Line 103
    [OrderType.NU_22m_68xxx, OrderType.ND_22m_143xxx],                                                  # Line 104
    [OrderType.ND_35m_143xxx, OrderType.ND_35m_79xxx, OrderType.ND_40m_143xxx],                         # Line 105
]

priority_lists = [                                                                                      # Define the priority list for each machine in case you want to implement Priority scheduling
    [OrderType.FX_16m_37xxx, OrderType.ND_22m_143xxx, OrderType.NU_20m_80xx, OrderType.NU_22m_68xxx],   # Line 103
    [OrderType.NU_22m_68xxx, OrderType.ND_22m_143xxx],                                                  # Line 104
    [OrderType.ND_35m_143xxx, OrderType.ND_35m_79xxx, OrderType.ND_40m_143xxx],                         # Line 105
]

# This part is mainly for the simultion setup, should not be changed in order to set parameters
configurations = []                                                                                     # This is for the setup of the scheduler, the configuration determines how we decide the runtime and error_rate parameters (by sampling)
for i in range(len(can_do_lists)):
    configurations.append(Configuration(can_do_lists[i], priority_lists[i]))
    
order_type_map = {e.name: e for e in OrderType}
order_types = [e for e in OrderType]
order_type_names = [type.name for type in order_types]