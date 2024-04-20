import logging
import Config

class Method:
    def __init__(self, name):
        self.name = name
        
    def schedule_next(self, machine):
        logging.error("Scheduling called on Method class is invalid")
        return None, 0

class FCFS(Method):
    def __init__(self):
        super().__init__("FCFS")
        
    def schedule_next(self, machine):
        order = machine.queue.pop()
        if order is not None:
            return order, order.profit
        return None, 0
    
class SJF(Method):
    def __init__(self):
        super().__init__("SJF")
        
    def schedule_next(self, machine):
        min_size = 1E30
        order = None
        
        for o in machine.queue:
            if o.size < min_size and o.type in machine.can_do_list:
                min_size = o.size
                order = o
                
        if order is not None:
            machine.queue.remove(order)
            return order, order.profit
        else:
            return None, 0
    
class HRRN(Method):
    def __init__(self):
        super().__init__("HRRN")
        
    def schedule_next(self, machine):
        worst_val = 0
        now = machine.env.now()
        order = None
        
        for o in machine.queue:
            if o.type in machine.can_do_list:
                execution_time = o.size / machine.runtime_per_type[o.type]
                val = o.get_response_ratio(now, execution_time)
                if val >= worst_val:
                    worst_val = val
                    order = o
                    
        if order is not None:
            machine.queue.remove(order)
            return order, order.profit
        else:
            return None, 0
        
class PS(Method):
    def __init__(self):
        super().__init__("PS")
        
    def schedule_next(self, machine):
        orders = [None] * len(Config.PRIORITY_LIST)
        order = None
        
        for o in machine.queue:
            if o.type in machine.can_do_list:
                for i, o_type in enumerate(Config.PRIORITY_LIST):
                    if o.type == o_type:
                        orders[i] = o
                        break
        
        for elem in orders:
            if elem is not None:
                order = elem
                break
            
        if order is not None:
            machine.queue.remove(order)
            return order, order.profit
        else:
            return None, 0
    
class RR(Method):
    def __init__(self, window_size):
        super().__init__(f"RR-{window_size}")
        self.window_size = window_size
        
    def schedule_next(self, machine):
        profit = 0
        if len(machine.queue) > 0:
            order = machine.queue[0]
            machine.queue.remove(order)
        
            execution_time = machine.get_execution_time(order)
            if execution_time > self.window_size:
                left_over = int((execution_time - self.window_size) * machine.runtime_per_type[order.type])
                profit = order.profit * (1 - (left_over / order.size))
                order.size = left_over
                machine.queue.add(order)
                
                for machine in machine.machines:
                    if machine.status() != 'passive':
                        machine.activate()
                        
            return order, profit
        else:
            return None, 0