import csv
import os

def print_win_percentage(working_dir):
    prisoners_log = os.path.join(working_dir, 'prisoners_results.csv')
    if not os.path.exists(prisoners_log):
        print("No results file found.")
        return

    sim_results = {}
    max_sim_id = -1
    with open(prisoners_log, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            sim_id = int(row['Simulation'])
            max_sim_id = max(max_sim_id, sim_id)
            found = row['FoundBox'] == 'True'
            if sim_id not in sim_results:
                sim_results[sim_id] = []
            sim_results[sim_id].append(found)

    if max_sim_id == -1:
        print("No simulations found.")
        return

    wins = sum(all(results) for results in sim_results.values())
    total_sims = max_sim_id + 1

    win_percentage = (wins / total_sims) * 100
    win_str = f"{win_percentage:.10f}".rstrip('0').rstrip('.')
    print(f"Win percentage: {win_str}%")

print_win_percentage("experiments/test") #testing