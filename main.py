import salabim as sim
from enum import Enum
import random
import csv
import time    
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import threading

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

# GUI parameters
REFRESH_RATE = 100

methods = ["FCFS", "SJF", "HRRN", "PS" , "RR-7", "RR-14", "RR-28"]
# methods = ["FCFS"]

class OrderType(Enum):
    HIGH_QUALITY = 0
    MEDIUM_QUALITY = 1
    LOW_QUALITY = 2

# Priority list for Priority Scheduling
PRIORITY_LIST = [OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY,]

class Machine(sim.Component):
    num_machines = 1
    
    def __init__(self, transition_per_type_combination, runtime_per_type, can_do_list, global_queue, machines, method, env):
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
        self.total_execution_time = 0
        self.env = env
        
    def process(self):
        while True:
            if len(self.queue) == 0:
                self.passivate()
                
            order = None
            
            # FCFS
            if self.method == "FCFS":
                order = self.queue.pop()
            
            # SJF
            elif self.method == "SJF":
                min_size = 1E30
                for o in self.queue:
                    if o.size < min_size and o.type in self.can_do_list:
                        min_size = o.size
                        order = o
                self.queue.remove(order)
                    
            # HRRN   
            elif self.method == "HRRN":
                worst_val = 0
                now = self.env.now()
                
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
                
            # RR
            elif "RR-" in self.method:
                if len(self.queue) > 0:
                    order = self.queue[0]
                    self.queue.remove(order)
                
            if order is not None:
                if order.type not in self.can_do_list:
                    self.queue.add(order)
                    for machine in self.machines:
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
                self.total_execution_time += execution_time
                self.hold(execution_time)
                order.end_time = self.env.now()
                order.execution_time = execution_time
                order.report()
                
                if "RR-" in self.method:
                    window = int(self.method.split("-")[1])
                    
                    if execution_time > window:
                        left_over = int((execution_time - window) * self.runtime_per_type[order.type])
                        order.size = left_over
                        self.queue.add(order)
                        
                        for machine in self.machines:
                            if machine.status() != 'passive':
                                machine.activate()
            
class Order(sim.Component):
    counter = 0
    
    def __init__(self, type, size, deadline, received_date, profit, method, env):
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
        active_report.report(self)
        # with open(f"report_{self.method}.csv", "a", newline = "") as file:
        #     writer = csv.writer(file)
        #     writer.writerow([self.identifier, self.start_time, self.end_time, self.execution_time])
            
    def get_response_ratio(self, now, execution_time):
        return (now - self.start_time) / execution_time
       
class OrderGenerator(sim.Component):
    def __init__(self, queue, method, machines, env):
        super().__init__()
        self.queue = queue
        self.num_generated = 0
        self.method = method
        self.machines = machines
        self.env = env
        
    def process(self):
        order_types = list(OrderType)
        order_type_weights = [0.1, 0.3, 0.6]  # adjust these values to your needs
        
        while gui_running:
            random_order_type = random.choices(order_types, weights=order_type_weights, k=1)[0]
            self.queue.add(Order(random_order_type, sim.Normal(ORDER_SIZE_MEAN, ORDER_SIZE_STD).sample(), 0, 0, 1, self.method, self.env))
            self.num_generated += 1
            self.hold(abs(sim.Normal(ORDER_INTERVAL_MEAN, ORDER_INTERVAL_STD).sample()))
            
            for machine in self.machines:
                if machine.status() == 'passive':
                    machine.activate()
        
        # self.env.exit()
        
    def report(self):
        print(f"Generated {self.num_generated} orders")

class DataReport:
    def __init__(self):
       self.df = pd.DataFrame(columns=["Order", "Starting time", "End time", "Execution time"])
       self.mutex = threading.Lock()
       
    def report(self, order):
        self.mutex.acquire()
        new_row = {"Order": order.identifier,
                   "Starting time": order.start_time,
                   "End time": order.end_time,
                   "Execution time": order.execution_time}
        
        self.df.loc[len(self.df)] = new_row
        self.mutex.release()
        
    def draw(self, name, ax):
        self.mutex.acquire()
        self.df["Turnaround time"] = self.df["End time"] - self.df["Starting time"]
        self.df["Response ratio"] = self.df["Turnaround time"] / self.df["Execution time"]
        self.df = self.df.sort_values("Response ratio")
        self.df = self.df.reset_index(drop=True)
        x_values = np.linspace(0, 100, len(self.df)) 
        ax.plot(x_values, self.df["Response ratio"], label=name)
        self.mutex.release()
        
    def print(self):
        self.mutex.acquire()
        print(self.df)
        self.mutex.release()

global active_report

reports = []
for i in range(len(methods)):
    reports.append(DataReport())

def draw_plot(ax, canvas, root):
    ax.clear()
    for i in range(len(methods)):
        name = methods[i]
        reports[i].draw(name, ax)

    ax.set_xlim([0, 100])
    ax.set_title("Response ratio")

    ax.set_xlabel("% of orders")
    ax.set_ylabel("Response ratio")

    ax.legend()
    ax.grid()
    ax.figure.savefig("response_ratio.png")
    canvas.draw()
    root.after(REFRESH_RATE, lambda: draw_plot(ax, canvas, root)) 

def run_gui():
    global gui_running

    root = tk.Tk()
    gui_running = True
    fig = Figure(figsize=(5, 5))
    ax = fig.add_subplot(111)

    for i in range(len(methods)):
        name = methods[i]
        reports[i].draw(name, ax)

    ax.set_xlim([0, 100])
    ax.set_title("Response ratio")

    ax.set_xlabel("% of orders")
    ax.set_ylabel("Response ratio")

    ax.legend()
    ax.grid()
    # ax.savefig("response_ratio.png")

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    root.after(REFRESH_RATE, lambda: draw_plot(ax, canvas, root)) 
    root.mainloop()
    gui_running = False

def run_simulation(index):
    global gui_running
        
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
        machine = Machine(transitions, runtime[i], can_do_lists[i], global_queue, machines, methods[index], env)
        machines.append(machine)

    for machine in machines:
        queues.append(machine.queue)

    generator = OrderGenerator(global_queue, methods[index], machines, env)
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
            string = f"Machine {i} made {machine.total_profit} profit, waited {machine.total_transition_time} on transitions, executed {machine.total_execution_time}."
            print(string)
            if len(string) > max_len:
                max_len = len(string)
            
    print("-" * max_len)

    if LOG_GENERATOR:
        generator.report()

global gui_running
gui_running = True

gui_thread = threading.Thread(target=run_gui)
gui_thread.start()

simulation_threads = []

for i in range(len(methods)):
    simulation_thread = threading.Thread(target=run_simulation, args=(i,))
    simulation_thread.start()
    simulation_threads.append(simulation_thread)

    active_report = reports[i]
    active_report.print()

    while gui_running:
        time.sleep(1)

for simulation_thread in simulation_threads:
    simulation_thread.join()

gui_thread.join()