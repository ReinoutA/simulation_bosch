class Configuration:
    num_configurations = 0
            
    def __init__(self, can_do_list, priority_list):
        self.name = f"Machine {Configuration.num_configurations}"
        Configuration.num_configurations += 1
        self.can_do_list = can_do_list
        self.priority_list = priority_list
        
    def get_runtime(self, order_type):
        return 1000