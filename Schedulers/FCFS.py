from Method import *

class FCFS(Method):
    def __init__(self):
        super().__init__("FCFS")
        
    def schedule_next(self, machine):
        order = machine.queue.pop()
        if order is not None:
            return order, order.profit
        return None, 0