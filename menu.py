'''
Provides a basic frontend
'''
import sys
import logging
import main
import table_setup as ts

# pylint: disable=W0703
# pylint: disable=E1133

ts.db_create()
DATABASE = 'Install_Calendar.db'
EC = main.init_employee_database(DATABASE)
IC = main.init_installer_database(DATABASE)
JC = main.init_job_database(DATABASE)

EmployeeNames = [
        ['Ian', 'Ianerson', False, 'ENG'],
        ['Tim', 'Timerson', False, 'INSTALL'],
        ['Ken', 'Kenerson', False, 'INSTALL'],
        ['Paul', 'Paulerson', False, 'INSTALL'],
        ['Russell', 'Russellson', True, 'INSTALL'],
        ['Alex', 'Alexson', False, 'SALES'],
        ['Darrell', 'Darrellson', False, 'INSTALL']
    ]

JobBacklog = [
        ['123456-1-1', 0, '2022-01-15'],
        ['234567-1-1', 1, '2022-01-15'],
        ['345678-1-1', 2, '2022-01-14'],
        ['456789-1-1', 2, '2022-01-13'],
        ['890123-1-1', 3, '2022-01-13'],
        ['567890-1-1', 0, '2022-01-20'],
        ['678901-1-1', 1, '2022-01-27'],
        ['789012-1-1', 3, '2022-01-20']
    ]

def load_employees():
    '''
    Loads employees from a list, prime the database
    '''
    try:
        for item in EmployeeNames:
            if not main.add_employee(item[0], item[1], item[2], item[3], EC):
                raise Exception
    except Exception:
        print('Failed to Load Employees')
        return False

    print('All Employees Loaded')
    return True

def load_installers():
    '''
    Loads installers from a list, prime the database
    '''
    try:
        installers = [1, 2, 3, 6]
        for item in installers:
            if not main.add_installer(item, IC):
                raise Exception
    except Exception:
        print('Failed to Load Installers')
        return False

    print('All Installers Loaded')
    return True

def load_jobs():
    '''
    Loads jobs from a list, prime the database
    '''
    try:
        for item in JobBacklog:
            if not main.add_job(item[0], item[1], item[2], JC):
                raise Exception
    except Exception:
        print('Failed to Load Jobs')
        return False

    print('All Jobs Loaded')
    return True

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
    emp_num = input('Which Employee to Install: ')
    ins_res = main.add_installer(emp_num, IC)
    if not ins_res:
        print('Error Adding Install Resource')
        return False

    print('Employee added as Install Resource')
    return True

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
    query = main.search_job_range(date_1, date_2, JC)
    if query is None:
        print('No Jobs returned for that date range')
        return False

    for job in query:
        print(f'Job #{job.JobNum} Due {job.DueDateOverride} by {job.ResourceID}')

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
