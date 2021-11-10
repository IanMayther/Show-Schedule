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
    emp_first = input('First Name: ')
    emp_last = input('Last Name: ')
    emp_depart = input('Employee Department: ')
    emp_add = main.add_employee(emp_first, emp_last, False, emp_depart, EC)
    if not emp_add:
        print('Error occured in adding Employee')
        return False
    
    print('Employee Successfully Added!')
    return True

def modify_employee():
    '''
    Updates information for an existing employee
    '''
    emp_num = input('Employee #: ')
    emp_first = input('First Name: ')
    emp_last = input('Last Name: ')
    emp_depart = input('Employee Department: ')
    emp_mod = main.modify_employee(emp_num, emp_first, emp_last, False, emp_depart, EC)
    if not emp_mod:
        print('Error occured in modifying Employee')
        return False

    print('Employee Successfully Modified!')
    return True

def search_employee():
    '''
    Searches an employee in the database
    '''
    emp_num = input('Employee #: ')
    emp_search = main.search_employee(emp_num, EC)
    if not emp_search:
        print('Could NOT find Employee')
        return False

    print('Employee #: ', emp_search[0])
    print('First Name: ', emp_search[1])
    print('Last Name: ', emp_search[2])
    print('Employee Department: ', emp_search[4])
    return True

def inactivate_employee():
    '''
    Inactivate an employee
    '''
    emp_num = input("Employee # to Inactivate: ")
    emp_ina = main.inactivate_employee(emp_num, EC)
    if not emp_ina:
        print('Error inactivating Employee #', emp_num)
        return False

    print('Inactivated Employee #', emp_num)
    return True

def add_installer():
    '''
    Add an employee as an installer resource
    '''

def add_job():
    '''
    Adds a new job into the database
    '''
    job_num = input('Job Number to add: ')
    ins_res = input('Assign Install Resource: ')
    due_date = input('Date to complete Job:')
    job_add = main.add_job(job_num, ins_res, due_date, JC)
    if not job_add:
        print('Error adding Job: ', job_num)
        return False

    print('Added Job: ', job_num)
    return True

def modify_job():
    '''
    Updates information for an existing job
    '''
    job_num = input('Job Number to modify: ')
    ins_res = input('Assign Install Resource: ')
    due_date = input('Date to complete Job:')
    job_mod = main.modify_job(job_num, ins_res, due_date, JC)
    if not job_mod:
        print('Error modifying Job: ', job_num)
        return False

    print('Modified Job: ', job_num)
    return True

def search_job():
    '''
    Searches a job in the database
    '''
    job_num = input('Job #: ')
    job_search = main.search_job(job_num, JC)
    if not job_search:
        print('Could NOT find Job')
        return False

    print('Job #: ', job_search[0])
    print('Install Resource: ', job_search[1])
    print('Due Date: ', job_search[2])
    return True

def job_range():
    '''
    Return jobs from a given range
    '''
    date_1 = input('Start Date of Range: ')
    date_2 = input('End Date of Range: ')
    query = main.search_job_range(date_1, date_1, JC)
    print(query)
    if query is None:
        print('No Jobs returned for that date range')
        return False

    for job in query:
        print('Job #{} Due {} by {}'.format(job[0], job[2], job[1]))

    return True

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
        'E': modify_employee,
        'F': search_employee,
        'G': inactivate_employee,
        'H': add_job,
        'I': modify_job,
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
                            E: Modify Employee
                            F: Search Employee
                            G: Inactivate Employee
                            H: Add Job
                            I: Modify Job
                            J: Search Job
                            K: Search Job by Range
                            L: Add Installer
                            Q: Quit
                            Please enter your choice: """)
        if user_selection.upper() in menu_options:
            menu_options[user_selection.upper()]()
        else:
            print("Invalid option")