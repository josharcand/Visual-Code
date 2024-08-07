import csv
import os
from datetime import datetime

def get_path(filename):
    # Get the path to a persistent directory for user-specific data
    home = os.path.expanduser("~")
    app_data_dir = os.path.join(home, "Documents", "Computronix", "Visual Code", "Project")
    if not os.path.exists(app_data_dir):
        os.makedirs(app_data_dir)
    return os.path.join(app_data_dir, filename)

def main():
    # Get the path for the CSV file
    csv_file = get_path("home.csv")
    # Initialize input1
    input1 = ""
    # Set field headers for dictionary
    fields = ["type", "done", "due"]

    # Open the CSV file with maintenance info and creates a dictionary
    maint = []
    try:
        with open(csv_file, mode ='r')as file:
            reader = csv.DictReader(file)
            for lines in reader:
                maint.append(lines)
    except FileNotFoundError:
        print(f"File {csv_file} not found. Creating a new one")
    
    if not maint:
        # Initialize with default values if file is newly created or empty
        maint = [{"type": "furnace", "done": "", "due": ""},
                 {"type": "fridge", "done": "", "due": ""},
                 {"type": "detector", "done": "", "due": ""},
                 {"type": "dryer", "done": "", "due": ""}]
        
    # Greet the user
    print("Welcome to the home maintenance reminder")
    print("What item would you like to enter?")
    
    # User selects which category they want to update
    while True:
        print("Type \"furnace\", \"fridge\", \"detector\", or \"dryer\"")
        print("or type \"view\" to view all due dates or \"exit\" to save and exit the program")
        # Asks the user what they would like to enter or see
        # Plus error handling for uppercase letters or extra characters
        input1 = input().strip().lower()

        if input1 == "exit":
            break

        # Create a service map to the different functions
        service_map = {
            "furnace": (0, furnace),
            "fridge": (1, fridge),
            "detector": (2, detector),
            "dryer": (3, dryer)
        }

        # Gathers info depending on user input
        if input1 in service_map:
            index, service_function = service_map[input1]
            update_maintenance(maint, index, service_function)
        # Prints everything and its due date
        elif input1 == "view":
            for item in maint:
                print(item["type"] + " is due " + item["due"])
        else:
            print("Invalid input, please try again.")

    # Write all the inputted data back to the file
    try:
        with open(csv_file, 'w', newline='') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
            csvwriter.writeheader()
            csvwriter.writerows(maint)
        print(f"Data has been updated successfully to {csv_file}")
    except IOError as e:
        print(f"Error writing to file {csv_file}: {e}")

# Function to update the maintenance record for the specified item
def update_maintenance(maint, index, service_function):
    if maint[index]["done"] != "":
        print("The " + maint[index]["type"] + " is due on " + maint[index]["due"])
        while True:
            print("Have you recently completed the service (yes/no): ")
            input2 = input().strip().lower()
            if input2 == "yes":
                maint[index]["done"], maint[index]["due"] = service_function()
                break
            elif input2 == "no":
                print("Service for " + maint[index]["type"] + " is still pending.")
                break
            else:
                print("Invalid input. Please type \"yes\" or \"no\".")
    else:
        maint[index]["done"], maint[index]["due"] = service_function()

# Function for changing the furnace filter (Every 3 Months)
def furnace():
    # Get the day, month and year when the filter was changed
    print("When did you last change your furnace filter?")
    done, doneDate = getDate()
    due = dueDate(done, 3)
    print("The furnace filter is due to be changed on: " + due)
    return doneDate, due

# Function for vaccuuming behind the fridge (Once a year)
def fridge():
    print("When did you last vacuum behind the fridge?")
    done, doneDate = getDate()
    due = dueDate(done, 12)
    print("The fridge is due to be vacuumed on: " + due)
    return doneDate, due

# Function for changing the batteries in the smoke and CO detectors
def detector():
    print("When did you change the batteries in the smoke and CO detectors?")
    done, doneDate = getDate()
    due = dueDate(done, 12)
    print("The smoke and CO detector batteries are due to be changed on: " + due)
    return doneDate, due

# Function for cleaning out the dryer exhaust vent
def dryer():
    print("When did you clean out the dryer vent?")
    done, doneDate = getDate()
    due = dueDate(done, 12)
    print("The dryer vent is due to be cleaned on: " + due)
    return doneDate, due

# Gets the date input from the user
def getDate():
    date = input("Enter the date you completed the service: (YYYY/MM/DD)")
    try:
        done = datetime.strptime(date, "%Y/%m/%d")
    # If date is entered in the wrong format or with letters they will be prompted to try again
    except ValueError:
        print("Incorrect format. Please try again")
        return getDate()
    # Format date to be stored and outputted
    doneDate = done.strftime("%Y/%m/%d")
    # return the date in datetime format and as a string
    return done, doneDate

# Calculate the due date for services
def dueDate(done, months):
    # Adds the number of months to the date that was entered
    # // is taking the remainer when divided by 12
    # % is taking the modulus when divided by 12...If there was a remainder it would be added to the year.
    due = datetime(done.year + (done.month + months - 1) // 12, (done.month + months - 1) % 12 + 1, done.day)
    due = due.strftime("%Y/%m/%d")
    return due

if __name__ == "__main__":
    main()