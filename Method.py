import logging
import Config

class Method:
    def __init__(self, name):
        self.name = name
        
    def schedule_next(self, machine):
        logging.error("Scheduling called on Method class is invalid")
        return None, 0