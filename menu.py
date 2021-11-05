'''
Provides a basic frontend
'''
import sys
import logging
import main
import table_setup as ts

ts.db_create()
DATABASE = 'Install_Calendar.db'
EC = main.init_employee_database(DATABASE)
IC = main.init_installer_database(DATABASE)
JC = main.init_job_database(DATABASE)

EmployeeNames = [
        [0, 'Ian', 'Ianerson', False, 'ENG'],
        [0, 'Tim', 'Timerson', False, 'INSTALL'],
        [0, 'Ken', 'Kenerson', False, 'INSTALL'],
        [0, 'Paul', 'Paulerson', False, 'INSTALL'],
        [0, 'Russell', 'Russellson', True, 'INSTALL'],
        [0, 'Alex', 'Alexson', False, 'SALES'],
        [0, 'Darrell', 'Darrellson', False, 'INSTALL']
    ]

JobBacklog = [
        ['123456-1-1', 0, '2021-10-15'],
        ['234567-1-1', 1, '2021-10-15'],
        ['345678-1-1', 2, '2021-10-14'],
        ['456789-1-1', 2, '2021-10-13'],
        ['890123-1-1', 3, '2021-10-13'],
        ['567890-1-1', 0, '2021-10-20'],
        ['678901-1-1', 1, '2021-10-27'],
        ['789012-1-1', 3, '2021-10-20']
    ]

def load_employees():
    '''
    Loads employees from a list, prime the database
    '''
    pass

def load_installers():
    '''
    Loads installers from a list, prime the database
    '''
    pass

def load_jobs():
    '''
    Loads jobs from a list, prime the database
    '''
    pass

def add_employee():
    '''
    Adds a new employee into the database
    emp_num, emp_first, emp_last, emp_inactive, emp_depart, database
    '''
    emp_num = input('Employee #: ')
    emp_first = input('First Name: ')
    emp_last = input('Last Name: ')
    emp_depart = input('Employee Department: ')
    emp_add = main.add_employee(emp_num, emp_first, emp_last, False, emp_depart, EC)
    if not emp_add:
        print('Error occured in adding Employee')
        return False
    
    print('Employee Successfully Added!')
    return True

def update_employee():
    '''
    Updates information for an existing employee
    '''
    pass

def search_employee():
    '''
    Searches an employee in the database
    '''
    pass

def inactivate_employee():
    '''
    Inactivate an employee
    '''
    pass

def add_installer():
    '''
    Add an employee as an installer resource
    '''

def add_job():
    '''
    Adds a new job into the database
    '''
    pass

def update_job():
    '''
    Updates information for an existing job
    '''
    pass

def search_job():
    '''
    Searches a job in the database
    '''
    pass

def job_range():
    '''
    Return jobs from a given range
    '''
    pass

def quit_program():
    '''
    Quits program
    '''

    logging.info("--Program closed--")
    sys.exit(0)

if __name__ == '__main__':
    logging.info("--Program executed--")
    ts.db_create()
    DATABASE = 'Install_Calendar.db'
    EC = main.init_employee_database(DATABASE)
    IC = main.init_installer_database(DATABASE)
    JC = main.init_job_database(DATABASE)

    menu_options = {
        'A': load_employees,
        'B': load_installers,
        'C': load_jobs,
        'D': add_employee,
        'E': update_employee,
        'F': search_employee,
        'G': inactivate_employee,
        'H': add_job,
        'I': update_job,
        'J': search_job,
        'K': job_range,
        'L': add_installer,
        'Q': quit_program
    }
    while True:
        user_selection = input("""
                            A: Load Employees into database
                            B: Load Installers into database
                            C: Load Jobs into database
                            D: Add Employee
                            E: Update Employee
                            F: Search Employee
                            G: Inactivate Employee
                            H: Add Job
                            I: Update Job
                            J: Search Job
                            K: Search Job by Range
                            L: Add Installer
                            Q: Quit
                            Please enter your choice: """)
        if user_selection.upper() in menu_options:
            menu_options[user_selection.upper()]()
        else:
            print("Invalid option")