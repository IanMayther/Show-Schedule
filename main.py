'''
Module to manage employees, installers, jobs
'''

import csv
import pathlib
import employees
import installers
import jobs

existing_employee_db = {}
existing_installer_db = {}
existing_job_db = {}

def init_employee_collection(database):
    '''
    Creates a list of functions for a given employee table
    0 - Add
    1 - Modify
    2 - Inactivate
    3 - Search
    '''
    existing_employee_db[database] = [0, 1, 2, 3]

def init_installer_collection(database):
    '''
    Creates a list of functions for a given installer table
    0 - Add
    1 - Delete
    2 - Search
    '''
    existing_installer_db[database] = [0, 1, 2]

def init_job_collection(database):
    '''
    Creates a list of functions for a give job table
    0 - Add
    1 - Search
    '''
    existing_job_db[database] = [0, 1]

def add_employee():
    pass

def modify_employee():
    pass

def inactivate_employee():
    pass

def search_employee():
    pass

def add_installer():
    pass

def delete_installer():
    pass

def search_installer():
    pass

def add_job():
    pass

def search_job():
    pass

'''
1- Add an employee
2- Modify an employee
2b- Inactivate employee
3- Search an employee
4- Add an installer
5- Delete an installer
6- Search an installer
7- Add a job
8- Search a job
'''