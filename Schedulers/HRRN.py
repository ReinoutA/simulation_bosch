from Method import *

class HRRN(Method):
    def __init__(self):
        super().__init__("HRRN")
        
    def schedule_next(self, machine):
        worst_val = 0
        now = machine.env.now()
        order = None
        
        for o in machine.queue:
            if o.type in machine.configuration.can_do_list:
                execution_time = o.size / machine.configuration.runtime[o.type]
                val = o.get_response_ratio(now, execution_time)
                if val >= worst_val:
                    worst_val = val
                    order = o
                    
        if order is not None:
            machine.queue.remove(order)
            return order, order.size
        else:
            return None, 0