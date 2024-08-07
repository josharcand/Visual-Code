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
    # Set field headers for dictionary
    fields = ["type", "done", "due"]
    maint = read_maintenance(csv_file)

    if not maint:
        # initialize with default values if file is newly created or empty
        maint = [{"type": "furnace", "done": "", "due": ""},
                 {"type": "fridge", "done": "", "due": ""},
                 {"type": "detector", "done": "", "due": ""},
                 {"type": "dryer", "done": "", "due": ""}]
        
    # Greet the user
    print("Welcome to the home maintenance reminder")
    
    # User selects which category they want to update
    while True:
        print("Type \"furnace\", \"fridge\", \"detector\", or \"dryer\"")
        print("or type \"view\" to view all due dates or \"exit\" to exit the program")
        # Asks the user what they would like to enter or see
        input1 = input().strip().lower()

        if input1 == "exit":
            break

        service_map = {
            "furnace": (0, furnace),
            "fridge": (1, fridge),
            "detector": (2, detector),
            "dryer": (3, dryer)
        }
        # Gathers info on when the furnace filter was last replaced
        if input1 in service_map:
            index, service_function = service_map[input1]
            update_maintenance(maint, index, service_function)
        elif input1 == "view":
            for item in maint:
                print(f"{item['type']} is due {item['due']}")   
        else:
            print("invalid input, please try again.")         

    write_maintenance(csv_file, maint, fields)

def read_maintenance(csv_file):
    maint = []
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for lines in reader:
                maint.append(lines)
    except FileNotFoundError:
        print(f"File {csv_file} not found. Creating a new one")
    return maint

def write_maintenance(csv_file, maint, fields):
    with open(csv_file, 'w', newline='') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
        csvwriter.writeheader()
        csvwriter.writerows(maint)

def update_maintenance(maint, index, service_function):
    if maint[index]["done"] != "":
        print(f"The {maint[index]['type']} is due on: {maint[index]['due']}")
        print("Have you recently completed the service (yes/no): ")
        input2 = input().strip().lower()
        if input2 == "yes":
            maint[index]["done"], maint[index]["due"] = service_function()
    else:
        maint[index]["done"], maint[index]["due"] = service_function()        

# Function for changing the furnace filter (Every 3 Months)
def furnace():
    # Get the day, month and year when the filter was changed
    print("When did you last change your furnace filter?")
    done, doneDate = getDate()
    due = dueDate(done, 3)
    return doneDate, due

# Function for vaccuuming behind the fridge (Once a year)
def fridge():
    print("When did you last vacuum behind the fridge?")
    done, doneDate = getDate()
    due = dueDate(done, 12)
    return doneDate, due

# Function for changing the batteries in the smoke and CO detectors
def detector():
    print("When did you change the batteries in the smoke and CO detectors?")
    done, doneDate = getDate()
    due = dueDate(done, 12)
    return doneDate, due

# Function for cleaning out the dryer exhaust vent
def dryer():
    print("When did you clean out the dryer vent?")
    done, doneDate = getDate()
    due = dueDate(done, 12)
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