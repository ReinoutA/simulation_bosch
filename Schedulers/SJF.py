from Method import *

class SJF(Method):
    def __init__(self):
        super().__init__("SJF")
        
    def schedule_next(self, machine):
        min_size = 1E30
        order = None
        
        for o in machine.queue:
            if o.size < min_size and o.type in machine.configuration.can_do_list:
                min_size = o.size
                order = o
                
        if order is not None:
            machine.queue.remove(order)
            return order, order.profit
        else:
            return None, 0