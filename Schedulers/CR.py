# Critical Ratio (CR): Dit algoritme berekent de verhouding tussen de resterende tijd tot de deadline en de verwerkingstijd van een taak. Taken worden vervolgens gesorteerd op basis van deze verhouding, waarbij taken met de laagste ratio voorrang krijgen. 
# Dit helpt bij het minimaliseren van de vertraging in verhouding tot de resterende tijd.

from Method import Method

class CR(Method):
    def __init__(self):
        super().__init__("CR")
        
    def schedule_next(self, machine):
        worst_val = 1E30
        order = None
        now = machine.env.now()

        for o in machine.queue:
            if o.size < worst_val / machine.get_execution_time(o) and o.type in machine.configuration.can_do_list:
                worst_val = o.get_time_left(now)
                order = o
                
        if order is not None:
            machine.queue.remove(order)
            return order, order.profit
        else:
            return None, 0