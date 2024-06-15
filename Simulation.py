import salabim as sim
import time

from Machine import Machine
from Config import *
from OrderGenerator import OrderGenerator
from DataReport import DataReport
from threading import Thread

# This is the class that contains all the logic to do the simulation of all the algorithms.
# Since we are using salabim, we can only create one environment called env. In order to run multiple scheduling situations
# at the same time we use a trick. For each scheduling situation we create a global queue and a list of machines. Each queue
# is connected to the machines in the list. We then create a OrderGenerator that generates orders for all the queues and machines.
# Each queue receives the same orders from the OrderGenerator.

class Simulation(Thread):
    def __init__(self, reports):
        super().__init__()
        self.reports = reports
        
    def run(self):
        env = sim.Environment(trace=ENABLE_SIM_TRACE)
        env.random_seed(int(time.time()))
        global_queues = []
        all_machines = []
        
        for index in range(len(Config.methods)):
            global_queues.append(sim.Queue(f"Global queue {index}"))
            report = DataReport(Config.methods[index].name)
            self.reports.append(report)

            machines = []
            for i in range(len(Config.configurations)):
                machine = Machine(global_queues[index], machines, Config.methods[index], env, Config.configurations[i])
                machines.append(machine)

            queues = []
            for machine in machines:
                queues.append(machine.queue)

            all_machines.append(machines)
            for machine in machines:
                if machine.status() != 'passive':
                    machine.activate()
            
        generator = OrderGenerator(global_queues, all_machines, env, self.reports)
        generator.activate()

        env.run()   # Start the simulation

        if LOG_QUEUES:
            for global_queue in global_queues:
                global_queue.print_statistics()

        max_len = 0
        if LOG_MACHINES:
            for machines in all_machines:
                for i, machine in enumerate(machines, start=1):
                    string = f"Machine {i} made {machine.total_profit} profit, waited {machine.total_transition_time} on transitions, executed {machine.total_execution_time}."
                    print(string)
                    if len(string) > max_len:
                        max_len = len(string)
            
        print("-" * max_len)

        if LOG_GENERATOR:
            generator.create_report()
            
        if LOG_DATAFRAMES:
            for report in self.reports:
                report.log_info()