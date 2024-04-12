import salabim as sim
from enum import Enum
import random
import csv
import time

TIME_LIMIT = 365
ENABLE_SIM_TRACE = True
LOG_QUEUES = True
methods = ["FCFS", "SJF", "HRRN"]

class OrderType(Enum):
    HIGH_QUALITY = 0
    MEDIUM_QUALITY = 1
    LOW_QUALITY = 2

class Machine(sim.Component):
    num_machines = 1
    
    def __init__(self, transition_per_type_combination, runtime_per_type, can_do_list, global_queue, machines, method):
        super().__init__()
        self.id = Machine.num_machines
        Machine.num_machines += 1
        # self.queue = sim.Queue(f"Machine queue {self.id}")
        self.queue = global_queue
        self.total_transition_time = 0
        self.last_order_type = 0
        self.total_profit = 0
        self.transition_per_type_combination = transition_per_type_combination
        self.runtime_per_type = runtime_per_type
        self.can_do_list = can_do_list
        self.machines = machines
        self.method = method
        
    def process(self):
        while True:
            if len(self.queue) == 0:
                self.passivate()
                
            # FCFS
            if self.method == "FCFS":
                order = self.queue.pop()
            
            # SJF
            elif self.method == "SJF":
                order = None
                min_size = 1E30
                for o in self.queue:
                    if o.size < min_size and o.type in self.can_do_list:
                        min_size = o.size
                        order = o
                self.queue.remove(order)
                    
            # HRRN   
            elif self.method == "HRRN":
                order = None
                worst_val = 0
                now = env.now()
                
                for o in self.queue:
                    if o.type in self.can_do_list:
                        execution_time = o.size / self.runtime_per_type[o.type]
                        val = o.get_response_ratio(now, execution_time)
                        if val >= worst_val:
                            worst_val = val
                            order = o
                self.queue.remove(order)
                
            if order is not None:
                if order.type not in self.can_do_list:
                    self.queue.add(order)
                    for machine in machines:
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
                self.hold(execution_time)
                order.end_time = env.now()
                order.execution_time = execution_time
                order.report()
            
class Order(sim.Component):
    counter = 0
    
    def __init__(self, type, size, deadline, received_date, profit, method):
        super().__init__()
        self.identifier = Order.counter
        Order.counter += 1
        self.type = type
        self.size = abs(size)
        self.deadline = deadline
        self.received_date = received_date
        self.profit = profit
        self.start_time = env.now()
        self.end_time = None
        self.execution_time = None
        self.method = method
        
    def report(self):
        with open(f"report_{self.method}.csv", "a", newline = "") as file:
            writer = csv.writer(file)
            writer.writerow([self.identifier, self.start_time, self.end_time, self.execution_time])
            
    def get_response_ratio(self, now, execution_time):
        return (now - self.start_time) / execution_time
       
class OrderGenerator(sim.Component):
    def __init__(self, queue, method):
        super().__init__()
        self.queue = queue
        self.num_generated = 0
        self.method = method
        
    def process(self):
        order_types = list(OrderType)
        order_type_weights = [0.1, 0.3, 0.6]  # adjust these values to your needs
        
        while env.now() < TIME_LIMIT:
            random_order_type = random.choices(order_types, weights=order_type_weights, k=1)[0]
            self.queue.add(Order(random_order_type, sim.Normal(100000, 50000).sample(), 0, 0, 1, self.method))
            self.num_generated += 1
            self.hold(abs(sim.Normal(7, 1).sample()))
            
            for machine in machines:
                if machine.status() == 'passive':
                    machine.activate()
        
    def report(self):
        print(f"Generated {self.num_generated} orders")
   

for method in methods:
    print(method) 
    with open(f"report_{method}.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["Order", "Starting time", "End time", "Execution time"])
        
    env = sim.Environment(trace=ENABLE_SIM_TRACE)
    env.random_seed(int(time.time()))

    queues = []

    transitions = {
        (OrderType.HIGH_QUALITY, OrderType.HIGH_QUALITY) : 0,
        (OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY) : 30,
        (OrderType.HIGH_QUALITY, OrderType.LOW_QUALITY) : 30,
        (OrderType.MEDIUM_QUALITY, OrderType.MEDIUM_QUALITY) : 0,
        (OrderType.MEDIUM_QUALITY, OrderType.HIGH_QUALITY) : 60,
        (OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY) : 30,
        (OrderType.LOW_QUALITY, OrderType.LOW_QUALITY) : 0,
        (OrderType.LOW_QUALITY, OrderType.HIGH_QUALITY) : 60,
        (OrderType.LOW_QUALITY, OrderType.MEDIUM_QUALITY) : 30,
    }

    runtime = [
        {
            OrderType.HIGH_QUALITY : 200000,
            OrderType.MEDIUM_QUALITY : 200000,
            OrderType.LOW_QUALITY : 200000,
        },
        {
            OrderType.HIGH_QUALITY : 100000,
            OrderType.MEDIUM_QUALITY : 200000,
            OrderType.LOW_QUALITY : 500000,
        },
        {
            OrderType.HIGH_QUALITY : 300000,
            OrderType.MEDIUM_QUALITY : 300000,
            OrderType.LOW_QUALITY : 400000,
        },
        {
            OrderType.HIGH_QUALITY : 60000,
            OrderType.MEDIUM_QUALITY : 280000,
            OrderType.LOW_QUALITY : 1000000,
        },
        {
            OrderType.HIGH_QUALITY : 300000,
            OrderType.MEDIUM_QUALITY : 300000,
            OrderType.LOW_QUALITY : 400000,
        },
    ]

    can_do_lists = [
        [OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY],
        [OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY],
        [OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY],
        [OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY],
        [OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY],
    ]

    global_queue = sim.Queue("Global queue")

    machines = []
    for i in range(5):
        machine = Machine(transitions, runtime[i], can_do_lists[i], global_queue, machines, method)
        machines.append(machine)

    for machine in machines:
        queues.append(machine.queue)

    generator = OrderGenerator(global_queue, method)
    generator.activate()

    for machine in machines:
        if machine.status() != 'passive':
            machine.activate()
        
    env.run()
    if LOG_QUEUES:
        global_queue.print_statistics()

    max_len = 0
    for i, machine in enumerate(machines, start=1):
        string = f"Machine {i} made {machine.total_profit} profit, waited {machine.total_transition_time} on transitions."
        print(string)
        if len(string) > max_len:
            max_len = len(string)
            
    print("-" * max_len)

    generator.report()