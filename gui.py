import tkinter as tk
from tkinter import Button
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import logging
from threading import Thread
# from threading import Timer

from Config import *
import Config
from Simulation import Simulation

class Gui(Thread):
    def __init__(self,):
        super().__init__()
        self.reports = []
        
    def run(self):
        self.root = tk.Tk()
        self.root.title("Scheduling simulation")

        button_frame = tk.Frame(self.root)
        button_frame.grid(row=1, column=1, sticky='s')

        options = ["Option 1", "Option 2", "Option 3"]
        self.selected_option = tk.StringVar(self.root)
        self.selected_option.set(options[0])  # default value
        option_menu = tk.OptionMenu(self.root, self.selected_option, *options)
        option_menu.grid(row=0, column=1)  # Use grid instead of pack

        start_simulation_button = Button(button_frame, text="Start simulation", command=self.start_simulation)
        start_simulation_button.grid(row=0, column=0)

        stop_simulation_button = Button(button_frame, text="Stop simulation", command=self.stop_simulation)
        stop_simulation_button.grid(row=1, column=0)

        self.fig = Figure(figsize=(5, 5))
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=2)

        self.root.mainloop()
        Config.gui_running = False
        
    def draw_plot(self):
        while Config.simulation_running:
            self.ax.clear()
            
            for i in range(len(methods)):
                if i < len(self.reports):
                    self.reports[i].draw(methods[i].name, self.ax, None)
                else:
                    logging.error("Reports index out of range")

            self.ax.set_xlim([0, 100])
            self.ax.set_title("Response ratio")

            self.ax.set_xlabel("% of orders")
            self.ax.set_ylabel("Response ratio")

            self.ax.legend()
            self.ax.grid()
            self.canvas.draw()
            # self.root.after(REFRESH_RATE, lambda: self.draw_plot()) 
    
    def start_simulation(self):
        if not Config.simulation_running:
            Config.simulation_running = True
            # self.root.after(REFRESH_RATE, lambda: self.draw_plot())
            # self.timer = Timer(Config.REFRESH_RATE / 1000, self.draw_plot)
            # self.timer.start()
            
            graphing_thread = Thread(target=self.draw_plot)
            graphing_thread.start()
        
            self.reports = []
            Simulation(self.reports).start()
    
    def stop_simulation(self):
        if Config.simulation_running:
            Config.simulation_running = False
            self.ax.clear()
            self.canvas.draw()