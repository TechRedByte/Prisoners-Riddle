import random

import config

def simulate_prisoners():
    cfg = config.get_config()

    for sim in range(cfg["num_simulations"]):
        prisoners = {i: False for i in range(cfg["num_prisoners"])}

        boxes = list(prisoners.keys())
        random.shuffle(boxes)

        for prisoner_id in prisoners:
            checked_boxes = {}
            for _ in range(cfg["total_box_checks"]):
                choice = config.prisoner_strategy(prisoner_id, prisoners, cfg["total_box_checks"], checked_boxes)
                if boxes[choice] == prisoner_id:
                    prisoners[prisoner_id] = True
                    break
                else:
                    checked_boxes[choice] = boxes[choice]

simulate_prisoners()