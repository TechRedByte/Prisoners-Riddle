'''
This is a sample configuration file. You can modify the parameters and strategy as needed.
Copy this file as config.py to each of your working directories.
'''

CONFIG = { # Settings for the simulation
    "num_prisoners": 100,
    "total_box_checks": 50,
    "num_simulations": 10000,
    "seed": None  # Set to an integer for reproducible results or None for random seed
}

def getConfig():
    return CONFIG

def prisonerStrategy(random, prisoner_id, prisoners, total_checks, checked_boxes): # Set strategy here
    # Use random.* for any randomness needed

    # Example: Loop strategy
    if checked_boxes:
        return(next(reversed(checked_boxes.values())))
    else:
        return prisoner_id