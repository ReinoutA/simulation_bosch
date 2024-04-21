class Configuration:
    num_configurations = 0
    
    def __init__(self):
        self.name = f"Machine {Configuration.num_configurations}"
        Configuration.num_configurations += 1
        self.transitions = {}
        self.runtime = {}
        self.can_do_list = []
        self.priority_list = []
        
    def __init__(self, transitions, runtime, can_do_list, priority_list):
        self.name = f"Machine {Configuration.num_configurations}"
        Configuration.num_configurations += 1
        self.transitions = transitions
        self.runtime = runtime
        self.can_do_list = can_do_list
        self.priority_list = priority_list
        
    def add_type(self, type, runtime):
        self.runtime[type] = runtime
        self.can_do_list.append(type)
        self.priority_list.append(type)
        
    def remove_type(self, type):
        keys_to_remove = []
        for key, value in self.transitions.items():
            if key[0] == type or key[1] == type:
                keys_to_remove.append(key)

        for key in keys_to_remove:
            del self.transitions[key]
                
        del self.runtime[type]
        self.can_do_list.remove(type)
        self.priority_list.remove(type)
    
    def add_transition(self, type_from, type_to, cost):
        self.transitions[(type_from, type_to)] = cost