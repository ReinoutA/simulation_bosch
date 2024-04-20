import salabim as sim
import time

from Machine import Machine
from Config import *
from OrderGenerator import OrderGenerator
from DataReport import DataReport
from threading import Thread

class Simulation(Thread):
    def __init__(self, index):
        Thread.__init__(self)

        self.env = sim.Environment(trace=open(f"env.txt", "w"))
        self.env.random_seed(int(time.time()))
        self.index = index

        self.queues = []
        self.global_queue = sim.Queue("Global queue")
        self.report = DataReport(methods[self.index])

        self.machines = []
        for i in range(5):
            machine = Machine(transitions, runtime[i], can_do_lists[i], self.global_queue, self.machines, methods[index], self.env)
            self.machines.append(machine)

        for machine in self.machines:
            self.queues.append(machine.queue)

        self.generator = OrderGenerator(self.global_queue, methods[index], self.machines, self.env, self.report)
        
    def run(self):
        self.generator.activate()

        for machine in self.machines:
            if machine.status() != 'passive':
                machine.activate()
        
        self.env.run()

    def create_report(self):
        self.global_queue.print_statistics()
        self.report.print()

    def draw(self, name, ax, color):
        self.report.draw(name, ax, color)