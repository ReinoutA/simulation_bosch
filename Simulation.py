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
        
        # class AdjustSpeedProcess(sim.Component):
        #     def process(self):
        #         while True:
        #             self.hold(50)
        #             env.speed(2)  # Increase the speed
        #             self.hold(50)
        #             env.speed(0.5)  # Decrease the speed

        # # Don't forget to create an instance of your components and start them
        # AdjustSpeedProcess()

        env.run()

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