from Method import *
import Config
        
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