'''
Testing for database functionality for Employees, Resources, JobOper
'''

import os
from unittest import TestCase
# from mock import Mock
# from mock import patch

from table_setup import Employee, db_create, db_delete
from employees import EmployeeCollection as EC

class DBTest(TestCase):
    '''Test basic functionality of database'''
    def test_a_create(self):
        '''Test creating the datebase'''
        db_create()
        self.assertTrue(os.path.exists('Install_Calendar.db'))
    
    def test_b_delete(self):
        '''Test deleting the database'''
        db_delete()
        self.assertFalse(os.path.exists('Install_Calendar.db'))

class EmployeeTest(TestCase):
    '''
    Test functionality of Employee Table in table_setup
    '''
    # def setUp(self):
    #     '''Set up tables'''
    #     db_create()

    def test_a_create(self):
        '''Test creating the datebase'''
        db_create()
        self.assertTrue(os.path.exists('Install_Calendar.db'))

    def test_b_add_emp(self):
        '''Add an employee to the table'''
        emp_table = EC('Install_Calendar.db')
        self.assertTrue(emp_table.add_emp(0,'Ian','Igor',False,'Engineering'))
        self.assertFalse(emp_table.add_emp(0,'Ian','Igor',False,'Engineering'))

    def test_c_delete(self):
        '''Test deleting the database'''
        db_delete()
        self.assertFalse(os.path.exists('Install_Calendar.db'))
    # def tearDown(self):
    #   db_delete()