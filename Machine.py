import salabim as sim
import numpy as np

class Machine(sim.Component):
    def __init__(self, runtime, transition, allowed_types, order_queue):
        super().__init__()
        self.runtime_per_type = runtime
        self.transition_per_type_combination = transition
        self.allowed_types = allowed_types
        
        self.total_produced = 0
        self.total_profit = 0
        self.total_waste = 0
        self.total_transition_time = 0

        self.order_queue = order_queue
        self.last_order_type = None

    def process(self):
        while True:
            while len(self.order_queue) == 0:
                self.passivate()
            
            order = self.order_queue.pop()
            
            if self.last_order_type:
                transition_time = self.transition_per_type_combination.get((self.last_order_type, self.customer.type), 0)
                self.total_transition_time += transition_time
                self.hold(transition_time)

            self.last_order_type = order.type
            self.total_profit += order.profit
            self.hold(order.size * self.runtime_per_type[order.type])