import csv
import os

def loadLogs(working_dir):
    lastSim = -1
    prisonersLog = os.path.join(working_dir, 'prisoners_results.csv')
    if not os.path.exists(prisonersLog) or os.stat(prisonersLog).st_size == 0:
        with open(prisonersLog, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Simulation', 'PrisonerID', 'FoundBox', 'AllFound'])
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

def logPrisonersResults(simId, results, working_dir):
    prisonersLog = os.path.join(working_dir, 'prisoners_results.csv')
    while True:
        try:
            with open(prisonersLog, mode='a', newline='') as file:
                writer = csv.writer(file)
                for prisonerId, found in results.items():
                    writer.writerow([simId, prisonerId, found])
            break
        except Exception as e:
            print(f"Error logging prisoner results: {e}")
            input("Press Enter to retry...")