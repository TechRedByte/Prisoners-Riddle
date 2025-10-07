import importlib.util
import sys
import random
import os

import utils.logging_utils as logging

def import_config_module(working_dir):
	config_path = os.path.join(working_dir, "config.py")
	spec = importlib.util.spec_from_file_location("config", config_path)
	if spec is None or spec.loader is None:
		raise FileNotFoundError(f"Could not load config.py from {working_dir}")
	config = importlib.util.module_from_spec(spec)
	sys.modules["config"] = config
	spec.loader.exec_module(config)
	return config

def get_working_directory():
	while True:
		WORKING_DIR = os.path.abspath(input("Enter the working directory: ").strip())
		if os.path.isdir(WORKING_DIR):
			return WORKING_DIR
		else:
			print(f"Directory {WORKING_DIR} does not exist. Please try again.")

def simulate_prisoners(WORKING_DIR=None, config=None):
	cfg = config.get_config()
	last_sim = logging.load_logs(WORKING_DIR)
	start_sim = last_sim + 1
	if start_sim >= cfg["num_simulations"]:
		print("All simulations have already been completed.")
		return
	for sim in range(start_sim, cfg["num_simulations"]):
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

		logging.log_prisoners_results(sim, prisoners, WORKING_DIR)
	print("All simulations completed.")    

if __name__ == "__main__":
	WORKING_DIR = get_working_directory()
	config = import_config_module(WORKING_DIR)
	simulate_prisoners(WORKING_DIR, config)
