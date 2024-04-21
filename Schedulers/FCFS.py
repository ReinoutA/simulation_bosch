from Method import *

class FCFS(Method):
    def __init__(self):
        super().__init__("FCFS")
        
    def schedule_next(self, machine):
        for order in machine.queue:
            if order is not None and machine.configuration.can_do_list:
                machine.queue.remove(order)
                return order, order.profit
        return None, 0