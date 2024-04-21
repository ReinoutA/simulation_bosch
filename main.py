import logging

import Config
from Gui import Gui

with open("log.txt", "w+") as f:
    pass
logging.basicConfig(filename="log.txt", level=logging.INFO)

with open(f"env.txt", "w+") as file:
    pass

Config.gui_running = True
Gui().start()