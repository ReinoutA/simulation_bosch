import salabim as sim

class Order(sim.Component):
    counter = 0
    
    def __init__(self, type, size, start_time, deadline, transition_time, received_date, profit, env, report):
        super().__init__()
        self.identifier = Order.counter
        Order.counter += 1
        self.type = type
        self.size = abs(size)
        self.original_size = self.size
        self.start_time = start_time
        self.deadline = deadline
        self.received_date = received_date
        self.profit = profit
        self.end_time = None
        self.execution_time = 0
        self.report = report
        self.num_processed = 0
        self.is_in_stock = False
        self.transition_time = transition_time
        
    def create_report(self, num_processed, now, total_transition_time, total_produced, total_uptime):
        self.report.append(self, num_processed, now, total_transition_time, total_produced, total_uptime)
            
    def get_response_ratio(self, now, execution_time):
        return ((now - self.start_time) + execution_time) / execution_time
    
    def get_time_left(self, now):
        return self.deadline - now