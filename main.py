import importlib.util
import subprocess
import sys
import random
import os

import utils.logging_utils as logging

def importConfigModule(working_dir):
	configPath = os.path.join(working_dir, "config.py")
	spec = importlib.util.spec_from_file_location("config", configPath)
	if spec is None or spec.loader is None:
		raise FileNotFoundError(f"Could not load config.py from {working_dir}")
	config = importlib.util.module_from_spec(spec)
	sys.modules["config"] = config
	spec.loader.exec_module(config)
	return config

def getWorkingDirectory():
	while True:
		working_dir = os.path.abspath(input("Enter the working directory: ").strip())
		if os.path.isdir(working_dir):
			return working_dir
		else:
			print(f"Directory {working_dir} does not exist. Please try again.")

def simulatePrisoners(working_dir=None, config=None):
	cfg = config.getConfig()
	lastSim = logging.loadLogs(working_dir)
	startSim = lastSim + 1
	if startSim >= cfg["num_simulations"]:
		print("All simulations have already been completed.")
		return
	for sim in range(startSim, cfg["num_simulations"]):
		prisoners = {i: False for i in range(cfg["num_prisoners"])}
		boxes = list(prisoners.keys())
		random.shuffle(boxes)

		for prisonerId in prisoners:
			checkedBoxes = {}
			for _ in range(cfg["total_box_checks"]):
				choice = config.prisonerStrategy(prisonerId, prisoners, cfg["total_box_checks"], checkedBoxes)
				if boxes[choice] == prisonerId:
					prisoners[prisonerId] = True
					break
				else:
					checkedBoxes[choice] = boxes[choice]

		logging.logPrisonersResults(sim, prisoners, working_dir)
	print("All simulations completed.")    

if __name__ == "__main__":
	base_dir = os.path.dirname(os.path.abspath(__file__))
	working_dir = getWorkingDirectory()
	while True:
		print(f"\nWorking directory: {working_dir}")
		print(f"\nChoose an option:")
		print(f"1. Change working directory")
		print(f"2. Run simulations")
		print(f"3. Plot results")
		print(f"4. Exit")
		choice = input("Make a selection (1-4): ").strip()
		if choice == '1':
			working_dir = getWorkingDirectory()
		elif choice == '2':
			config = importConfigModule(working_dir)
			simulatePrisoners(working_dir, config)
		elif choice == '3':
			subprocess.run([sys.executable, os.path.join(base_dir, 'utils', 'plots_stats.py'), working_dir])
		elif choice == '4':
			print("Exiting.")
			break
		else:
			print("Invalid choice. Please select a valid option.")
