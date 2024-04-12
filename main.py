import salabim as sim
from enum import Enum
import random
import csv
import time    
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

TIME_LIMIT = 365

# Logging parameters
ENABLE_SIM_TRACE = True
LOG_QUEUES = True
LOG_MACHINES = True
LOG_GENERATOR = True

# Generator parameters
ORDER_SIZE_MEAN = 100000
ORDER_SIZE_STD = 50000
ORDER_INTERVAL_MEAN = 7
ORDER_INTERVAL_STD = 1

methods = ["FCFS", "SJF", "HRRN", "PS"]

class OrderType(Enum):
    HIGH_QUALITY = 0
    MEDIUM_QUALITY = 1
    LOW_QUALITY = 2

# Priority list for PS
PRIORITY_LIST = [OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY,]

class Machine(sim.Component):
    num_machines = 1
    
    def __init__(self, transition_per_type_combination, runtime_per_type, can_do_list, global_queue, machines, method):
        super().__init__()
        self.id = Machine.num_machines
        Machine.num_machines += 1
        # self.queue = sim.Queue(f"Machine queue {self.id}")
        self.queue = global_queue
        self.total_transition_time = 0
        self.last_order_type = 0
        self.total_profit = 0
        self.transition_per_type_combination = transition_per_type_combination
        self.runtime_per_type = runtime_per_type
        self.can_do_list = can_do_list
        self.machines = machines
        self.method = method
        
    def process(self):
        while True:
            if len(self.queue) == 0:
                self.passivate()
                
            # FCFS
            if self.method == "FCFS":
                order = self.queue.pop()
            
            # SJF
            elif self.method == "SJF":
                order = None
                min_size = 1E30
                for o in self.queue:
                    if o.size < min_size and o.type in self.can_do_list:
                        min_size = o.size
                        order = o
                self.queue.remove(order)
                    
            # HRRN   
            elif self.method == "HRRN":
                order = None
                worst_val = 0
                now = env.now()
                
                for o in self.queue:
                    if o.type in self.can_do_list:
                        execution_time = o.size / self.runtime_per_type[o.type]
                        val = o.get_response_ratio(now, execution_time)
                        if val >= worst_val:
                            worst_val = val
                            order = o
                self.queue.remove(order)
                
            # PS
            elif self.method == "PS":
                orders = [None] * len(PRIORITY_LIST)
                order = None
                
                for o in self.queue:
                    if o.type in self.can_do_list:
                        for i, o_type in enumerate(PRIORITY_LIST):
                            if o.type == o_type:
                                orders[i] = o
                                break
                
                for elem in orders:
                    if elem is not None:
                        order = elem
                        break
                    
                self.queue.remove(order)
                
            if order is not None:
                if order.type not in self.can_do_list:
                    self.queue.add(order)
                    for machine in machines:
                        if machine.status() != 'passive':
                            machine.activate()
                    self.passivate()
                
                if self.last_order_type != 0:
                    transition_time = self.transition_per_type_combination.get((self.last_order_type, order.type), 0)
                    self.total_transition_time += transition_time
                    self.hold(transition_time)

                self.last_order_type = order.type
                self.total_profit += order.profit
                execution_time = order.size / self.runtime_per_type[order.type]
                self.hold(execution_time)
                order.end_time = env.now()
                order.execution_time = execution_time
                order.report()
            
class Order(sim.Component):
    counter = 0
    
    def __init__(self, type, size, deadline, received_date, profit, method):
        super().__init__()
        self.identifier = Order.counter
        Order.counter += 1
        self.type = type
        self.size = abs(size)
        self.deadline = deadline
        self.received_date = received_date
        self.profit = profit
        self.start_time = env.now()
        self.end_time = None
        self.execution_time = None
        self.method = method
        
    def report(self):
        with open(f"report_{self.method}.csv", "a", newline = "") as file:
            writer = csv.writer(file)
            writer.writerow([self.identifier, self.start_time, self.end_time, self.execution_time])
            
    def get_response_ratio(self, now, execution_time):
        return (now - self.start_time) / execution_time
       
class OrderGenerator(sim.Component):
    def __init__(self, queue, method):
        super().__init__()
        self.queue = queue
        self.num_generated = 0
        self.method = method
        
    def process(self):
        order_types = list(OrderType)
        order_type_weights = [0.1, 0.3, 0.6]  # adjust these values to your needs
        
        while env.now() < TIME_LIMIT:
            random_order_type = random.choices(order_types, weights=order_type_weights, k=1)[0]
            self.queue.add(Order(random_order_type, sim.Normal(ORDER_SIZE_MEAN, ORDER_SIZE_STD).sample(), 0, 0, 1, self.method))
            self.num_generated += 1
            self.hold(abs(sim.Normal(ORDER_INTERVAL_MEAN, ORDER_INTERVAL_STD).sample()))
            
            for machine in machines:
                if machine.status() == 'passive':
                    machine.activate()
        
    def report(self):
        print(f"Generated {self.num_generated} orders")
   

for method in methods:
    print(method) 
    with open(f"report_{method}.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["Order", "Starting time", "End time", "Execution time"])
        
    env = sim.Environment(trace=ENABLE_SIM_TRACE)
    env.random_seed(int(time.time()))

    queues = []

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

    global_queue = sim.Queue("Global queue")

    machines = []
    for i in range(5):
        machine = Machine(transitions, runtime[i], can_do_lists[i], global_queue, machines, method)
        machines.append(machine)

    for machine in machines:
        queues.append(machine.queue)

    generator = OrderGenerator(global_queue, method)
    generator.activate()

    for machine in machines:
        if machine.status() != 'passive':
            machine.activate()
        
    env.run()
    if LOG_QUEUES:
        global_queue.print_statistics()

    max_len = 0
    if LOG_MACHINES:
        for i, machine in enumerate(machines, start=1):
            string = f"Machine {i} made {machine.total_profit} profit, waited {machine.total_transition_time} on transitions."
            print(string)
            if len(string) > max_len:
                max_len = len(string)
            
    print("-" * max_len)

    if LOG_GENERATOR:
        generator.report()

print("Started graphing...")

dfs = []

for name in methods:
    df = pd.read_csv(f"report_{name}.csv")
    df["Turnaround time"] = df["End time"] - df["Starting time"]
    df["Response ratio"] = df["Turnaround time"] / df["Execution time"]
    df = df.sort_values("Response ratio")
    df = df.reset_index(drop=True)
    dfs.append(df)

for i in range(len(methods)):
    name = methods[i]
    df = dfs[i]
    x_values = np.linspace(0, 100, len(df)) 
    plt.plot(x_values, df["Response ratio"], label=name)
    
plt.xlim([0, 100])
plt.title("Response ratio")

plt.xlabel("% of orders")
plt.ylabel("Response ratio")

plt.legend()
plt.grid()
plt.savefig("response_ratio.png")