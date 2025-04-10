# SE T17 - Compulsory Task 1 - Capstone project
# Student: Marius Moldovan
# Date: 04.06.2023

# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

# Import libraries
import os
from datetime import datetime, date

# Define the date format
DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create global variables
# A list that contains all the tasks
task_list = []
# A list that contains all the usernames and passwords
username_password = {}
# A variable to be used to identify if a user is logged id, that is initially set to False
logged_in = False
# A variable that contains the username for the current user that is logged in
curr_user = ""

# The function initialization(), no parameters defined
# initializes all the required files and variables in order for the program to run
def initialization():
    # Define the global variables that will be used
    global task_list, username_password, logged_in, curr_user
    # 1. TASKS
    # Create tasks.txt file if it doesn't exist
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            pass
    
    # Get the data from tasks.txt and save it in task_data list each line as new item removing the end of line char
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    # Parse all the data and create dictionary entries for each line
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
        # Add each dictionary as an item to main list of tasks(task_list)
        task_list.append(curr_t)
    
    # 2. USER
    # Login Section
    # This code reads usernames and password from the user.txt file to allow a user to login.
    # If no user.txt file, write one with a default password
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")
    # Read in user_data
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")
    # Convert to a dictionary
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password

    # 3. LOGGED IN
    # Check if an user is logged in, if not ask for credentials
    print("Hello! Welcome to the Tasks Management System(TMS).")
    while not logged_in:
        print("Please enter your credentials in the Login form")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        if curr_user not in username_password.keys():
            print("Error: The user does not exist!")
            continue
        elif username_password[curr_user] != curr_pass:
            print("Error: the password is wrong!")
            continue
        else:
            print("Info: Login was successful!")
            logged_in = True

# The function reg_user(), no parameters defined
# ads a new user to the user.txt file if the username doesn't exist
def reg_user():
        # Declare username_password as global variable
        global username_password
        print("Info: Add a new user to the system")
        while True:
            # Request input of a new username
            new_username = input("New username: ")
            while True:
                # Check if the username already exists
                if (new_username in username_password):
                    new_username = input("Error: The username that you choosen already exists!\nNew username: ")
                    continue
                elif (len(new_username) < 5):
                    new_username = input("Error: The length of the username should be at least 5 characters!\nNew username: ")
                else:
                    break

            # Request input of a new password
            new_password = input("New password: ")
            while True:
                # Check if the username already exists
                if (len(new_password) < 5):
                    new_password = input("Error: The length of the password should be at least 5 characters!\nNew password: ")
                else:
                    break
            # Request input of password confirmation.
            confirm_password = input("Confirm password: ")
            # Check if the new password and confirmed password are the same.
            if new_password == confirm_password:
                # - If they are the same, add them to the user.txt file,
                print("Notice: New user added")
                username_password[new_username] = new_password
                # Update the user.txt file to contain the new user
                with open("user.txt", "w") as out_file:
                    user_data = []
                    for k in username_password:
                        user_data.append(f"{k};{username_password[k]}")
                    out_file.write("\n".join(user_data))
                break

            # - Otherwise you present a relevant error message.
            else:
                print("Error: The passwords do no match!")

# The function add_tasks(), no parameters defined
# ads a new task to the system
def add_task():
    # Declare the global variables that will be used
    global task_list, username_password
    # Allow a user to add a new task to task.txt file
    # Prompt a user for the following: 
    # - A username of the person whom the task is assigned to,
    # - A title of a task,
    # - A description of the task and 
    # - the due date of the task.
    print("Notice: Add new task")
    # Retrieve the username for the task allocation
    # if it doesn't exists then ask the user to try again
    while True:
        task_username = input("Name of the person assigned to the task(username): ")
        if task_username not in username_password.keys():
            print("Error: The username does not exist. Please enter a valid username!")
        else:
            break
    # Ask the user to input a title that is at least 5 characters
    while True:
        task_title = input("Title of the Task: ")
        if len(task_title) < 5:
            print("Error: The task title should be at least 5 characters!")
        else:
            break
    # Ask the user to input a description that is at least 5 characters
    while True:
        task_description = input("Description of the Task: ")
        if len(task_description) < 5:
            print("Error: The task description should be at least 5 characters!")
        else:
            break
    # Ask the user to input the due date in a certain format an not in the past
    # create first a today variable with today's date
    today = datetime.strptime(str(date.today()), DATETIME_STRING_FORMAT)
    while True:
        try:
            task_due_date = input("Due date of the task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            if due_date_time < today:
                print("Error: Please enter a date that is not in the past!")
            else:
                break
        except ValueError:
            print("Error: Invalid datetime format. Please use this format YYYY-MM-DD for the date!")

    # Then get the current date.
    curr_date = date.today()
    # Add the data to the file task.txt and
    # Include 'No' to indicate if the task is complete.
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
    print("Notice: The task was successfully added.")

# The function view_all(), no parameters defined
# displays all the tasks that were added in the TMS
def view_all():
    # Reads the task from task.txt file and prints to the console in the 
    # format of Output 2 presented in the task pdf (i.e. includes spacing
    # and labelling)
    print("Notice: Printing all the tasks")
    i = 1
    for t in task_list:
        disp_str = f"Task {i}: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        disp_str += f"Task Completed: {t['completed']}\n"
        print(disp_str)
        i += 1

# The function view_mine(), no parameters defined
# displays the tasks and the options available for the tasks allocated to the logged in user
def view_mine():
    # Define the global variables that will be used
    global task_list, curr_user
    # Reads the task from task.txt file and prints to the console in the 
    # format of Output 2 presented in the task pdf (i.e. includes spacing
    # and labelling)
    print("Notice: These are the tasks that are currently allocated to you")
    i = 1
    for t in task_list:
        if t['username'] == curr_user:
            disp_str =  f"Task number {i}: {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)} | "
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: {t['description']}\n"
            completed = "Yes" if t['completed'] else "No"
            disp_str += f"Task Completed: {completed}\n"
            print(disp_str)
            i += 1
    # If no tasks have been found(i will not change) print this to the screen
    if i == 1:
        print("Notice: There are no tasks allocated to you in the task list!")
    else: 
        while True:
            # ask the user to input the task number he would like to modify of -1 to exit this submenu
            while True:
                try:
                    vm_option = int(input("Please enter the task number you want to finish or edit or enter -1 to return to the main menu! "))
                    break
                except ValueError:
                    print("Error: Please enter a number!")
            if vm_option == -1:
                break
            else:
                # Print the task that has been selected if the task exists
                while True:
                    print(f"Notice: You have selected task number {vm_option}.")
                    selected_task = {}
                    i = 1
                    for t in task_list:
                        if t['username'] == curr_user:
                            if i == vm_option:
                                disp_str =  f"Task number {vm_option}: {t['title']}\n"
                                disp_str += f"Assigned to: \t {t['username']}\n"
                                disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                                disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                                disp_str += f"Task Description: \n {t['description']}\n"
                                completed = "Yes" if t['completed'] else "No"
                                disp_str += f"Task Completed: {completed}\n"
                                print(disp_str)
                                # Create a copy of the dictionary for this task that will be used later on
                                selected_task = t
                            i += 1
                    # Return an error message if the task that the user selected doens't exist
                    if (i == 1):
                        print("Error: The selected task doesn't exist!")
                        break    
                    # Return an error message if the task has been marked as complete
                    if selected_task["completed"]:
                        print("Error: This task can't be edited as it has been marked as complete!")
                        break
                    else:
                        # Call the edit_task() function to allow the user to modifify the class
                        # Pass a copy of the task that the user selected(dictionary) and the number of the task
                        edit_task(selected_task, vm_option)
                        break
                break

# The function edit_task(), 2 parameters required, a dictionary named task and an int named taskNo
# allows the user to mark the task complete, to change the username of the task or the due date
def edit_task(task, taskNo):
    # Define the global variables that will be used
    global task_list, curr_user, username_password
    while True:
        # Ask the user to choose what he wants to edit
        task_option = input("Please select one from the 3 options available.\nc - Mark as complete\nu - Edit username\nd - Edit due date\n")
        # If users selects mark as complete ask the user to confirm his choice
        if (task_option.lower() == "c"):
            print(f"Please confirm that you want to mark task no {taskNo} as complete! y/n")
            while True:
                complete_option = input("")
                # If the user inputs y it means that he confirmed
                # update the completed field in the dictionary for the task
                # update the tasks.txt file with this change
                if complete_option.lower() == "y":
                    for task_dict in task_list:
                        if task_dict.get("title") == task["title"]:
                            task_dict.update({"completed": True})
                            update_tasks_file(taskNo)
                    break
                # If the user inputs n display a message
                elif complete_option.lower() == "n":
                    print("Notice: You selected No, the task has not been modifed")
                    break
                # For anything else continue to run the loop until
                # the user selects y or n
                else:
                    continue
            break
        # If the user wants to change the username ask for the new username
        elif (task_option.lower() == "u"):
            while True:
                print("Please enter the new username that this task will be allocated to:")
                new_username = input()
                # Check if the username exists
                if (new_username in username_password):
                    for task_dict in task_list:
                        if task_dict.get("title") == task["title"]:
                            # Update the username field in the dictionary for the task
                            # update the tasks.txt file with this change
                            task_dict.update({"username": new_username})
                            update_tasks_file(taskNo)
                            print("The task has been allocated to " + new_username + "!")
                    break
                else:
                    # Else print an error message that the username doesn't exists
                    print("Error: This username doesn't exist!")
            break
        # Else if the user wants to change the due date
        elif (task_option.lower() == "d"):
            # Get the new date and generate the today's date
            print("Please enter the new due date for this task")
            today = datetime.strptime(str(date.today()), DATETIME_STRING_FORMAT)
            while True:
                try:
                    # The user inputs the new date and this is formated as definde by DATETIME_STRING_FORMAT
                    new_task_due_date = input("Due date of task (YYYY-MM-DD): ")
                    due_date_time = datetime.strptime(new_task_due_date, DATETIME_STRING_FORMAT)
                    # If the due date is in the past display an error message
                    if due_date_time < today:
                        print("Error: Please enter a date that is not in the past!")
                    else:
                        break
                # If the date that the user inputs doesn't match the format display an error message
                except ValueError:
                    print("Error: Invalid datetime format. Please use the format specified")
            # Update the new due date in the dictionary
            # Update the tasks.txt file
            for task_dict in task_list:
                    if task_dict.get("title") == task["title"]:
                        task_dict.update({"due_date": due_date_time})
                        update_tasks_file(taskNo)
                        print("Notice: The task has been updated with the new date! - " + str(due_date_time))
            break
        else:
            # Print an error message if the option doesn't exists
            print("Error: The option that you have selected doesn't exist!")

# The function update_tasks_file(), 1 parameter required, an int named taskNo
# updates the tasks.txt file whenever the task_list has been altered in order to save the changes
def update_tasks_file(taskNo):
    # Define the global variables that will be used
    global task_list
    # Get the data from tasks.txt and save it in task_data list each line as new item removing the end of line char
    with open("tasks.txt", 'w') as task_file:
        i=0
        for dict in task_list:
            completed = "Yes" if dict["completed"] == True else "No"
            task_file.write(dict["username"] + ";" + dict["title"] + ";" + dict["description"] + ";" + str(dict["due_date"].strftime(DATETIME_STRING_FORMAT)) + ";" + str(dict["assigned_date"].strftime(DATETIME_STRING_FORMAT)) + ";" + completed)
            
            if i == len(task_list):
                continue
            else:
                task_file.write("\n")
    # Print confirmation email that the task and the tasks.txt has been updated
    print(f"Notice: The task no {taskNo} has been updated!")
    print("Notice: The file tasks.txt has been updated!")

# The function generate_reports(), no parameters defined
# generates reports and saves them to the task_overview.txt and user_overview.txt files
def generate_reports():
    # Print a header and generate today's date to be used in the report
    print("Notice: Generating reports ")
    today = datetime.strptime(str(date.today()), DATETIME_STRING_FORMAT)
    # 1. Compute the data and generate task_overview.txt
    # declare the variables needed and initialize them
    total_tasks = len(task_list)
    total_tasks_uncompleted = 0
    total_tasks_overdue = 0
    # count all the tasks that are uncompleted and overdue
    for task_dict in task_list:
        if task_dict["completed"] == False:
            total_tasks_uncompleted += 1
        if task_dict["completed"] == False and task_dict["due_date"] < today:
            total_tasks_overdue += 1
    # Calculate the percentage for uncompleted and overdue
    uncompleted_percentage = round(total_tasks_uncompleted*100/total_tasks)
    overdue_percentage = round(total_tasks_overdue*100/total_tasks)
    # Write the task_overview.txt in a certain format containing the statistics
    with open("task_overview.txt", 'w') as task_overview_file:
        task_overview_file.write("This Report that is saved in task_overview.txt has been generated on " + str(date.today()) + ".\n")
        task_overview_file.write("The total number of tasks that have been generated and tracked by TMS is " + str(total_tasks) + ".\n")
        task_overview_file.write("The total number of completed tasks is " + str(total_tasks - total_tasks_uncompleted) + ".\n")
        task_overview_file.write("The total number of uncompleted tasks is " + str(total_tasks_uncompleted) + ".\n")
        task_overview_file.write("The total number of uncompleted tasks that are overdue is " + str(total_tasks_overdue) + ".\n")
        task_overview_file.write("The percentage of tasks that are uncompleted is " + str(uncompleted_percentage) + "%.\n")
        task_overview_file.write("The percentage of tasks that are overdue is " + str(overdue_percentage) + "%.")
    # Print that the task_overview.txt has been generated
    print("Notice: The file task_overview.txt has been generated!")

    # 2. Compute the data and generate user_overview.txt
    # open user_overview.txt to write it
    with open("user_overview.txt", 'w') as user_overview_file:
        # Calculate the total number of users and write the first part of the report
        total_users = len(username_password)
        user_overview_file.write("This Report that is saved in user_overview.txt has been generated on " + str(date.today()) + ".\n")
        user_overview_file.write("The total number of users that are registered on TMS is " + str(total_users) + ".\n")
        user_overview_file.write("The total number of tasks that have been generated and tracked by TMS is " + str(total_tasks) + ".\n")
        # For each user create empty variables to be used to calculate the statistics
        for key in username_password:
            user_overview_file.write("Username: " + key + "\n")
            total_user_tasks = 0
            total_user_tasks_uncompleted = 0
            total_user_tasks_overdue = 0
            # Parse the list task_list to identify the tasks that are for this user
            # increment the variables if uncompleted or overdue 
            for task_dict in task_list:
                if task_dict["username"] == key:
                    total_user_tasks += 1
                    if task_dict["completed"] == False:
                        total_user_tasks_uncompleted += 1
                    if task_dict["completed"] == False and task_dict["due_date"] < today:
                        total_user_tasks_overdue += 1
            # If there are no tasks allocated to this user write a line to outline this
            if total_user_tasks == 0:
                user_overview_file.write("\tThis user has no tasks allocated, therefore the statstics can't be generated.\n")
            else:
                # Calculate all the variables needed for the statistics
                user_total_percentage = round(total_user_tasks*100/total_tasks)
                user_uncompleted_percentage = round(total_user_tasks_uncompleted*100/total_user_tasks)
                user_completed_percentage = 100 - user_uncompleted_percentage
                user_overdue_percentage = round(total_user_tasks_overdue*100/total_user_tasks)
                # Write the statistics in the file in a certain format
                user_overview_file.write("\tThe total number of tasks assigned to this user is " + str(total_user_tasks) + ".\n")
                user_overview_file.write("\tThe percentage of the total number of tasks assigned to this user is " + str(user_total_percentage) + "%.\n")
                user_overview_file.write("\tThe percentage of the tasks assigned to this user that have been completed is " + str(user_completed_percentage) + "%.\n")
                user_overview_file.write("\tThe percentage of the tasks assigned to this user that must still be completed is " + str(user_uncompleted_percentage) + "%.\n")
                user_overview_file.write("\tThe percentage of the tasks assigned to this user that are overdue is " + str(user_overdue_percentage) + "%.\n")
    # Print that the user_overview.txt has been generated
    print("Notice: The file user_overview.txt has been generated!")

# The main menu function that calls the menu and the other functions
def main_menu():
    while True:
        # Presenting the menu to the user and making sure that the user input is converted to lower case.
        print()
        menu = input('''Main menu
    Please select one of the following options below:
    r  - Registering a user
    a  - Adding a task
    va - View all tasks
    vm - View my task
    gr - Generate reports
    ds - Display statistics
    e - Exit
: ''').lower()

        # If user selects r call the reg_user() function to add a new user to the user.txt file
        if menu == 'r':
            print("Notice: You have selected option r")
            reg_user()
        # Else if user selects a call the add_task() function to add a new task
        elif menu == 'a':
            print("Notice: You have selected option a")
            add_task()
        # Else if user selects va call the view_all() function to output all the tasks that are found in the tasks.txt
        elif menu == 'va':
            print("Notice: You have selected option va")
            view_all()
        # Else if user selects vm call the view_mine() function to output and manage all the tasks that are allocated to the logged_in user
        elif menu == 'vm':
            print("Notice: You have selected option vm")
            view_mine()
         # Else if user selects gr call generate_reports() function to generate reports which are outputed in task_overview.txt and user_overview.txt
        elif menu == 'gr':
            print("Notice: You have selected option gr")
            generate_reports()
        # Else if user selects ds display the statistics
        elif menu == 'ds' and curr_user == 'admin':
            print("Notice: You have selected option ds")
            # If one of the files doesn't exists call generate_reports() to generate the reports first
            if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
                print("Notice: One of the report files is missing.")
                generate_reports()
            # Display header to inform the user what is printed
            print("These are the statistics generated in regards to TMS: ")
            print("==================================================================")
            # Open the task_overview.txt, read it and print to the screen
            with open("task_overview.txt", 'r') as task_overview_file:
                print(task_overview_file.read())
            print("==================================================================")
            # Open the user_overview.txt, read it and print to the screen
            with open("user_overview.txt", 'r') as user_overview_file:
                print(user_overview_file.read())
            print("==================================================================")
        # Else if the user selects option e exit the program
        elif menu == 'e':
            print('Notice: You have selected option e to exit the program.\nThank you for using the TMS! Goodbye!')
            exit()
        # Else an unknown option has been introduced, outputs an error message
        else:
            print("==================================================================")
            print("Error: The option you have selected doesn't exist or you don't have admin rights!\nPlease try again!")

# MAIN PROGRAM CALLOUT
# Call the initialization function to generate variables and to call user login
initialization()

# Call the main menu function
main_menu()