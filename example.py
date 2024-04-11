import salabim as sim
from enum import Enum
import random

import OrderType
import Machine

class OrderGenerator(sim.Component):
    def process(self):
        print(env.now())
        order_types = list(orderType)
        order_type_weights = [0.1, 0.3, 0.6]  # adjust these values to your needs
        while True:
            random_order_type = random.choices(order_types, weights=order_type_weights, k=1)[0]
            Order(type=random_order_type, size=sim.Normal(50, 2).sample())
            self.hold(abs(sim.Normal(0.1, 1).sample()))

env = sim.Environment(trace=True)

OrderGenerator().activate()

transition_times = {
    (OrderType.HIGH_QUALITY, OrderType.MEDIUM_QUALITY): 5,
    (OrderType.HIGH_QUALITY, OrderType.LOW_QUALITY): 5,
    (OrderType.MEDIUM_QUALITY, OrderType.HIGH_QUALITY): 45,
    (OrderType.MEDIUM_QUALITY, OrderType.LOW_QUALITY): 15,
    (OrderType.LOW_QUALITY, OrderType.HIGH_QUALITY): 90,
    (OrderType.LOW_QUALITY, OrderType.MEDIUM_QUALITY): 30,
}

machines = [0 for _ in range(5)]
for i in range(5):
    machines[i] = Machine(speed=int(abs(sim.Uniform(0, 5).sample())))
    machines[i].activate()
orderQueue = sim.Queue("orderQueue")
env.run(till=500)
orderQueue.print_statistics()

for i, machine in enumerate(machines, start=1):
    print(f"Machine {i} processed {machine.order_count} orders @ {machine.speed}, waited {machine.total_transition_time} for transitions, order types: {machine.order_types}")