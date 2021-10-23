'''
Testing for database functionality for Employees, Resources, JobOper
'''

import os
from unittest import TestCase
import table_setup as ts
# from mock import Mock
# from mock import patch

from employees import EmployeeCollection as EC
from installers import InstallerCollection as IC

emp_table = EC('Install_Calendar.db')
ins_table = IC('Install_Calendar.db')

class DBTest(TestCase):
    '''Test basic functionality of database'''
    def test_a_create(self):
        '''Test creating the datebase'''
        ts.db_create()
        self.assertTrue(os.path.exists('Install_Calendar.db'))

    def test_z_delete(self):
        '''Test deleting the database'''
        ts.db_delete()
        self.assertFalse(os.path.exists('Install_Calendar.db'))

class EmployeeTest(TestCase):
    '''
    Test functionality of Employee Collection with Employee Table in table_setup
    '''
    def setUp(self):
        '''Set up tables'''
        ts.db_create()

    def test_aa_val_input(self):
        '''Test the validity of input info'''
        self.assertTrue(emp_table.validate_input(0,'Ian','Igor',False,'ENG'))
        self.assertFalse(emp_table.validate_input(1234567,'Ian','Igor',False,'ENG'))
        self.assertFalse(emp_table.validate_input(0,'IanIanIanIanIanIanIanIanIanIanI',
                                            'Igor',False,'ENG'))
        self.assertFalse(emp_table.validate_input(0,'Ian', 'IgorIgorIgorIgorIgorIgorIgorIgor',
                                            False,'ENG'))
        self.assertFalse(emp_table.validate_input(0,'Ian','Igor',False,'Engineering'))

    def test_ab_add_emp(self):
        '''Add an employee to the table'''
        self.assertTrue(emp_table.add_emp(0,'Ian','Igor',False,'ENG'))
        self.assertFalse(emp_table.add_emp(0,'Ian','Igor',False,'ENG'))
        self.assertFalse(emp_table.add_emp(1,'Ian', 'IgorIgorIgorIgorIgorIgorIgorIgor',
                                    False,'ENG'))

    def test_ac_modify_emp(self):
        '''Modify an employee'''
        emp_table.add_emp(0,'Ian','Igor',False,'ENG')
        self.assertTrue(emp_table.modify_emp(0,'Ivan','Olmanov',False,'METAL'))
        self.assertFalse(emp_table.modify_emp(15,'Ivan','Olmanov',False,'METAL'))
        self.assertTrue(emp_table.modify_emp(0,'Ivan','Olmanov',True,'METAL'))
        self.assertFalse(emp_table.modify_emp(0,'Ian', 'IgorIgorIgorIgorIgorIgorIgorIgor',
                            False,'ENG'))

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
        ts.db_delete()

class InstallerTest(TestCase):
    '''
    Test functionality of Installer Collection with Installer Table in table_setup
    '''
    def setUp(self):
        '''Set up tables'''
        ts.db_create()
        emp_table.add_emp(0,'Tim','Timerson',False,'INSTALL')
        ins_table.counter = 0

    def test_af_val_inputs(self):
        '''Validate that the inputs conform to table requirements'''
        self.assertTrue(ins_table.validate_input(0))
        self.assertFalse(ins_table.validate_input(1))

    def test_ag_add_ins(self):
        '''Test adding installer to the table'''
        self.assertEqual(ins_table.counter, 0)
        self.assertTrue(ins_table.add_ins(0))
        self.assertFalse(ins_table.add_ins(1))
        self.assertEqual(ins_table.counter, 1)
        self.assertFalse(ins_table.add_ins(0))
        self.assertEqual(ins_table.counter, 1)

    def test_ah_del_ins(self):
        '''Test deleting an installer out of the table'''
        self.assertTrue(ins_table.add_ins(0))
        self.assertTrue(ins_table.delete_ins(0))
        self.assertFalse(ins_table.delete_ins(0))

    def test_ai_search_ins(self):
        '''Test searching an installer by resource #'''
        self.assertTrue(ins_table.add_ins(0))
        self.assertIsInstance(ins_table.search_ins(0), list)
        self.assertFalse(ins_table.search_ins(1))

    def tearDown(self):
        '''Delete table'''
        ts.db_delete()
