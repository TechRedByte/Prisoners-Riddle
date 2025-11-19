import importlib.util
import sys
import random
import os
import pickle
import time
from matplotlib import pyplot as plt

class plots_stats:
    def printWinPercentage():
        results = saving.loadResults()
        total_sims = len(results)
        wins = sum(1 for result in results if result["escaped"])

        winPercentage = (wins / total_sims) * 100
        winStr = f"{winPercentage:.10f}".rstrip('0').rstrip('.')
        print(f"\nWin percentage: {winStr}%")

    def printAvgBoxChecks():
        results = saving.loadResults()
        total_sims = len(results)
        num_prisoners = len(results[0]["prisoners"])
        checksPerPrisoner = {i: 0 for i in range(num_prisoners)}

        for result in results:
            for prisonerId, prisoner_data in enumerate(result["prisoners"]):
                checksPerPrisoner[prisonerId] += len(prisoner_data["checked_boxes"])
        avgChecksPerPrisoner = {prisoner: checks / total_sims for prisoner, checks in checksPerPrisoner.items()}
        
        overallAvg = sum(avgChecksPerPrisoner.values()) / num_prisoners

        plt.bar(avgChecksPerPrisoner.keys(), avgChecksPerPrisoner.values())
        plt.axhline(y=overallAvg, color='r', linestyle='-', label=f'Overall Average: {overallAvg:.2f}')
        plt.xlabel("Prisoner ID")
        plt.ylabel("Average Checked Boxes")
        plt.title("Average Checked Boxes per Prisoner")
        plt.legend(loc='lower left')
        plt.show()

    def printPctFinds():
        results = saving.loadResults()
        total_sims = len(results)
        num_prisoners = len(results[0]["prisoners"])
        findsPerPrisoner = {i: 0 for i in range(num_prisoners)}

        for result in results:
            for prisonerId, prisoner_data in enumerate(result["prisoners"]):
                if prisoner_data["found"]:
                    findsPerPrisoner[prisonerId] += 1
        pctFinds = {prisoner: (finds / total_sims) * 100 for prisoner, finds in findsPerPrisoner.items()}

        avgPctFinds = sum(pctFinds.values()) / num_prisoners

        plt.bar(pctFinds.keys(), pctFinds.values())
        plt.axhline(y=avgPctFinds, color='r', linestyle='-', label=f'Overall Average: {avgPctFinds:.2f}%')
        plt.ylim(0, 100)
        plt.xlabel("Prisoner ID")
        plt.ylabel("Percentage of Finds (%)")
        plt.title("Percentage of Finds per Prisoner")
        plt.legend()
        plt.show()

    def run():
        if not os.path.exists(resultsPath):
            print("No results found. Please run simulations first.")
            return
        
        while True:
            print(f"\nWorking directory: {working_dir}")
            print("\nChoose an option:")
            print("1. Show win percentage")
            print("2. Show average number of checked boxes per prisoner")
            print("3. Show percentage of finds per prisoner")
            print("4. Return to main menu")
            choice = input("Enter your choice: ").strip()
            if choice == '1':
                plots_stats.printWinPercentage()
            elif choice == '2':
                plots_stats.printAvgBoxChecks()
            elif choice == '3':
                plots_stats.printPctFinds()
            elif choice == '4':
                print("Exiting.")
                return
            else:
                print("Invalid choice. Please select a valid option.")

class saving:
    def save(results, checkpoint):
        with open(resultsPath + '.tmp', 'wb') as file:
            pickle.dump(results, file)
        for _ in range(20):
            try:
                os.replace(resultsPath + '.tmp', resultsPath)
                break
            except PermissionError:
                time.sleep(0.01)
                
        with open(checkpointPath + '.tmp', 'wb') as file:
            pickle.dump(checkpoint, file)
        for _ in range(20):
            try:
                os.replace(checkpointPath + '.tmp', checkpointPath)
                break
            except PermissionError:
                time.sleep(0.01)
            
    def loadResults():
        if os.path.exists(resultsPath):
            with open(resultsPath, 'rb') as file:
                results = pickle.load(file)
            return results
        return None
    
    def loadCheckpoint():
        if os.path.exists(checkpointPath):
            with open(checkpointPath, 'rb') as file:
                checkpoint = pickle.load(file)
            return checkpoint
        return None

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
    global working_dir
    while True:
        working_dir = os.path.abspath(input("Enter the working directory: ").strip())
        if os.path.isdir(working_dir):
            return working_dir
        else:
            print(f"Directory {working_dir} does not exist. Please try again.")

def simulatePrisoners():
    results = saving.loadResults()
    checkpoint = saving.loadCheckpoint()
    if checkpoint and results:
        startSim = checkpoint.get("last_simulation") + 1
        rng = random.Random(cfg.get("seed", None))
        rng.setstate(checkpoint.get("rng_state"))
        print(f"Resuming from simulation {startSim}.")
    else:
        startSim = 0
        results = []
        rng = random.Random(cfg.get("seed", None))
        checkpoint = {"last_simulation": -1, "rng_state": rng.getstate()}
        print("Starting new simulations.")

    if startSim >= cfg["num_simulations"]:
        print("All simulations have already been completed.")
        return
    
    for sim in range(startSim, cfg["num_simulations"]):
        prisoners = {i: [0, False] for i in range(cfg["num_prisoners"])}
        boxes = list(prisoners.keys())
        rng.shuffle(boxes)
        results.append({"escaped": None, "prisoners": []})

        for prisonerId in prisoners:
            checkedBoxes = {}
            for _ in range(cfg["total_box_checks"]):
                choice = config.prisonerStrategy(rng, prisonerId, prisoners, cfg["total_box_checks"], checkedBoxes)
                if boxes[choice] == prisonerId:
                    checkedBoxes[choice] = boxes[choice]
                    prisoners[prisonerId] = (checkedBoxes, True)
                    break
                else:
                    checkedBoxes[choice] = boxes[choice]
                    prisoners[prisonerId] = (checkedBoxes, False)

        results[-1]["escaped"] = all(prisoners[prisoner][1] for prisoner in prisoners)
        for prisoner in prisoners:
            results[-1]["prisoners"].append({"found": prisoners[prisoner][1], "checked_boxes": prisoners[prisoner][0]})

    saving.save(results, {"last_simulation": sim, "rng_state": rng.getstate()})
    print("All simulations completed.")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    working_dir = getWorkingDir()
    config = importConfigModule()
    cfg = config.getConfig()
    resultsPath = os.path.join(working_dir, 'results.pkl')
    checkpointPath = os.path.join(working_dir, 'checkpoint.pkl')

    while True:
        print(f"\nWorking directory: {working_dir}")
        print(f"\nChoose an option:")
        print(f"1. Change working directory")
        print(f"2. Run simulations")
        print(f"3. Plot results")
        print(f"4. Exit")
        choice = input("Make a selection (1-4): ").strip()
        if choice == '1':
            getWorkingDir()
        elif choice == '2':
            simulatePrisoners()
        elif choice == '3':
            plots_stats.run()
        elif choice == '4':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please select a valid option.")
