import salabim as sim

class Order(sim.Component):
    counter = 0
    
    def __init__(self, type, size, deadline, received_date, profit, env, report):
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
        self.execution_time = 0
        self.report = report
        
    def create_report(self):
        self.report.append(self)
            
    def get_response_ratio(self, now, execution_time):
        return (now - self.start_time) / execution_time