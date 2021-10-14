'''
Testing for database functionality for Employees, Resources, JobOper
'''

from unittest import TestCase
# from mock import Mock
# from mock import patch

from table_setup import Employee, main
from employees import EmployeeCollection as EC

class EmployeeTest(TestCase):
    '''
    Test functionality of Employee Table in table_setup
    '''
    def setUp(self):
        '''Set up tables'''
        main()

    def test_a_add_emp(self):
        '''Add an employee to the table'''
        emp_table = EC('Install_Calendar.db')
        self.assertTrue(emp_table.add_emp(15,'Ian','Igor',False,'Engineering'))