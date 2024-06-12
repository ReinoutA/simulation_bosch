import pandas as pd
import threading
import logging
import numpy as np
from Config import *

class DataReport:
    def __init__(self, name):
        self.df = pd.DataFrame(columns=["Order", "Starting time", "End time", "Execution time", "Deadline"])
        self.stock = [(0, 0)]
        self.mutex = threading.Lock()
        self.name = name
        self.update_queue = []
       
    def append(self, order, num_processed, now):
        self.mutex.acquire()
        new_row = {"Order": order.identifier,
                   "Starting time": order.start_time,
                   "End time": order.end_time,
                   "Execution time": order.execution_time,
                   "Deadline": order.deadline}
        
        self.df.loc[len(self.df)] = new_row
        
        new_val = self.stock[len(self.stock) - 1][1]
        if now < order.deadline:
            new_val += num_processed
            order.is_in_stock = True
            self.update_queue.append(order)
        
        for o in self.update_queue:
            if now >= o.deadline:
                if order.is_in_stock:
                    new_val -= order.original_size
                self.update_queue.remove(o)
        
        self.stock.append((now, new_val))
        self.stock.sort(key=lambda x: x[0])
        logging.info(f"Appending DataFrame {self.name}")
        self.mutex.release()
        
    def draw(self, name, ax_stock, ax_tn, color, lines_tn):
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
            
            if color is not None:
                # line_rr = ax_rr.plot(x_values, self.df["Response ratio"], label=name, color=color)[0]
                # ax_stock.plot(self.stock[selected_type], label=name, color=color)[0]
                # ax_stock.set_xlim([0, len(self.stock[OrderType.LOW_QUALITY])])
                # self.stock.sort()
                
                stock_val = []
                stock_time = []
                
                for (time, stock) in self.stock:
                    stock_time.append(time)
                    stock_val.append(stock)
                    
                ax_stock.plot(stock_time, stock_val, label=name, color=color)[0]
                ax_stock.set_xlim([0, stock_time[-1]])
            else:
                # line_rr = ax_rr.plot(x_values, self.df["Response ratio"], label=name)[0]
                # self.stock.sort()
                
                stock_val = []
                stock_time = []
                
                for (time, stock) in self.stock:
                    stock_time.append(time)
                    stock_val.append(stock)
                    
                ax_stock.plot(stock_time, stock_val, label=name)[0]
                ax_stock.set_xlim([0, stock_time[-1]])
                # print(self.stock[-1])

            # ax_rr.set_yscale('log')

            self.df["Tardiness"] = (self.df["End time"] - self.df["Deadline"]).clip(lower=0)
            if self.df is not None:
                self.df.sort_values("Tardiness", inplace=True)
                self.df = self.df.reset_index(drop=True)
                x_values = np.linspace(0, 100, len(self.df)) 
            
            line_tn = None
            if color is not None:
                line_tn = ax_tn.plot(x_values, self.df["Tardiness"], label=name, color=color)[0]
                lines_tn.append(line_tn)
            else:
                line_tn = ax_tn.plot(x_values, self.df["Tardiness"], label=name)[0]
                lines_tn.append(line_tn)

            # ax_tn.set_yscale('log')
        self.mutex.release()
        
        return lines_tn
        
    def log_info(self):
        self.mutex.acquire()
        if self.df.empty:
            logging.error(f"Empty DataFrame when printing {self.name}")
        else:
            logging.info(f"Printing DataFrame {self.name}")
            logging.info(self.df)
        self.mutex.release()