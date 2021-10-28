'''
Module to manage employees, installers, jobs
'''

import csv
import pathlib
import logging
import employees
import installers
import jobs

def init_employee_database(database):
    '''Initialize an employee database'''
    return employees.EmployeeCollection(database)

def init_installer_database(database):
    '''Initialize an installer database'''
    return installers.InstallerCollection(database)

def init_job_database(database):
    '''Initialize an job database'''
    return jobs.JobCollection(database)

def add_employee(emp_num, emp_first, emp_last, emp_inactive, emp_depart, database):
    '''Add an employee to the database'''
    return database.add_emp(emp_num, emp_first, emp_last, emp_inactive, emp_depart)

def modify_employee(emp_num, emp_first, emp_last, emp_inactive, emp_depart, database):
    '''Modify the information for an existing employee, except inactivate'''
    if emp_inactive is True:
        logging.info('Error updating Employee: %s, Use inactivate method', emp_num)
        return False
    return database.modify_emp(emp_num, emp_first, emp_last, emp_inactive, emp_depart)

def inactivate_employee(emp_num, database):
    '''Inactivating employee removes them from necessary resource groups ie - install'''
    emp_details = database.search_emp(emp_num)
    if isinstance(emp_details, bool) or emp_details[3] is True:
        logging.info('Error inactivating Employee: %s', emp_num)
        return False
    return database.modify_emp(emp_details[0], emp_details[1], emp_details[2],
                                True, emp_details[4])

def search_employee(emp_num, database):
    '''Searching through employee database for employee row'''
    return database.search_emp(emp_num)

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
3- Search an employee
4- Add an installer
5- Delete an installer
6- Search an installer
7- Add a job
8- Search a job
'''