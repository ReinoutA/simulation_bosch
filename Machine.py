import salabim as sim
from Config import *

class Machine(sim.Component):
    num_machines = 1
    
    def __init__(self, transition_per_type_combination, runtime_per_type, can_do_list, global_queue, machines, method, env):
        super().__init__()
        self.id = Machine.num_machines
        Machine.num_machines += 1
        self.queue = global_queue
        self.total_transition_time = 0
        self.last_order_type = 0
        self.total_profit = 0
        self.transition_per_type_combination = transition_per_type_combination
        self.runtime_per_type = runtime_per_type
        self.can_do_list = can_do_list
        self.machines = machines
        self.method = method
        self.total_execution_time = 0
        self.env = env
        
    def process(self):
        while Config.simulation_running and Config.gui_running:
            if len(self.queue) == 0:
                self.passivate()
                
            order, profit = self.method.schedule_next(self)
            
            if order is not None:
                if order.type not in self.can_do_list:
                    self.queue.add(order)
                    for machine in self.machines:
                        if machine.status() != 'passive':
                            machine.activate()
                    self.passivate()
                
                if self.last_order_type != 0:
                    transition_time = self.get_transition_time(order)
                    self.total_transition_time += transition_time
                    self.hold(transition_time)

                self.last_order_type = order.type
                self.total_profit += profit
                execution_time = self.get_execution_time(order)
                self.total_execution_time += execution_time
                self.hold(execution_time)
                order.end_time = self.env.now()
                order.execution_time += execution_time
                order.create_report()
                
    def get_transition_time(self, order):
        return self.transition_per_type_combination.get((self.last_order_type, order.type), 0)
    
    def get_execution_time(self, order):
        return order.size / self.runtime_per_type[order.type]