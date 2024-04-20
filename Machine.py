import salabim as sim
import threading
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
        while True:
            if len(self.queue) == 0:
                self.passivate()
                
            order = None
            
            # FCFS
            if self.method == "FCFS":
                order = self.queue.pop()
            
            # SJF
            elif self.method == "SJF":
                min_size = 1E30
                for o in self.queue:
                    if o.size < min_size and o.type in self.can_do_list:
                        min_size = o.size
                        order = o
                self.queue.remove(order)
                    
            # HRRN   
            elif self.method == "HRRN":
                worst_val = 0
                now = self.env.now()
                
                for o in self.queue:
                    if o.type in self.can_do_list:
                        execution_time = o.size / self.runtime_per_type[o.type]
                        val = o.get_response_ratio(now, execution_time)
                        if val >= worst_val:
                            worst_val = val
                            order = o
                self.queue.remove(order)
                
            # PS
            elif self.method == "PS":
                orders = [None] * len(PRIORITY_LIST)
                
                for o in self.queue:
                    if o.type in self.can_do_list:
                        for i, o_type in enumerate(PRIORITY_LIST):
                            if o.type == o_type:
                                orders[i] = o
                                break
                
                for elem in orders:
                    if elem is not None:
                        order = elem
                        break
                    
                self.queue.remove(order)
                
            # RR
            elif "RR-" in self.method:
                if len(self.queue) > 0:
                    order = self.queue[0]
                    self.queue.remove(order)
                
            if order is not None:
                if order.type not in self.can_do_list:
                    self.queue.add(order)
                    for machine in self.machines:
                        if machine.status() != 'passive':
                            machine.activate()
                    self.passivate()
                
                if self.last_order_type != 0:
                    transition_time = self.transition_per_type_combination.get((self.last_order_type, order.type), 0)
                    self.total_transition_time += transition_time
                    self.hold(transition_time)

                self.last_order_type = order.type
                self.total_profit += order.profit
                execution_time = order.size / self.runtime_per_type[order.type]
                self.total_execution_time += execution_time
                self.hold(execution_time)
                order.end_time = self.env.now()
                order.execution_time = execution_time
                order.create_report()
                
                if "RR-" in self.method:
                    window = int(self.method.split("-")[1])
                    
                    if execution_time > window:
                        left_over = int((execution_time - window) * self.runtime_per_type[order.type])
                        order.size = left_over
                        self.queue.add(order)
                        
                        for machine in self.machines:
                            if machine.status() != 'passive':
                                machine.activate()
