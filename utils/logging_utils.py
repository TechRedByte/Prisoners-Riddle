import csv
import os

def load_logs(working_dir):
    last_sim = -1
    prisoners_log = os.path.join(working_dir, 'prisoners_results.csv')
    if not os.path.exists(prisoners_log) or os.stat(prisoners_log).st_size == 0:
        with open(prisoners_log, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Simulation', 'PrisonerID', 'FoundBox', 'AllFound'])
        print(f"Created new log file at {prisoners_log}")
    else:
        print(f"Log file {prisoners_log} already exists and is not empty. Appending new results.")
        with open(prisoners_log, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader, None) # Skip header
            for row in reader:
                if row and row[0].isdigit():
                    last_sim = max(last_sim, int(row[0]))
    return last_sim

def log_prisoners_results(sim_id, results, working_dir):
    prisoners_log = os.path.join(working_dir, 'prisoners_results.csv')
    while True:
        try:
            with open(prisoners_log, mode='a', newline='') as file:
                writer = csv.writer(file)
                for prisoner_id, found in results.items():
                    writer.writerow([sim_id, prisoner_id, found])
            break
        except Exception as e:
            print(f"Error logging prisoner results: {e}")
            input("Press Enter to retry...")