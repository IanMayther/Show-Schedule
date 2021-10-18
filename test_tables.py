'''
Testing for database functionality for Employees, Resources, JobOper
'''

import os
from unittest import TestCase
# from mock import Mock
# from mock import patch

from table_setup import Employee, db_create, db_delete
from employees import EmployeeCollection as EC

emp_table = EC('Install_Calendar.db')

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
    def setUp(self):
        '''Set up tables'''
        db_create()

    def test_aa_val_input(self):
        '''Test the validity of input info'''
        self.assertTrue(emp_table.validate_input(0,'Ian','Igor',False,'ENG'))
        self.assertFalse(emp_table.validate_input(0,'IanIanIanIanIanIanIanIanIanIan',
                                            'Igor',False,'ENG'))
        self.assertFalse(emp_table.validate_input(0,'Ian', 'IgorIgorIgorIgorIgorIgorIgorIgor',
                                            False,'ENG'))
        self.assertFalse(emp_table.validate_input(0,'Ian','Igor',False,'Engineering'))      
    
    def test_ab_add_emp(self):
        '''Add an employee to the table'''
        self.assertTrue(emp_table.add_emp(0,'Ian','Igor',False,'ENG'))
        self.assertFalse(emp_table.add_emp(0,'Ian','Igor',False,'ENG'))
    
    def test_ac_modify_emp(self):
        '''Modify an employee'''
        emp_table.add_emp(0,'Ian','Igor',False,'ENG')
        self.assertTrue(emp_table.modify_emp(0,'Ivan','Olmanov',False,'METAL'))
        self.assertFalse(emp_table.modify_emp(15,'Ivan','Olmanov',False,'METAL'))
        self.assertTrue(emp_table.modify_emp(0,'Ivan','Olmanov',True,'METAL'))

    def test_ad_delete_emp(self):
        '''Delete an employee'''
        emp_table.add_emp(0,'Ian','Igor',False,'ENG')
        self.assertTrue(emp_table.delete_emp(0))
        self.assertFalse(emp_table.delete_emp(0))

    def test_ae_search_emp(self):
        '''Search for an employee'''
        emp_table.add_emp(0,'Ian','Igor',False,'ENG')
        self.assertIsInstance(emp_table.search_emp(0), list)
        answer = emp_table.search_emp(0)
        self.assertEqual(answer[0],0)
        self.assertEqual(answer[1],'Ian')
        self.assertEqual(answer[2],'Igor')
        self.assertEqual(answer[3],False)
        self.assertEqual(answer[4],'ENG')
        self.assertFalse(emp_table.search_emp(1))

    def tearDown(self):
        '''Delete table'''
        db_delete()