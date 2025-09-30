import random

import config
import utils.logging_utils as logging

def simulate_prisoners():
    cfg = config.get_config()
    logging.load_logs()
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

        logging.log_prisoners_results(sim, prisoners)

simulate_prisoners()