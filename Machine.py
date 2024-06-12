import salabim as sim
from Config import *

class Machine(sim.Component):
    num_machines = 1
    
    def __init__(self, global_queue, machines, method, env, configuration):
        super().__init__()
        self.id = Machine.num_machines
        Machine.num_machines += 1
        self.queue = global_queue
        self.total_transition_time = 0
        self.last_order_type = 0
        self.total_profit = 0
        self.machines = machines
        self.method = method
        self.total_execution_time = 0
        self.env = env
        self.configuration = configuration
        self.total_broken = 0
        self.runtime = 1.0
        self.error_rate = 0.0
        self.total_produced = 0
        
    def process(self):
        while Config.simulation_running and Config.gui_running:
            if len(self.queue) == 0:
                self.passivate()
                            
            order, num_processed = self.method.schedule_next(self)
            
            if order is not None:
                if order.size == 0:
                    print("Order size is 0, skipping")
                if order.type not in self.configuration.can_do_list:
                    self.queue.add(order)
                    for machine in self.machines:
                        if machine.status() != 'passive':
                            machine.activate()
                    self.passivate()
                else:
                    if self.last_order_type != 0:
                        transition_time = sim.Gamma(Config.SHAPE_PARAM, Config.SCALE_PARAM).sample()
                        self.total_transition_time += transition_time
                        self.hold(transition_time)

                    self.runtime, self.error_rate = self.configuration.get_sample(order.type)

                    self.last_order_type = order.type
                    if order.size == 0:
                        continue
                    
                    self.total_profit += int(order.profit * num_processed / order.size)
                    now = self.env.now()
                    if 1 - (num_processed / order.size) < 0.05:
                        order.end_time = now
                        
                    self.total_produced += num_processed
                    order.size -= num_processed
                    execution_time = int(num_processed / self.runtime)
                    order.execution_time += execution_time
                    self.total_execution_time += execution_time
                    self.hold(execution_time)
                    # print(f"order.type = {order.type}, self.runtime = {self.runtime}, self.error_rate = {self.error_rate}, order.size = {order.size}, order.execution_time = {order.execution_time}")
                    
                    total_transition_time = self.total_transition_time
                    total_produced = self.total_produced
                    for machine in self.machines:
                        total_transition_time += machine.total_transition_time
                        total_produced += machine.total_produced
                    
                    order.create_report(num_processed, now, total_transition_time, total_produced)
            else:
                self.passivate()
                
    def get_transition_time(self, order):
        if self.last_order_type == order.type:
            return 0
        return self.configuration.transitions.get((self.last_order_type, order.type), 0).sample()
    
    def get_runtime(self):
        return self.runtime
    
    def get_priority_list(self):
        return self.configuration.priority_list
    
    def get_error_rate(self):
        return self.error_rate
    
    def get_execution_time(self, order):
        return order.size / self.runtime