import salabim as sim

class CustomerGenerator(sim.Component):
    def process(self):
        print(env.now())
        while True:
            Customer()
            self.hold(sim.Uniform(5, 15).sample())


class Customer(sim.Component):
    def process(self):
        self.enter(waitingline)
        if clerk.ispassive():
            clerk.activate()
        # Removed yield statement
        self.passivate()


class Clerk(sim.Component):
    def process(self):
        while True:
            while len(waitingline) == 0:
                # Removed yield statement
                self.passivate()
            self.customer = waitingline.pop()
            self.hold(30)
            self.customer.activate()


env = sim.Environment(trace=True)

CustomerGenerator()
clerk = Clerk()
waitingline = sim.Queue("waitingline")

env.run(till=50)
print()
waitingline.print_statistics()
