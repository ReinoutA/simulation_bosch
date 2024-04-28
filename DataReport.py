import pandas as pd
import threading
import logging
import numpy as np
from Config import *

class DataReport:
    def __init__(self, name):
       self.df = pd.DataFrame(columns=["Order", "Starting time", "End time", "Execution time", "Deadline"])
       self.mutex = threading.Lock()
       self.name = name
       
    def append(self, order):
        self.mutex.acquire()
        new_row = {"Order": order.identifier,
                   "Starting time": order.start_time,
                   "End time": order.end_time,
                   "Execution time": order.execution_time,
                   "Deadline": order.deadline}
        
        self.df.loc[len(self.df)] = new_row
        # logging.info(f"Appending DataFrame {self.name}")
        self.mutex.release()
        
    def draw(self, name, ax_rr, ax_tn, fig, color):
        if not Config.gui_running:
            logging.error(f"Gui running is False")
            return
        
        self.mutex.acquire()

        if self.df.empty:
            logging.error(f"Empty DataFrame when drawing {self.name}")
        else:
            self.df["Turnaround time"] = self.df["End time"] - self.df["Starting time"]
            self.df["Response ratio"] = self.df["Turnaround time"] / self.df["Execution time"]
            if self.df is not None:
                self.df.sort_values("Response ratio", inplace=True)
                self.df = self.df.reset_index(drop=True)
                x_values = np.linspace(0, 100, len(self.df)) 
            
            line_rr = None

            if color is not None:
                line_rr = ax_rr.plot(x_values, self.df["Response ratio"], label=name, color=color)
            else:
                line_rr = ax_rr.plot(x_values, self.df["Response ratio"], label=name)

            ax_rr.set_yscale('log')

            self.df["Lateness"] = self.df["End time"] - self.df["Deadline"]
            if self.df is not None:
                self.df.sort_values("Lateness", inplace=True)
                self.df = self.df.reset_index(drop=True)
                x_values = np.linspace(0, 100, len(self.df)) 
            
            line_tn = None
            if color is not None:
                line_tn = ax_tn.plot(x_values, self.df["Lateness"], label=name, color=color)
            else:
                line_tn = ax_tn.plot(x_values, self.df["Lateness"], label=name)

            # ax_tn.set_yscale('log')
            # if line_rr is not None or line_tn is not None:
            #     fig.legend(handles=[line_rr, line_tn], loc='upper right')
        self.mutex.release()
        
    def log_info(self):
        self.mutex.acquire()
        if self.df.empty:
            logging.error(f"Empty DataFrame when printing {self.name}")
        else:
            logging.info(f"Printing DataFrame {self.name}")
            logging.info(self.df)
        self.mutex.release()