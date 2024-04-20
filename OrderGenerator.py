import salabim as sim
import logging
import random
from Config import *
import Config
from Order import Order
from OrderType import OrderType

class OrderGenerator(sim.Component):
    def __init__(self, queue, method, machines, env, report):
        super().__init__()
        self.queue = queue
        self.num_generated = 0
        self.method = method
        self.machines = machines
        self.env = env
        self.report = report

    def process(self):
        order_types = list(OrderType)
        order_type_weights = [0.1, 0.3, 0.6]  # adjust these values to your needs
        
        print(Config.gui_running)
        while Config.gui_running:
            print("ping")
            random_order_type = random.choices(order_types, weights=order_type_weights, k=1)[0]
            self.queue.add(Order(random_order_type, sim.Normal(ORDER_SIZE_MEAN, ORDER_SIZE_STD).sample(), 0, 0, 1, self.method, self.env, self.report))
            self.num_generated += 1
            self.hold(abs(sim.Normal(ORDER_INTERVAL_MEAN, ORDER_INTERVAL_STD).sample()))
            
            for machine in self.machines:
                if machine.status() == 'passive':
                    machine.activate()
        
    def create_report(self):
        logging.info(f"Ordergenerator generated {self.num_generated} orders")