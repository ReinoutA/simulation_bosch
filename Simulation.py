import salabim as sim
import time

from Machine import Machine
from Config import *
from OrderGenerator import OrderGenerator
from DataReport import DataReport
from threading import Thread

class Simulation(Thread):
    def __init__(self, reports):
        super().__init__()
        self.reports = reports
        
    def run(self):
        env = sim.Environment(trace=ENABLE_SIM_TRACE)
        env.random_seed(int(time.time()))

        for index in range(len(methods)):
            global_queue = sim.Queue("Global queue")
            report = DataReport(methods[index])
            self.reports.append(report)

            machines = []
            for i in range(5):
                machine = Machine(transitions, runtime[i], can_do_lists[i], global_queue, machines, methods[index], env)
                machines.append(machine)

            queues = []
            for machine in machines:
                queues.append(machine.queue)

            generator = OrderGenerator(global_queue, methods[index], machines, env, report)
            generator.activate()

            for machine in machines:
                if machine.status() != 'passive':
                    machine.activate()
            
        env.run()

        if LOG_QUEUES:
            global_queue.print_statistics()

        max_len = 0
        if LOG_MACHINES:
            for i, machine in enumerate(machines, start=1):
                string = f"Machine {i} made {machine.total_profit} profit, waited {machine.total_transition_time} on transitions, executed {machine.total_execution_time}."
                print(string)
                if len(string) > max_len:
                    max_len = len(string)
            
        print("-" * max_len)

        if LOG_GENERATOR:
            generator.create_report()