import platform
import sys
import random
import inspect
import os
import pickle
import time
from datetime import datetime
from matplotlib import pyplot as plt

# Terminal Control Constants
class TermCtrl:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    
    # Foreground Colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright Foreground Colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # Background Colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

class utils:
    def formatTimeSeconds(seconds):
        try:
            secs = float(seconds)
        except Exception:
            return str(seconds)
        s = int(secs)
        hh = s // 3600
        mm = (s % 3600) // 60
        ss = s % 60
        return f"{hh:02d}:{mm:02d}:{ss:02d}"

    def formatTimestamp(ts):
        try:
            return datetime.fromtimestamp(float(ts)).strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            return str(ts)
        
    def detectSystem():
        system = platform.system().lower()
        
        if system == 'windows':
            return "windows"
        elif system == 'linux':
            if os.path.exists("/data/data/com.termux"):
                return "android"
            return "linux"
        elif system == 'darwin':
            return "macos"
        else:
            return "unknown"

class Menu_Manager:
    def __init__(self):
        self.title = "Prisoners Riddle Simulator"
        self.message = ""

    def printHeader(self, lines, collums):
        headerStr = f"{TermCtrl.RESET}{TermCtrl.BOLD}{TermCtrl.UNDERLINE}{self.title}{TermCtrl.RESET}" + "\n"*(lines - 1)
        if lines > 0:
            print(headerStr)

    def printBody(self, lines, collums, task):
        logLines = max(0, int(lines // 2))
        secondBodyLines = max(0, lines - logLines)
        if self.message != "":
            logLines -= 1

        # Print log entries
        print("Log:")
        last_logs = log[-logLines:]
        for entry in last_logs:
            print(entry)
        extraLines = max(0,  logLines - len(last_logs))
        if extraLines:
            print("\n" * extraLines, end='')

        # Print message if exists
        if self.message != "":
            print(f"{TermCtrl.BRIGHT_YELLOW}* {self.message}{TermCtrl.RESET}")
            self.message = ""

        simName = os.path.basename(working_dir) if working_dir else "N/A"
        print(f"Current Simulation: {simName}\n")

        # Print second part of body
        if task["type"] == "options":
            if "information" in task:
                for key, value in task["information"].items():
                    print(f"{key}: {value}\n")

            print("Menu Options:")
            for option in [{"key": key, "desc": desc} for key, desc in task["options"].items()]:
                print(f"{option['key']}. {option['desc']}")
            try:
                choice = int(input("Enter your choice: ").strip())
            except ValueError:
                self.message = "Invalid choice: input was not an integer"
                return self.renderMenu(task)
            if choice in task["options"]:
                return choice
            else:
                self.message = f"Invalid choice: {choice}"
                return self.renderMenu(task)

        elif task["type"] == "progress":
            progressLines = max(0, secondBodyLines)
            remainingTime = (task["elapsed_time"] / task["current"]) * (task["total"] - task["current"])
            print(f"Start Time: {utils.formatTimestamp(task['start_time'])}")
            print(f"Current Simulation: {task['current']} / {task['total']}")
            print(f"Elapsed Time: {utils.formatTimeSeconds(task['elapsed_time'])}")
            print(f"Estimated Remaining Time: {utils.formatTimeSeconds(remainingTime)}")

    def renderMenu(self, task):
        collums, lines = os.get_terminal_size()
        headerHeight = 1
        bodyHeight = lines - headerHeight
        os.system('cls')
        self.printHeader(headerHeight, collums)
        return self.printBody(bodyHeight, collums, task)

class Plots_Stats:
    def winPercentage():
        results = Results_Manager.loadResults()
        total_sims = len(results)
        wins = sum(1 for result in results if result["escaped"])

        winPercentage = (wins / total_sims) * 100
        winStr = f"{winPercentage:.10f}".rstrip('0').rstrip('.')
        return winStr

    def printAvgBoxChecks():
        results = Results_Manager.loadResults()
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
        results = Results_Manager.loadResults()
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
        if resultsPath is None or not os.path.exists(resultsPath):
            menu.message = "No results found. Please run simulations first."
            return
        
        while True:
            task = {"type": "options", "information": {"Win Percentage": Plots_Stats.winPercentage()} , "options": {1: "Show average number of checked boxes per prisoner", 2: "Show percentage of finds per prisoner", 3: "Return to main menu"}}
            choice = menu.renderMenu(task)
            if choice == 1:
                Plots_Stats.printAvgBoxChecks()
            elif choice == 2:
                Plots_Stats.printPctFinds()
            elif choice == 3:
                return
            else:
                menu.message = "Invalid choice. Please select a valid option."

class Results_Manager:
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
    results = Results_Manager.loadResults()
    checkpoint = Results_Manager.loadCheckpoint()
    currentTime = time.time()
    startTime = currentTime
    lastPrintTime = currentTime
    if checkpoint and results:
        startSim = checkpoint.get("last_simulation") + 1
        rng = random.Random(config["CONFIG"].get("seed", None))
        rng.setstate(checkpoint.get("rng_state"))
        if startSim >= config["CONFIG"]["num_simulations"]:
            menu.message = "All simulations already completed."
            return
        menu.message = f"Resuming from simulation {startSim}."
    else:
        startSim = 0
        results = []
        rng = random.Random(config["CONFIG"].get("seed", None))
        checkpoint = {"last_simulation": -1, "rng_state": rng.getstate()}

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
        
        # Print progress
        currentTime = time.time()
        if currentTime - lastPrintTime >= 1 or sim == config["CONFIG"]["num_simulations"] - 1:
            lastPrintTime = currentTime
            elapsedTime = currentTime - startTime
            task = {"type": "progress", "current": sim + 1, "total": config["CONFIG"]["num_simulations"], "start_time": startTime, "elapsed_time": elapsedTime}
            menu.renderMenu(task)

    Results_Manager.save(results, {"last_simulation": sim, "rng_state": rng.getstate()})
    print("All simulations completed.")

def main():
    global system
    global base_dir
    global log
    global menu

    global working_dir
    global resultsPath
    global checkpointPath
    global configPath
    global prisonerStrategy
    global config
    working_dir = None
    resultsPath = None
    checkpointPath = None
    configPath = None
    prisonerStrategy = None
    config = None

    log = []
    log.append("Initializing...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    system = utils.detectSystem()
    menu = Menu_Manager()
    while True:
        task = {"type": "options", "options": {1: "Create New Simulation", 2: "Load Existing Simulation", 3: "Run Simulations", 4: "View Plots/Stats", 5: "Exit"}}
        choice = menu.renderMenu(task)
        if choice == 1:
            Results_Manager.createNewSimulation()
        elif choice == 2:
            Results_Manager.loadSimulation()
        elif choice == 3:
            simulatePrisoners()
        elif choice == 4:
            Plots_Stats.run()
        elif choice == 5:
            sys.exit(0)

if __name__ == "__main__":
    main()