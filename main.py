import importlib.util
import sys
import random
import inspect
import os
import pickle
import time
from matplotlib import pyplot as plt

class plots_stats:
    def printWinPercentage():
        results = results_manager.loadResults()
        total_sims = len(results)
        wins = sum(1 for result in results if result["escaped"])

        winPercentage = (wins / total_sims) * 100
        winStr = f"{winPercentage:.10f}".rstrip('0').rstrip('.')
        print(f"\nWin percentage: {winStr}%")

    def printAvgBoxChecks():
        results = results_manager.loadResults()
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
        results = results_manager.loadResults()
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

class results_manager:
    def save(results, checkpoint):
        with open(resultsPath + '.tmp', 'wb') as file:
            pickle.dump(results, file)
        for _ in range(20):
            try:
                os.replace(resultsPath + '.tmp', resultsPath)
                break
            except PermissionError:
                time.sleep(0.01)
        else:
            raise PermissionError("Could not save results due to persistent PermissionError.")

        with open(checkpointPath + '.tmp', 'wb') as file:
            pickle.dump(checkpoint, file)
        for _ in range(20):
            try:
                os.replace(checkpointPath + '.tmp', checkpointPath)
                break
            except PermissionError:
                time.sleep(0.01)
        else:
            raise PermissionError("Could not save checkpoint due to persistent PermissionError.")
            
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
    
    def createNewSimulation():
        global working_dir
        global resultsPath
        global checkpointPath
        global configPath
        global prisonerStrategy
        global config
        while True:
            simID = input("Enter new simulation ID: ").strip()
            working_dir = os.path.join(base_dir, "results", simID)
            resultsPath = os.path.join(working_dir, "results.pkl")
            checkpointPath = os.path.join(working_dir, "checkpoint.pkl")
            configPath = os.path.join(working_dir, "config.pkl")
            if not os.path.exists(working_dir):
                os.makedirs(working_dir)
                break
            print("Simulation ID already exists. Please choose a different ID.")
        import config as baseConfig
        prisonerStrategy = baseConfig.prisonerStrategy
        prisonerStrategy_string = inspect.getsource(baseConfig.prisonerStrategy)
        config = {"CONFIG": baseConfig.getConfig(), "prisonerStrategy": prisonerStrategy_string}
        with open(configPath, 'wb') as file:
            pickle.dump(config, file)

    def loadSimulation():
        global working_dir
        global resultsPath
        global checkpointPath
        global configPath
        global prisonerStrategy
        global config
        while True:
            simID = input("Enter simulation ID: ").strip()
            working_dir = os.path.join(base_dir, "results", simID)
            resultsPath = os.path.join(working_dir, "results.pkl")
            checkpointPath = os.path.join(working_dir, "checkpoint.pkl")
            configPath = os.path.join(working_dir, "config.pkl")
            if os.path.exists(configPath):
                break
            print("Invalid simulation ID. Please try again.")
        with open(configPath, 'rb') as file:
            config = pickle.load(file)
        namespace = {}
        exec(config["prisonerStrategy"], namespace)
        prisonerStrategy = namespace["prisonerStrategy"]

def simulatePrisoners():
    results = results_manager.loadResults()
    checkpoint = results_manager.loadCheckpoint()
    if checkpoint and results:
        startSim = checkpoint.get("last_simulation") + 1
        rng = random.Random(config["CONFIG"].get("seed", None))
        rng.setstate(checkpoint.get("rng_state"))
        print(f"Resuming from simulation {startSim}.")
    else:
        startSim = 0
        results = []
        rng = random.Random(config["CONFIG"].get("seed", None))
        checkpoint = {"last_simulation": -1, "rng_state": rng.getstate()}
        print("Starting new simulations.")

    if startSim >= config["CONFIG"]["num_simulations"]:
        print("All simulations have already been completed.")
        return
    
    for sim in range(startSim, config["CONFIG"]["num_simulations"]):
        prisoners = {i: [0, False] for i in range(config["CONFIG"]["num_prisoners"])}
        boxes = list(prisoners.keys())
        rng.shuffle(boxes)
        results.append({"escaped": None, "prisoners": []})

        for prisonerId in prisoners:
            checkedBoxes = {}
            for _ in range(config["CONFIG"]["total_box_checks"]):
                choice = prisonerStrategy(rng, prisonerId, prisoners, config["CONFIG"]["total_box_checks"], checkedBoxes)
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

    results_manager.save(results, {"last_simulation": sim, "rng_state": rng.getstate()})
    print("All simulations completed.")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    while True:
        print(f"\nChoose an option:")
        print(f"1. Create new simulation")
        print(f"2. Load simulation")
        print(f"3. Simulate prisoners (load or create simulation first)")
        print(f"4. Show plots and statistics (load or create simulation first)")
        print(f"5. Exit")
        choice = input("Make a selection (1-5): ").strip()
        if choice == '1':
            results_manager.createNewSimulation()
        elif choice == '2':
            results_manager.loadSimulation()
        elif choice == '3':
            if config is None:
                print("\nPlease create or load a simulation first.")
            else:
                simulatePrisoners()
        elif choice == '4':
            if config is None:
                print("\nPlease create or load a simulation first.")
            else:
                plots_stats.run()
        elif choice == '5':
            print("Exiting.")
            sys.exit(0)
        else:
            print("Invalid choice. Please select a valid option.")
