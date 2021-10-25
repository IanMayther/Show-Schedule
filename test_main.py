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

class DBTest(TestCase):
    '''Test initializing of the tables'''

    def test_aa_employee_init(self):
        '''Test initalizing employee table'''
        main.init_employee_collection(database)
        self.assertIsInstance(main.existing_employee_db[database], list)

    def test_ab_installer_init(self):
        '''Test initalizing installer table'''
        main.init_installer_collection(database)
        self.assertIsInstance(main.existing_installer_db[database], list)

    def test_ac_job_init(self):
        '''Test initializing job table'''
        main.init_job_collection(database)
        self.assertIsInstance(main.existing_job_db[database], list)

class Emp_Test(TestCase):
    '''Test Employee functionality of main.py'''
    def setUp(self):
        '''Create database for each test'''
        ts.db_create()

    def test_ad_add_emp(self):
        '''Test adding employee for '''
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