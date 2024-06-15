# Project software simulation

This project is a simulation of three extrusion lines in the Bossch-factory in Tienen. We consider different scheduling algorithms and provide a simple framework in which new algorithms can be included.

Authors:

Brecht Van de Sijpe,

Reinout Annaert


Contact information in case of questions:

Brecht Van de Sijpe: brecht.van.de.sijpe@gmail.com

Reinout Annaert: reinout.annaert@gmail.com

## Setup
Our setup:

Python version: 3.12.2

Required packages: logging, numpy, salabim, pandas, threading, tkinter, greenlet, os, glob, inspect, time, random

To setup the project we would recomment the ussage of anaconda in order to use the libraries.

## Adding new algorithms

New algorithms can be added by inheriting the Method-class, located in Method.py . The FCFS examples shows us how:

1. Create a new file in the Schedulers folder, call this the name of your algorithm. The name should be without spaces or special characters. THe program automaticly detects the files and adds them to the model. You can select in the GUI which algorithms you want to compare. It is python code, so you make it end on ".py". In the case of First Come First Serve this is: "FCFS.py".

2. Write the necessary code for the scheduling algorithm.

```
from Method import *

class FCFS(Method):
    def __init__(self):
        super().__init__("FCFS")
        
    def schedule_next(self, machine):
        for order in machine.queue:
            if order is not None and machine.configuration.can_do_list:
                machine.queue.remove(order)
                return order, order.size
        return None, 0
```

Comment: In order to let the program correctly detect and use the scheduler, fill in the exact name of the file -".py" into the field of the super().__init__(<name>). The classname should be the same value. The scheduler is linked to a machine, you can access the current orderqueue for this machine via the "queue"-field of the machine. All scheduling logic starts and ends in the schedule_next-method. This method receives the machine it is assigned to and returns the next order to run and the amount of  pieces the machine has to run. This allows the programmer to let the machine process only a part of the order, adding the remaining part back into the queue and thus providing preemption if required. In case you want to process the full order you can return the "size"-field of the order as the second argument. For example SJF would then look like this in SJF.py:

```
from Method import *

class SJF(Method):
    def __init__(self):
        super().__init__("SJF")
        
    def schedule_next(self, machine):
        # Here you put the scheduling code
        return <the chosen order>, <amount of processed pieces>
```

3. In order to recognize the new algorithm in the program you have to include it in the "Config.py" file. In order to do this for the FCFS algorithm you can use this line:

```
from Schedulers.FCFS import FCFS
```

Comment: in your case you replace the "FCFS" in this line with the name of your algorithm.

## Setting config parameters

In Config.py all parameters can be changed. These include logging paramters, of which most logs can be found in the log.txt file. Logging of the queues is, when enabled, provided in the terminal.

## Model

Each scheduling-algorithm gets the same orders from the OrderGenerator, this is done so the algorithms can be compared in a fair way based on the same input. A diagram of the framework can be found in "Overview.png".

## Folders

Data folder -> csv files from which the model can read and sample new values.

data-analysis -> the full data analysis we performed

.idea, ```__pycache__``` -> Pycharm metadata, not specificly necessary (probably not even present in the folder)