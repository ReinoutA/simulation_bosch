from Method import *

class SDD(Method):
    def __init__(self):
        super().__init__("SDD")
        
    def schedule_next(self, machine):
        min_time = 1E30
        order = None
        now = machine.env.now()

        for o in machine.queue:
            if o.size < min_time and o.type in machine.configuration.can_do_list:
                min_time = o.get_time_left(now)
                order = o
                
        if order is not None:
            machine.queue.remove(order)
            return order, order.profit
        else:
            return None, 0