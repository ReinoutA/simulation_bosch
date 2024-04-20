import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import rcParams
import logging
from threading import Thread
from Config import *
import Config

class Gui(Thread):
    def __init__(self, reports):
        super().__init__()
        self.reports = reports
        
    def run(self):
        root = tk.Tk()
        fig = Figure(figsize=(5, 5))
        ax = fig.add_subplot(111)

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack()

        root.after(REFRESH_RATE, lambda: self.draw_plot(ax, canvas, root)) 
        root.mainloop()
        Config.gui_running = False
        
    def draw_plot(self, ax, canvas, root):
        ax.clear()
        
        for i in range(len(methods)):
            if i < len(self.reports):
                logging.info(f"Calling draw for {i}")
                self.reports[i].draw(methods[i].name, ax, None)
            else:
                logging.error("Index out of range")

        ax.set_xlim([0, 100])
        ax.set_title("Response ratio")

        ax.set_xlabel("% of orders")
        ax.set_ylabel("Response ratio")

        ax.legend()
        ax.grid()
        canvas.draw()
        root.after(REFRESH_RATE, lambda: self.draw_plot(ax, canvas, root)) 