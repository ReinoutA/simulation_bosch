import logging

import Config
from Gui import Gui
from Simulation import Simulation

with open("log.txt", "w+") as f:
    pass

logging.basicConfig(filename="log.txt", level=logging.INFO)

with open(f"env.txt", "w+") as file:
    pass

global reports
reports = []

Config.gui_running = True
Gui(reports).start()
Simulation(reports).start()