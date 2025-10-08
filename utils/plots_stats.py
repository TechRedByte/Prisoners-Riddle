import csv
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import main

def printWinPercentage(working_dir):
    prisonersLog = os.path.join(working_dir, 'prisoners_results.csv')
    if not os.path.exists(prisonersLog):
        print("No results file found.")
        return

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
    print(f"Win percentage: {winStr}%")

if __name__ == "__main__":
    working_dir = sys.argv[1]
    if not os.path.isdir(working_dir):
        print(f"Directory {working_dir} does not exist.")
        working_dir = main.getWorkingDirectory()
    while True:
        print(f"\nWorking directory: {working_dir}")
        print("\nChoose an option:")
        print("1. Change working directory")
        print("2. Show win percentage")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            working_dir = main.getWorkingDirectory()
        elif choice == '2':
            printWinPercentage(working_dir)
        elif choice == '3':
            print("Exiting to main menu.")
            break
        else:
            print("Invalid choice. Please select a valid option.")