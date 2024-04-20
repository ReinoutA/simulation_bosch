import salabim as sim

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import rcParams
import numpy as np
import threading
import logging
import time

from Order import Order
from OrderGenerator import OrderGenerator
from OrderType import OrderType
from Config import *
import Config
from Simulation import Simulation
from Machine import Machine
from DataReport import DataReport

def draw_plot(ax, canvas, root):
    ax.clear()
    
    color_cycle = rcParams['axes.prop_cycle'].by_key()['color']
    
    if len(reports) == len(methods):
        for i, color in zip(range(len(methods)), color_cycle):
            name = methods[i]
            if i < len(reports):
                logging.info(f"Calling draw for {i}")
                reports[i].draw(name, ax, None)
            else:
                logging.error("Index out of range")

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
    root = tk.Tk()
    fig = Figure(figsize=(5, 5))
    ax = fig.add_subplot(111)

    color_cycle = rcParams['axes.prop_cycle'].by_key()['color']
    
    if len(reports) == len(methods):
        for i, color in zip(range(len(methods)), color_cycle):
            name = methods[i]
            if i < len(reports):
                logging.info(f"Calling draw for {i}")
                reports[i].draw(name, ax, None)
            else:
                logging.error("Index out of range")

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
    Config.gui_running = False

def run_simulation():
    env = sim.Environment(trace=ENABLE_SIM_TRACE)
    env.random_seed(int(time.time()))

    for index in range(len(methods)):
        global_queue = sim.Queue("Global queue")
        report = DataReport(methods[index])
        reports.append(report)

        machines = []
        for i in range(5):
            machine = Machine(transitions, runtime[i], can_do_lists[i], global_queue, machines, methods[index], env)
            machines.append(machine)

        queues = []
        for machine in machines:
            queues.append(machine.queue)

        generator = OrderGenerator(global_queue, methods[index], machines, env, report)
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
        generator.create_report()

with open("log.txt", "w+") as f:
    pass

logging.basicConfig(filename="log.txt", level=logging.INFO)

with open(f"env.txt", "w+") as file:
    pass

global reports
reports = []
Config.gui_running = True

simulation_thread = threading.Thread(target=run_simulation, args=())
simulation_thread.start()

gui_thread = threading.Thread(target=run_gui)
gui_thread.start()

# simulation = Simulation(index)