import pandas as pd
import threading
import logging
import numpy as np
from Config import *

class DataReport:
    def __init__(self, name):
       self.df = pd.DataFrame(columns=["Order", "Starting time", "End time", "Execution time"])
       self.mutex = threading.Lock()
       self.name = name
       
    def append(self, order):
        self.mutex.acquire()
        new_row = {"Order": order.identifier,
                   "Starting time": order.start_time,
                   "End time": order.end_time,
                   "Execution time": order.execution_time}
        
        self.df.loc[len(self.df)] = new_row
        logging.info(f"Printing DataFrame {self.name}")
        logging.info(self.df)
        self.mutex.release()
        
    def draw(self, name, ax, color):
        if not gui_running:
            return
        
        self.mutex.acquire()

        if self.df.empty:
            logging.error(f"Empty DataFrame when drawing {self.name}")
        else:
            self.df["Turnaround time"] = self.df["End time"] - self.df["Starting time"]
            self.df["Response ratio"] = self.df["Turnaround time"] / self.df["Execution time"]
            self.df = self.df.sort_values("Response ratio")
            self.df = self.df.reset_index(drop=True)
            x_values = np.linspace(0, 100, len(self.df)) 
            
            logging.info(f"Drawing {self.name}")
            if color is not None:
                ax.plot(x_values, self.df["Response ratio"], label=name, color=color)
            else:
                ax.plot(x_values, self.df["Response ratio"], label=name)

        self.mutex.release()
        
    def print(self):
        self.mutex.acquire()
        if self.df.empty:
            logging.error(f"Empty DataFrame when printing {self.name}")
        else:
            logging.info(f"Printing DataFrame {self.name}")
            logging.info(self.df)
        self.mutex.release()