import salabim as sim
from enum import Enum
import random
import numpy as np

class orderType(Enum):
    TYPE1 = 1
    TYPE2 = 2
    TYPE3 = 3

class OrderGenerator(sim.Component):
    def process(self):
        print(env.now())
        order_types = list(orderType)
        while True:
            random_order_type = random.choice(order_types)
            Order(type=random_order_type, size=sim.Normal(50, 2).sample())
            self.hold(abs(sim.Normal(0.1, 1).sample()))

class Order(sim.Component):
    def __init__(self, type, size):
        super().__init__()  # Call the __init__ method of the parent class
        self.type = type
        self.size = size

    def process(self):
        self.enter(orderQueue)
        
        for machine in machines:
            if machine.ispassive():
                machine.activate()

        self.passivate()

class Machine(sim.Component):
    def __init__(self, speed):
        super().__init__()
        self.order_count = 0
        self.speed = speed

    def process(self):
        while True:
            while len(orderQueue) == 0:
                self.passivate()
            self.customer = orderQueue.pop()
            # if self.customer.processing_time > self.env.now():
            #     self.hold(self.customer.processing_time - self.env.now())
            self.hold(np.ceil(self.customer.size / self.speed))
            self.customer.activate()
            self.order_count += 1

env = sim.Environment(trace=True)

OrderGenerator().activate()
machines = [0 for _ in range(5)]
for i in range(5):
    machines[i] = Machine(speed=int(abs(sim.Uniform(0, 5).sample())))
    machines[i].activate()
orderQueue = sim.Queue("orderQueue")

env.run(till=500)
print()
orderQueue.print_statistics()

# Print the number of orders processed by each machine
for i, machine in enumerate(machines, start=1):
    print(f"Machine {i} processed {machine.order_count} orders @ {machine.speed}")