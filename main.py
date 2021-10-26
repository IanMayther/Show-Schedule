'''
Module to manage employees, installers, jobs
'''

import csv
import pathlib
import logging
import employees
import installers
import jobs

def init_employee_collection(database):
    '''Initialize an employee collection'''
    return employees.EmployeeCollection(database)

def init_installer_collection(database):
    '''Initialize an installer collection'''
    return installers.InstallerCollection(database)

def init_job_collection(database):
    '''Initialize an job collection'''
    return jobs.JobCollection(database)

def add_employee(emp_num, emp_first, emp_last, emp_inactive, emp_depart, collection):
    '''Add an employee to the collection'''
    return collection.add_emp(emp_num, emp_first, emp_last, emp_inactive, emp_depart)

def modify_employee(emp_num, emp_first, emp_last, emp_inactive, emp_depart, collection):
    '''Modify the information for an existing employee, except inactivate'''
    if emp_inactive is True:
        logging.info('Error updating Employee: %s, Use inactivate method', emp_num)
        return False
    return collection.modify_emp(emp_num, emp_first, emp_last, emp_inactive, emp_depart)

def inactivate_employee():
    '''Inactivating employee removes them from necessary resource groups ie - install'''
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
2b- Inactivate employee
3- Search an employee
4- Add an installer
5- Delete an installer
6- Search an installer
7- Add a job
8- Search a job
'''