import salabim as sim
import logging
import random
from Config import *
import Config
from Order import Order
from OrderType import OrderType

class OrderGenerator(sim.Component):
    def __init__(self, queues, machines, env, reports):
        super().__init__()
        self.queues = queues
        self.num_generated = 0
        self.machines = machines
        self.env = env
        self.reports = reports

    def process(self):
        order_types = list(OrderType)
        order_type_weights = [0.1, 0.3, 0.6]  # adjust these values to your needs
        
        while Config.simulation_running and Config.gui_running:
            random_order_type = random.choices(order_types, weights=order_type_weights, k=1)[0]
            
            size = abs(int(sim.Normal(ORDER_SIZE_MEAN, ORDER_SIZE_STD).sample()))
            self.num_generated += 1
            self.hold(abs(sim.Normal(ORDER_INTERVAL_MEAN, ORDER_INTERVAL_STD).sample()))
            
            for i in range(len(self.queues)):
                order = Order(random_order_type, size, 0, 0, 1, self.env, self.reports[i])
                self.queues[i].add(order)
                
                for machine in self.machines[i]:
                    if machine.status() == 'passive':
                        machine.activate()
        
    def create_report(self):
        logging.info(f"Ordergenerator generated {self.num_generated} orders")