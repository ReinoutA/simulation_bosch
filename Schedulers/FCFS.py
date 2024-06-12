from Method import *

class FCFS(Method):
    def __init__(self):
        super().__init__("FCFS")
        
    def schedule_next(self, machine):
        # if machine.last_order_type != 0:
        #     for order in machine.queue:
        #         if order is not None and order.type == machine.last_order_type and machine.configuration.can_do_list:
        #             break
                
        for order in machine.queue:
            if order is not None and machine.configuration.can_do_list:
                machine.queue.remove(order)
                return order, order.size
        return None, 0