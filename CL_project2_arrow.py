#===============================================================================
# Author: Christian Liguori
# Date: 03/31/21
# Program Name: CL_project2_arrow.py
# This program is a task manager that showcases the use of the Arrow python
#   library. It can create, delete and show task and uses the date and 
#   time functionality of the Arrow library to save and display times in 
#   the users timezone and in an easy to understand format.
#===============================================================================


#===============================================================================
# Library Imports
#===============================================================================
# Handle an import error if the arrow library was not installed.
try:
    import arrow
except ImportError:
    print(
        '''
        The Arrow library was not found. 
        Install the library by typing the following into your terminal: 
            pip install arrow
        '''
    )

    exit()
#===============================================================================


#===============================================================================
# Task class:
# A object that holds task data. 
#===============================================================================
class Task:
    def __init__(self, name, description, time):
        self.name = name
        self.description = description
        self.time = time
#===============================================================================


#===============================================================================
# Main functions
#===============================================================================
# Function to view the next task scheduled.
def view_next_task(tasks_array):
    task_found = False # variable used to keep track of results

    # Check if there are any tasks before continuing
    if len(tasks_array) == 0:
        print('\nNo tasks added.')
    else:
        # Loop through each task and check if it is scheduled later than now. 
        # Because the tasks are sorted based on their times, the first task
        # found that is later than now is next task.
        for task in tasks_array:
            if (task.time - arrow.now('local')).total_seconds() > -1 and \
                task_found == False:
                
                # prints the next tasks info. The indentation is skewed because
                #   the whitespace before the text is displayed to the user.
                print(
                    '''
            The next task is {} and is coming up in {}
                    '''.format(task.name, task.time.humanize()))
                
                task_found = True
    
    if task_found == False:
        print('You have no tasks comming up.')
    
    input('\nPress any key to continue: ') # wait for user input to continue
#===============================================================================


#===============================================================================
# Function that displays all of the currently stored tasks
def view_tasks(tasks_array):
    # Check if there are any tasks
    if len(tasks_array) == 0:
        print('\nNo tasks added.')
    else:
        # Loop through each task and print their data
        for task in tasks_array:
            print(
                '''
                Task Name: {}
                Task Description: {}
                Time: {}
                '''.format(task.name, task.description, \
                    task.time.format('dddd MMMM Do - hh:mm:ss A')))
    
    input('\nPress any key to continue: ') # wait for user input to continue
#===============================================================================


#===============================================================================
# Function that adds a task to the task list. It uses the Arrow library's
#   ability to parse dates and times from a string.
def add_task(tasks_array):
    task_name = input('Enter the name of the task: ')
    task_description = input('Enter a description of the task: ')

    # try to parse the time from a user submitted string. If there is an 
    #   error when parsing, a message will be displayed to the user.
    try:
        # get user input
        task_time = input('''
        Enter the time the task is scheduled for in the following format, 
        (03-28 08:00 AM or month-day hours:minutes AM/PM): ''')
        
        # Parse user input
        task_time = arrow.get(
            task_time + ' {}'.format(arrow.now('local').year), 
            'MM-DD hh:mm A YYYY', 
            tzinfo='local'
        )
    
    except:
        # catch any errors when parsing the time input string
        print(
            '''
        There was an error with the time entered. Make sure it is in the
        correct format.
            '''
        )

        input('\nPress any key to continue: ') # wait for user input to continue

        return False # stop executing this function

    # Create a new task with the information from the user
    task = Task(task_name, task_description, task_time)

    # Add task to task list
    tasks_array.append(task)

    # Sort the tasks by their time fields
    tasks_array.sort(key=lambda task:task.time)

    print('\nTask added successfully!') # print conformation message
    
    input('\nPress any key to continue: ') # wait for user input to continue
#===============================================================================


#===============================================================================
# Function to remove a task from the task list
def remove_task(task_array):
    # Get task name from user
    task_name = input('Enter the name of the task you want to remove: ')

    task_removed = False # variable to keep to keep track of results
    
    # loop through each task in the task array and check if the name of
    #   the task matches the name entered by the user. If it does, remove it.
    for task in task_array:
        if task.name == task_name and task_removed == False:
            task_array.remove(task)
            task_removed = True
    
    # Check if a task was removed and display the correct message
    if task_removed:
        print('\nThe task was removed.')
    else:
        print('\nA task with that name was not found.')

    input('\nPress any key to continue: ') # wait for user input to continue
#===============================================================================


#===============================================================================
# Setting up variables and creating test data
#===============================================================================
tasks = [] # list to hold all of the tasks created

# Create and add some tasks to the tasks list to make testing easier.
tasks.append(Task('Test Task 1', 'A premade task to make testing easier', \
    arrow.Arrow(2021, 3, 30, 10, tzinfo='local')))
tasks.append(Task('Test Task 2', 'A premade task to make testing easier', \
    arrow.Arrow(2021, 3, 31, 12, tzinfo='local')))
tasks.append(Task('Test Task 3', 'A premade task to make testing easier', \
    arrow.Arrow(2021, 3, 31, 15, tzinfo='local')))
tasks.append(Task('Test Task 4', 'A premade task to make testing easier', \
    arrow.Arrow(2021, 3, 31, 11, tzinfo='local')))

# sort all the test tasks created by their time
tasks.sort(key=lambda task:task.time)
#===============================================================================


#===============================================================================
# Starting the program
#===============================================================================
# Display a message to the user about the program.
print(
    '''
#===============================================================================
        Hello, this program is a task manager that handles the creation,
    deletion, and viewing of tasks. This is a showcase of the features of
    the Arrow python library. It makes working with dates and times easy and
    provides many utility functions to parse, format, shift, and generate dates
    and times. 
#===============================================================================
    '''
)

input('\nPress any key to continue: ') # wait for user input to continue

# Main Loop of the program. Will continue until the exit option is selected.
while True:
    print(
        '''
        Todays date is: {date}     

        The time is currently: {time}
        
        Please make a selection from the list below:
        1) Show next scheduled task
        2) View all tasks
        3) Add a task
        4) Remove a task
        0) Exit program
        '''.format(date=arrow.now('local').format('dddd MMMM Do, YYYY'), \
            time=arrow.now('local').format('hh:mm A'))
    )

    user_selection = input('>> ')

    if user_selection == '1':
        view_next_task(tasks)
    elif user_selection == '2':
        view_tasks(tasks)
    elif user_selection == '3':
        add_task(tasks)
    elif user_selection == '4':  
        remove_task(tasks)
    elif user_selection == '0':
        print('Have a nice day!')
        exit()
    else:
        print(
            '''
            SELECTION ERROR - Input not valid
            '''
        )
        
        input('\nPress any key to continue: ')# wait for user input to continue

#===============================================================================