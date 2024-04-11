import salabim as sim
from enum import Enum
import random

class OrderType(Enum):
    HIGH_QUALITY = 0
    MEDIUM_QUALITY = 1
    LOW_QUALITY = 2

class Machine(sim.Component):
    num_machines = 1
    
    def __init__(self, transition_per_type_combination, runtime_per_type, can_do_list):
        super().__init__()
        self.id = Machine.num_machines
        Machine.num_machines += 1
        self.queue = sim.Queue(f"Machine queue {self.id}")
        self.total_transition_time = 0
        self.last_order_type = 0
        self.total_profit = 0
        self.transition_per_type_combination = transition_per_type_combination
        self.runtime_per_type = runtime_per_type
        self.can_do_list = can_do_list
        
    def process(self):
        while True:
            if len(self.queue) == 0:
                self.passivate()

            order = self.queue.pop()
            
            if self.last_order_type != 0:
                transition_time = self.transition_per_type_combination.get((self.last_order_type, order.type), 0)
                self.total_transition_time += transition_time
                self.hold(transition_time)

            self.last_order_type = order.type
            self.total_profit += order.profit
            self.hold(order.size * self.runtime_per_type[order.type])
            
    def can_do(self, order):
        return order.type in self.can_do_list
            
class Order(sim.Component):
    def __init__(self, type, size, deadline, received_date, profit):
        super().__init__()
        self.type = type
        self.size = abs(size)
        self.deadline = deadline
        self.received_date = received_date
        self.profit = profit
       
class OrderGenerator(sim.Component):
    def __init__(self, queue, scheduler):
        super().__init__()
        self.queue = queue
        self.scheduler = scheduler
        
    def process(self):
        order_types = list(OrderType)
        order_type_weights = [0.1, 0.3, 0.6]  # adjust these values to your needs
        
        while True:
            random_order_type = random.choices(order_types, weights=order_type_weights, k=1)[0]
            self.queue.add(Order(random_order_type, sim.Normal(5, 2).sample(), 0, 0, 1))
            self.scheduler.activate()
            self.hold(abs(sim.Normal(0.1, 1).sample()))
            
class Scheduler(sim.Component):
    def __init__(self, input_queue, outputs, machines):
        super().__init__()
        self.input = input_queue
        self.outputs = outputs
        self.machines = machines
    
    def process(self):
        i = 0
        
        while True:            
            if len(self.input) <= 0:
                self.passivate()
            else:
                i += 1
                if i == len(self.outputs):
                    i = 0
                    
                if self.machines[i].can_do(self.input.head()):
                    self.outputs[i].add(self.input.pop())
                    self.machines[i].activate()
             
env = sim.Environment(trace=True)

queues = []

transitions = {
    (OrderType.HIGH_QUALITY, OrderType.HIGH_QUALITY) : 0,
    (OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY) : 10,
    (OrderType.HIGH_QUALITY, OrderType.LOW_QUALITY) : 10,
    (OrderType.MEDIUM_QUALITY, OrderType.MEDIUM_QUALITY) : 0,
    (OrderType.MEDIUM_QUALITY, OrderType.HIGH_QUALITY) : 20,
    (OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY) : 10,
    (OrderType.LOW_QUALITY, OrderType.LOW_QUALITY) : 0,
    (OrderType.LOW_QUALITY, OrderType.HIGH_QUALITY) : 20,
    (OrderType.LOW_QUALITY, OrderType.MEDIUM_QUALITY) : 10,
}

runtime = {
    OrderType.HIGH_QUALITY : 20,
    OrderType.MEDIUM_QUALITY : 15,
    OrderType.LOW_QUALITY : 10,
}

can_do_lists = [[OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY], [OrderType.LOW_QUALITY], [OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY]]

machines = []
for i in range(3):
    machine = Machine(transitions, runtime, can_do_lists[i])
    machines.append(machine)

for machine in machines:
    queues.append(machine.queue)

global_queue = sim.Queue("Global queue")
scheduler = Scheduler(global_queue, queues, machines)
OrderGenerator(global_queue, scheduler).activate()
scheduler.activate()

for machine in machines:
    machine.activate()
    
env.run(till=100)

for queue in queues:
    queue.print_statistics()
global_queue.print_statistics()

for i, machine in enumerate(machines, start=1):
    print(f"Machine {i} made {machine.total_profit} profit, waited {machine.total_transition_time} on transitions.")