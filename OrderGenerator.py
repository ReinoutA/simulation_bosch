import salabim as sim
import logging
import random
from Config import *
import Config
from Order import Order
from OrderType import OrderType
import pandas as pd
import time

class OrderGenerator(sim.Component):
    def __init__(self, queues, machines, env, reports):
        super().__init__()
        self.queues = queues
        self.num_generated = 0
        self.machines = machines
        self.env = env
        self.reports = reports
        self.total_hold_time = 0
        self.total_produced = {}
        for material in Config.materials:
            self.total_produced[material] = pd.read_csv(f"Data/total_produced_{material}.csv")
        
    def process(self):
        total_hold_time = 0
        while Config.simulation_running and Config.gui_running:
            random_order_type = random.choices(Config.order_types, weights=Config.order_type_weights, k=1)[0]
            material = str(random_order_type).replace("OrderType.", "").split("_")[0]
            sampled_row = self.total_produced[material].sample(n=1)
            size = sampled_row["total produced"].values[0]
            # size = max(ORDER_MIN_SIZE, abs(int(sim.Normal(ORDER_SIZE_MEAN, ORDER_SIZE_STD).sample())))

            self.num_generated += 1
            hold_time = abs(sim.Normal(ORDER_INTERVAL_MEAN, ORDER_INTERVAL_STD).sample())
            if SLEEP_FACTOR > 0.0:
                time.sleep(SLEEP_FACTOR)
            total_hold_time += hold_time
            
            #logging.info(total_hold_time)
            self.hold(hold_time)
            
            start_time = int(self.env.now())
            deadline = int(start_time + min(DEADLINE_MIN, sim.Normal(DEADLINE_MEAN, DEADLINE_STD).sample()) * DAYS_IN_WEEK * HOURS_IN_DAY * MINUTES_IN_HOUR)
            transition_time = sim.Gamma(Config.SHAPE_PARAM, Config.SCALE_PARAM).sample()
                
            for i in range(len(self.queues)):
                # deadline = max(DEADLINE_MIN, abs(int(sim.Normal(DEADLINE_MEAN, DEADLINE_STD).sample())))
                order = Order(random_order_type, size, start_time, deadline, transition_time, 0, 1, self.env, self.reports[i])
                self.queues[i].add(order)
                
                for machine in self.machines[i]:
                    if machine.status() == 'passive':
                        machine.activate()
        
    def create_report(self):
        logging.info(f"Ordergenerator generated {self.num_generated} orders")