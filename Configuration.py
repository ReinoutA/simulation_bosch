import pandas as pd
import threading
from Config import *
import Config

# This class contains logic for the machines to determine parameters like runtime and error rate. The machine calls the
# get_sample method to get a sample of the runtime and error rate for a specific order type. This is done by sampling from the dataframe
# that is loaded in the constructor. The machine also has a mutex lock to prevent. The historic samples are found in the Data folder.

class Configuration:
    num_configurations = 0
            
    def __init__(self, can_do_list, priority_list):
        self.name = f"Machine {Configuration.num_configurations}"
        Configuration.num_configurations += 1
        self.can_do_list = can_do_list
        self.priority_list = priority_list
        self.dfs = {}
        for type in self.can_do_list:
            self.dfs[type] = pd.read_csv(f"Data/{Config.line_numbers[Configuration.num_configurations - 1]}_{str(type).replace('OrderType.', '')}.csv")
        self.mutex = threading.Lock()
        
    def get_sample(self, order_type):
        sampled_row = self.dfs[order_type].sample(n=1)
        runtime = sampled_row["production speed [PC / min]"].values[0]
        sampled_row = self.dfs[order_type].sample(n=1)
        error_rate = sampled_row["error rate"].values[0]
        return runtime, error_rate
        