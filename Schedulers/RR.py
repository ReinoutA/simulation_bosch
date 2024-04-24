from Method import *
    
class RR(Method):
    def __init__(self, window_size):
        # window_size = 7
        super().__init__(f"RR-{int(window_size)}")
        self.window_size = int(window_size)
        
    def schedule_next(self, machine):
        profit = 0
        if len(machine.queue) > 0:
            order = machine.queue[0]
            machine.queue.remove(order)
        
            execution_time = machine.get_execution_time(order)
            if execution_time > self.window_size:
                left_over = int((execution_time - self.window_size) * machine.configuration.runtime[order.type])
                profit = order.profit * (1 - (left_over / order.size))
                order.size = left_over
                machine.queue.add(order)
                
                for machine in machine.machines:
                    if machine.status() != 'passive':
                        machine.activate()
                        
            return order, profit
        else:
            return None, 0