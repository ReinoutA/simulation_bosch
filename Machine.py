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
        
    def process(self):
        while Config.simulation_running and Config.gui_running:
            if len(self.queue) == 0:
                self.passivate()
                            
            order, num_processed = self.method.schedule_next(self)
            # print(f"Machine {self.id}")
            
            if order is not None:
                if order.type not in self.configuration.can_do_list:
                    self.queue.add(order)
                    for machine in self.machines:
                        if machine.status() != 'passive':
                            machine.activate()
                    self.passivate()
                
                if self.last_order_type != 0:
                    transition_time = sim.Gamma(Config.SHAPE_PARAM, Config.SCALE_PARAM).sample()
                    self.total_transition_time += transition_time
                    self.hold(transition_time)

                self.last_order_type = order.type
                self.total_profit += int(order.profit * num_processed / order.size)
                execution_time = self.get_execution_time(order)
                self.total_execution_time += execution_time
                self.hold(execution_time)
                now = self.env.now()
                if 1 - (num_processed / order.size) < 0.05:
                    order.end_time = now
                order.size -= num_processed
                order.execution_time += execution_time
                order.create_report(num_processed, now)
            else:
                self.passivate()
                
    def get_transition_time(self, order):
        if self.last_order_type == order.type:
            return 0
        return self.configuration.transitions.get((self.last_order_type, order.type), 0).sample()
    
    def get_execution_time(self, order):
        return order.size / self.configuration.get_runtime(order.type)
    
    def get_priority_list(self):
        return self.configuration.priority_list