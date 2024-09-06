import json
import sys
import os
from datetime import datetime
data_base = 'todos.txt'
allowed_commands = ['-dl', '-at', '-rt', '-tt', '-in']
# x's    ✗
# checks ✓
def commands():
    print("""
    -dl     display list
    -at     add task
    -rt     remove task
    -ct     toggle task
    -in     init files
    """)

def convert_to_month(month):
    dates = {
        '01': 'Jan',
        '02': 'Feb',
        '03': 'Mar',
        '04': 'Apr',
        '05': 'May',
        '06': 'Jun',
        '07': 'Jul',
        '08': 'Aug',
        '09': 'Sep',
        '10': 'Oct',
        '11': 'Nov',
        '12': 'Dec'
    }
    if month in dates:
        return dates[month]

def organize_dates(curr_date):
    """
    red - due in the next month
    yellow - due after the next month
    green - due > 2 months

    """
    dates = {
        "Jan": '01',
        "Feb": '02',
        "Mar": '03',
        "Apr": '04',
        "May": '05',
        "Jun": '06',
        "Jul": '07',
        "Aug": '08',
        "Sep": '09',
        "Oct": '10',
        "Nov": '11',
        "Dec": '12'
    }
    month = curr_date.find(' ')
    month = curr_date[:month]
    current_date = datetime.now().strftime("%m")
    if month in dates:
        duration = abs(int(dates[month]) - int(current_date))
        if duration >= 3:
            return "\033[92m "
        if duration >=2 :
            return "\033[93m "
        elif duration <= 1:
            return "\033[91m "


def sort_tasks(list_of_tasks):
    # Dictionary to convert month names to numeric values
    dates = {
        "Jan": '01',
        "Feb": '02',
        "Mar": '03',
        "Apr": '04',
        "May": '05',
        "Jun": '06',
        "Jul": '07',
        "Aug": '08',
        "Sep": '09',
        "Oct": '10',
        "Nov": '11',
        "Dec": '12'
    }
    
    # Get the current month in numeric format
    current_month = datetime.now().strftime('%m')
    
    # Helper function to extract and convert date information
    def get_date_key(task):
        description, date_str = task.split('|')
        month, day = date_str.split()
        month_numeric = dates[month]
        # Calculate the difference in months from the current month
        month_diff = (int(month_numeric) - int(current_month)) % 12
        if month_diff < 0:
            month_diff += 12
        # Return a tuple (month_diff, month_numeric, day) for sorting
        return (month_diff, month_numeric, day)
    
    # Sort the tasks based on the extracted date information
    sorted_tasks = sorted(list_of_tasks, key=get_date_key)
    
    return sorted_tasks

def display_list(data_base):
    lists = []
    result = []
    longest_len = 0
    if os.path.isfile(data_base) == False:
        return result
    with open(data_base, 'r') as content:
        for line in content:
            lines = line.strip()
            lists.append(lines)
            task_name_location = lines.find("|")
            task_name = line[:task_name_location]
            due_date = line[task_name_location+1:]
            if len(task_name) > longest_len:
                longest_len = len(task_name) + 5
            sorted_list = sort_tasks(lists)
        for info in sorted_list:
            task_location = info.find("|")
            task = info[:task_location]
            duedate_loc = info.find("/")
            due_date = info[task_location+1:duedate_loc]
            status = info[duedate_loc+1:]
            distance = longest_len - len(task)
            distance = distance * " "
            result.append(f'\033[0m\033[97m[\033[0m{status}\033[97m]\033[0m {task}{distance}{organize_dates(due_date)}{due_date}')
        return result

def init(data_base):
    if os.path.isfile(data_base) == True:
        print("\033[31merror: \033[0mData Base Already Exist, display with '-dl'")
        exit()
    else:
        month = datetime.now().strftime("%m")
        date = datetime.now().strftime("%d")
        month = convert_to_month(month)
        with open(data_base, 'w') as data:
            data.write(f"Write Tasks With '-at'|{month} {date}/✗\n")
        print("\033[32mdone: \033[0mData Base Created!, add tasks with '-at'")

def add_tasks(data_base):
    # Get the current month and day
    month = datetime.now().strftime("%m")
    date = datetime.now().strftime("%d")
    
    # Convert month to its name
    month = convert_to_month(month)
    
    # Get task name and due date from user input
    task_name = input("Please Add A Task Name: ")
    due_date = input(f"Please Add A Due Date ({month} {date}): ")
    
    # Create the task string in the format "task_name|due_date"
    write = f"{task_name}|{due_date}/✗"
    
    # Flag to check if the task already exists
    task_exists = False
    
    # Read from the database file
    with open(data_base, 'r') as db:
        for line in db:
            line = line.strip()
            if line == write:
                task_exists = True
                print("\033[31merror: \033[0mThis Task Already Exists")
                break
    
    # If task does not exist, write it to the file
    if not task_exists:
        with open(data_base, 'a') as db:  # Use 'a' to append to the file
            db.write(f"{write}\n")
        print(f"\033[32mdone: \033[0mAdded '{task_name}' To Database!")


def remove_task(data_base):
    # Store all lines and task names
    tasks = []
    
    # Open the file and read all tasks, displaying them to the user
    with open(data_base, 'r') as db:
        linenum = 0
        for line in db:
            line = line.strip()
            if '|' in line:  # Ensure the line is valid
                line_locate = line.find("|")
                line_task = line[:line_locate]  # Extract the task name
                linenum += 1
                tasks.append(line)  # Store the task line
                print(f"{linenum}) {line_task}")
    
    # If there are no tasks, print a message and exit
    if not tasks:
        print("\033[31merror: \033[0mNo tasks found.")
        return
    
    # Ask the user to select which task to remove
    try:
        task_num = int(input("\nPlease select the number of the task you want to remove: "))
        if task_num < 1 or task_num > len(tasks):
            print("\033[31merror: \033[0mInvalid Selection.")
            return
    except ValueError:
        print("\033[31merror: \033[0mPlease Enter A Valid Number.")
        return
    
    # Remove the selected task
    task_to_remove = tasks[task_num - 1]
    
    # Rewrite the file without the selected task
    with open(data_base, 'w') as db:
        for task in tasks:
            if task != task_to_remove:
                db.write(task + '\n')
    
    print("\033[32mdone: \033[0mRemoved!")
            

def main():
    if len(sys.argv) < 2:
        print("\033[31merror: \033[0mPlease Provide An Action")
        commands()
        exit
    elif sys.argv[1] not in allowed_commands:
        print(f"\033[31merror: \033[91m'{sys.argv[1]}'\033[0m is not recognized as a command")
        commands()
    elif sys.argv[1] in allowed_commands:
        if sys.argv[1] == '-dl':
            lists = display_list(data_base)
            if not lists:
                print("\033[31merror: \033[0mData Base Is Empty, Add Tasks With '-at'")
            else:
                for task in lists:
                    print(task)
        elif sys.argv[1] == '-in':
            init(data_base)
        elif sys.argv[1] == '-at':
            add_tasks(data_base)
        elif sys.argv[1] == '-rt':
            remove_task(data_base)

        

if __name__ == "__main__":
    main()
    
