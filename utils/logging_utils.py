import csv
import os

def load_logs(prisoners_log='prisoners_results.csv'):
    if not os.path.exists(prisoners_log) or os.stat(prisoners_log).st_size == 0:
        with open(prisoners_log, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Simulation', 'PrisonerID', 'FoundBox', 'AllFound'])

def log_prisoners_results(sim_id, results, filename='prisoners_results.csv'):
    while True:
        try:
            with open(filename, mode='a', newline='') as file:
                writer=csv.writer(file)
                for prisoner_id, found in results.items():
                    writer.writerow([sim_id, prisoner_id, found])
            break
        except Exception as e:
            print(f"Error logging prisoner results: {e}")
            input("Press Enter to retry...")