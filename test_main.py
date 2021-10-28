'''
Tests main's functionality to control employees, installers, jobs
'''

import os
from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

import table_setup as ts
import employees
import installers
import jobs
import main

database = 'Install_Calendar.db'
EC = main.init_employee_database(database)
IC = main.init_installer_database(database)
JC = main.init_job_database(database)

class DBTest(TestCase):
    '''Test initializing of the tables'''

    def test_aa_employee_init(self):
        '''Test initalizing employee table'''
        self.assertIsInstance(main.init_employee_database(database), employees.EmployeeCollection)

    def test_ab_installer_init(self):
        '''Test initalizing installer table'''
        self.assertIsInstance(main.init_installer_database(database), installers.InstallerCollection)

    def test_ac_job_init(self):
        '''Test initializing job table'''
        self.assertIsInstance(main.init_job_database(database), jobs.JobCollection)

class Emp_Test(TestCase):
    '''Test Employee functionality of main.py'''
    def setUp(self):
        '''Create database for each test'''
        ts.db_create()

    def test_ad_add_emp(self):
        '''Test adding employee to an existing collection'''
        self.assertTrue(main.add_employee(0, 'Ian', 'Ianson', False, 'ENG', EC))
        self.assertFalse(main.add_employee(0, 'Ian', 'Ianson', False, 'ENG', EC))

    def test_ae_modify_emp(self):
        '''Test modifying information for an employee'''
        main.add_employee(0, 'Ian', 'Ianson', False, 'ENG', EC)
        self.assertTrue(main.modify_employee(0, 'Ted', 'Tederson', False, 'INSTALL', EC))
        self.assertFalse(main.modify_employee(0, 'Ted', 'Tederson', True, 'INSTALL', EC))
        self.assertFalse(main.modify_employee(1, 'Ted', 'Tederson', False, 'INSTALL', EC))

    def test_af_inactivate_emp(self):
        '''Test inactivating an employee'''
        main.add_employee(0, 'Ian', 'Ianson', False, 'ENG', EC)
        self.assertTrue(main.inactivate_employee(0, EC))
        self.assertFalse(main.inactivate_employee(1, EC))
        self.assertFalse(main.inactivate_employee(0, EC))

    def test_ag_search_emp(self):
        '''Test searching for an employee'''
        main.add_employee(0, 'Ian', 'Ianson', False, 'ENG', EC)
        self.assertIsInstance(main.search_employee(0, EC), list)
        results = main.search_employee(0, EC)
        self.assertEqual(results[0], 0)
        self.assertEqual(results[1], 'Ian')
        self.assertEqual(results[2], 'Ianson')
        self.assertEqual(results[3], False)
        self.assertEqual(results[4], 'ENG')
        self.assertFalse(main.search_employee(1, EC))

    def tearDown(self):
        ts.db_delete()

'''
3- Search an employee
4- Add an installer
5- Delete an installer
6- Search an installer
7- Add a job
8- Search a job
'''