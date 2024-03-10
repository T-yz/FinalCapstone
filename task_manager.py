# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


def reg_user():
        # - Request input of a new username
    username_validity = False
    while not username_validity:
        new_username = input("New Username: ")
        if new_username in username_password.keys():
            print("Username already in use, Please use another ")
            continue
        else:
            username_validity = True

        # - Request input of a new password
    new_password = input("New Password: ")

        # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

        # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password

        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))
    else:
        print("Passwords do no match")


def add_task():
    '''Allow a user to add a new task to task.txt file
    Prompt a user for the following: 
    - A username of the person whom the task is assigned to,
    - A title of a task,
    - A description of the task and 
    - the due date of the task.'''
    username_validity = False
    while not username_validity:
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        else:
            username_validity = True
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")


def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling) 
    '''
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)


def view_mine():
    '''Allows the user to view and manage their tasks, including marking tasks as complete and editing tasks.'''
    user_tasks = [t for t in task_list if t['username'] == curr_user]
    for i, t in enumerate(user_tasks, start=1):
        disp_str = f"Task ID {i}:\n"
        disp_str += f"  Title: {t['title']}\n"
        disp_str += f"  Assigned to: {t['username']}\n"
        disp_str += f"  Date Assigned: {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"  Due Date: {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"  Description: {t['description']}\n"
        print(disp_str)

    selected_task = input("Enter the task number to manage or '-1' to return to the main menu: ")
    if selected_task == '-1':
        return  # Return to main menu
    else:
        # Convert selected_task to number and -1 to match the list index
        selected_index = int(selected_task) - 1
        if 0 <= selected_index < len(user_tasks):
            selected_task_details = user_tasks[selected_index]
            print("Selected Task:")
            disp_str = f"  Title: {selected_task_details['title']}\n"
            disp_str += f"  Assigned to: {selected_task_details['username']}\n"
            disp_str += f"  Date Assigned: {selected_task_details['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"  Due Date: {selected_task_details['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"  Description: {selected_task_details['description']}\n"
            print(disp_str)

            action = input("Select an action for this task:\n1. Mark as complete\n2. Edit task\n3. Return to main menu\nEnter your choice: ")
            if action == '1':
                # Mark the task as complete
                user_tasks[selected_index]['completed'] = True
                print("Task marked as complete.")
            elif action == '2':
                # Edit the task
                print("Editing Task:")
                print("Enter new details for the task:")
                selected_task_details['title'] = input("Title: ")
                selected_task_details['description'] = input("Description: ")
                while True:
                    try:
                        task_due_date = input("Due date of task (YYYY-MM-DD): ")
                        due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                        selected_task_details['due_date'] = due_date_time
                        break

                    except ValueError:
                        print("Invalid datetime format. Please use the format specified")

                print("Task edited successfully.")
            elif action == '3':
                return
            else:
                print("Invalid choice. Returning to main menu.")
        else:
            print("Invalid task number")

def generate_report():
    # All of the vars for task_overview
    total_task = len(task_list)
    completed_task = sum(1 for task in task_list if task["completed"])
    incompleted_task = total_task - completed_task
    incompleted_task_perc = (incompleted_task / total_task) * 100
    overdue_task =  sum(1 for task in task_list if task["due_date"] > datetime.today())
    overdue_task_perc = (overdue_task /total_task) * 100

    total_users = len(username_password.keys())

    with open("task_overview.txt", "w") as default_task_file:
        default_task_file.write(f"Task overview \n")
        default_task_file.write(f"Total Tasks: {total_task} \n")
        default_task_file.write(f"Completed Tasks: {completed_task} \n")
        default_task_file.write(f"Incompleted Tasks: {incompleted_task} \n")
        default_task_file.write(f"Percentage of Incomplete Tasks: {incompleted_task_perc}% \n")
        default_task_file.write(f"Percentage of Overdue Tasks: {overdue_task_perc}% \n")
    print("Report generated and saved to 'task_overview.txt'.")


    with open("user_overview.txt", "w") as default_user_file:
        default_user_file.write(f"User Overview \n")
        default_user_file.write(f"Total Users: {total_users} \n")
        default_user_file.write(f"Total Tasks: {total_task} \n")
        # all vars are listed here aswell as the write to file

        for users in username_password.keys():
            user_tasks = sum(1 for task in task_list if task["username"]== users)
            completed_user_tasks = sum(1 for task in task_list if task["completed"] and task["username"] == users)
            user_tasks_perc_assigned = (completed_user_tasks/total_task) * 100
            user_tasks_perc_completed = (completed_user_tasks/user_tasks) * 100
            user_tasks_incomplete = user_tasks - completed_user_tasks
            user_tasks_perc_incomplete = (user_tasks_incomplete / user_tasks) * 100
            user_tasks_overdue = sum(1 for task in task_list if not task["completed"] and task["username"] == users and task["due_date"] > datetime.today())
            user_tasks_overdue_perc = (user_tasks_overdue / user_tasks) * 100

            default_user_file.write(f" {users}'s Tasks: {user_tasks} \n")
            default_user_file.write(f"{users} has {user_tasks_perc_assigned}% of the total task workload \n")
            default_user_file.write(f"{users} has completed {user_tasks_perc_completed}% of their assigned work \n")
            default_user_file.write(f"{users} needs to complete {user_tasks_perc_incomplete}% of their assigned work \n")
            default_user_file.write(f"{users} is overdue on {user_tasks_overdue_perc}% of their assigned work \n")
        print("Report generated and saved to 'user_overview.txt'.")




while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate report
ds - Display statistics
e - Exit
: ''').lower()
    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()
    
    elif menu == 'gr':
        generate_report()

    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
        and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")   

        generate_report()


    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")