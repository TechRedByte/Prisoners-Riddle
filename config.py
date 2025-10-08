'''
This is a sample configuration file. You can modify the parameters and strategy as needed.
Copy this file as config.py to each of your working directory.
'''

import random

CONFIG = {
    # Settings for the simulation
    "num_prisoners": 100,
    "total_box_checks": 50,
    "num_simulations": 10000
}

def getConfig():
    return CONFIG

def prisonerStrategy(prisoner_id, prisoners, total_checks, checked_boxes):
    # Set strategy here
    # Example: Random choice strategy
    available_boxes = [i for i in range(len(prisoners)) if i not in checked_boxes]
    return random.choice(available_boxes)