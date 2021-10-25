'''
Module to manage employees, installers, jobs
'''

import csv
import pathlib
import employees
import installers
import jobs

def init_employee_collection(database):
    '''Initalizes an employee table in database'''
    return employees.EmployeeCollection(database)

def init_installer_collection(database):
    '''Initializes an installer table in database'''
    return installers.InstallerCollection(database)

def init_job_collection(database):
    '''Initializes a job table in database'''
    return jobs.JobCollection(database)

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
