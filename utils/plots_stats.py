import csv
import sys
import os

def printWinPercentage(working_dir):
    prisonersLog = os.path.join(working_dir, 'results.csv')
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
        print("Please choose a valid directory with a results.csv file.")
        print("Returning to main menu.")
        sys.exit(1)
    while True:
        print(f"\nWorking directory: {working_dir}")
        print("\nChoose an option:")
        print("1. Show win percentage")
        print("2. Back to main menu")
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            printWinPercentage(working_dir)
        elif choice == '2':
            print("Returning to main menu.")
            sys.exit(0)
        else:
            print("Invalid choice. Please select a valid option.")