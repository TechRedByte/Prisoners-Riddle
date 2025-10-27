import importlib.util
import sys
import random
import os
import csv
from matplotlib import pyplot as plt

class plots_stats:
    def printWinPercentage():
        prisonersLog = os.path.join(working_dir, 'results.csv')
        simResults = {}
        maxSimId = -1
        with open(prisonersLog, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                simId = int(row['Simulation'])
                maxSimId = max(maxSimId, simId)
                found = row['FoundBox'] == 'True'
                if simId not in simResults:
                    simResults[simId] = []
                simResults[simId].append(found)

        if maxSimId == -1:
            print("No simulations found.")
            return

        wins = sum(all(results) for results in simResults.values())
        totalSims = maxSimId + 1

        winPercentage = (wins / totalSims) * 100
        winStr = f"{winPercentage:.10f}".rstrip('0').rstrip('.')
        print(f"\nWin percentage: {winStr}%")

    def printAvgBoxChecks(cfg):
        prisonersLog = os.path.join(working_dir, 'results.csv')
        simResults = {}
        avgChecksPerPrisoner = {}
        with open(prisonersLog, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                simId = int(row['Simulation'])
                prisoner = int(row['PrisonerID'])
                checkedBoxesCount = int(row['CheckedBoxesCount'])
                if simId not in simResults:
                    simResults[simId] = {}
                simResults[simId][prisoner] = checkedBoxesCount

        for prisoner in range(cfg["num_prisoners"]):
            totalChecks = sum(simResults[simId].get(prisoner, 0) for simId in simResults)
            avgChecksPerPrisoner[prisoner] = totalChecks / cfg["num_simulations"]
        overall_avg = sum(avgChecksPerPrisoner.values()) / len(avgChecksPerPrisoner)
        
        plt.bar(avgChecksPerPrisoner.keys(), avgChecksPerPrisoner.values())
        plt.axhline(y=overall_avg, color='r', linestyle='-', label=f'Overall Average: {overall_avg:.2f}')
        plt.xlabel("Prisoner ID")
        plt.ylabel("Average Checked Boxes")
        plt.title("Average Checked Boxes per Prisoner")
        plt.legend()
        plt.show()

    def run(cfg):
        prisonersLog = os.path.join(working_dir, 'results.csv')
        if not os.path.exists(prisonersLog):
            print("No results file found.")
            return
        
        while True:
            print(f"\nWorking directory: {working_dir}")
            print("\nChoose an option:")
            print("1. Show win percentage")
            print("2. Show average checked boxes per prisoner")
            print("3. Exit/Return to main menu")
            choice = input("Enter your choice: ").strip()
            if choice == '1':
                plots_stats.printWinPercentage()
            elif choice == '2':
                plots_stats.printAvgBoxChecks(cfg)
            elif choice == '3':
                print("Exiting.")
                return
            else:
                print("Invalid choice. Please select a valid option.")

class logging:
    def loadLogs():
        lastSim = -1
        prisonersLog = os.path.join(working_dir, 'results.csv')
        if not os.path.exists(prisonersLog) or os.stat(prisonersLog).st_size == 0:
            with open(prisonersLog, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Simulation', 'PrisonerID', 'CheckedBoxesCount', 'FoundBox'])
            print(f"Created new log file at {prisonersLog}")
        else:
            print(f"Log file {prisonersLog} already exists and is not empty. Appending new results.")
            with open(prisonersLog, mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader, None) # Skip header
                for row in reader:
                    if row and row[0].isdigit():
                        lastSim = max(lastSim, int(row[0]))
        return lastSim

    def logPrisonersResults(simId, results):
        prisonersLog = os.path.join(working_dir, 'results.csv')
        while True:
            try:
                with open(prisonersLog, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    for prisonerId, (checkedBoxesCount, found) in results.items():
                        writer.writerow([simId, prisonerId, checkedBoxesCount, found])
                break
            except Exception as e:
                print(f"Error logging prisoner results: {e}")
                input("Press Enter to retry or Ctrl+C to abort...")

def importConfigModule():
    configPath = os.path.join(working_dir, "config.py")
    spec = importlib.util.spec_from_file_location("config", configPath)
    if spec is None or spec.loader is None:
        raise FileNotFoundError(f"Could not load config.py from {working_dir}")
    config = importlib.util.module_from_spec(spec)
    sys.modules["config"] = config
    spec.loader.exec_module(config)
    return config

def getWorkingDir():
    while True:
        working_dir = os.path.abspath(input("Enter the working directory: ").strip())
        if os.path.isdir(working_dir):
            return working_dir
        else:
            print(f"Directory {working_dir} does not exist. Please try again.")

def simulatePrisoners(cfg):
    lastSim = logging.loadLogs()
    startSim = lastSim + 1
    if startSim >= cfg["num_simulations"]:
        print("All simulations have already been completed.")
        return
    for sim in range(startSim, cfg["num_simulations"]):
        prisoners = {i: [0, False] for i in range(cfg["num_prisoners"])}
        boxes = list(prisoners.keys())
        random.shuffle(boxes)

        for prisonerId in prisoners:
            checkedBoxes = {}
            for _ in range(cfg["total_box_checks"]):
                choice = config.prisonerStrategy(prisonerId, prisoners, cfg["total_box_checks"], checkedBoxes)
                if boxes[choice] == prisonerId:
                    prisoners[prisonerId] = (len(checkedBoxes) + 1, True)
                    break
                else:
                    checkedBoxes[choice] = boxes[choice]
                    prisoners[prisonerId] = (len(checkedBoxes), False)

        logging.logPrisonersResults(sim, prisoners)
    print("All simulations completed.")    

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    working_dir = getWorkingDir()
    config = importConfigModule()
    cfg = config.getConfig()
    while True:
        print(f"\nWorking directory: {working_dir}")
        print(f"\nChoose an option:")
        print(f"1. Change working directory")
        print(f"2. Run simulations")
        print(f"3. Plot results")
        print(f"4. Exit")
        choice = input("Make a selection (1-4): ").strip()
        if choice == '1':
            working_dir = getWorkingDir()
        elif choice == '2':
            simulatePrisoners(cfg)
        elif choice == '3':
            plots_stats.run(cfg)
        elif choice == '4':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please select a valid option.")
