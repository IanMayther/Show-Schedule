'''
Testing for database functionality for Employees, Resources, JobOper
'''

from unittest import TestCase
from mock import Mock
from mock import patch

from table_setup import Employee
from employees import EmployeeCollection as EC

class EmployeeTest(TestCase):
    '''
    Test functionality of Employee Table in table_setup
    '''
