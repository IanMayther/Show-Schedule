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
        self.assertIsInstance(main.init_employee_collection(database), employees.EmployeeCollection)

    def test_ab_installer_init(self):
        '''Test initalizing installer table'''
        self.assertIsInstance(main.init_installer_collection(database), installers.InstallerCollection)

    def test_ac_job_init(self):
        '''Test initializing job table'''
        self.assertIsInstance(main.init_job_collection(database), jobs.JobCollection)

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