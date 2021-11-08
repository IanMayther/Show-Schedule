'''Testing the menu interface for local CRUD'''

import os
from sys import path, path_hooks
from unittest import TestCase
from unittest import mock
from unittest.mock import Mock
from unittest.mock import patch

import menu
import main
import table_setup as ts

ts.db_create()
DATABASE = 'Install_Calendar.db'
EC = main.init_employee_database(DATABASE)
IC = main.init_installer_database(DATABASE)
JC = main.init_job_database(DATABASE)

class MainTest(TestCase):
    '''
    Integration testing for menu.py
    '''
    def test_ad_add_employee(self):
        '''Test adding an employee in menu'''
        menu.input = Mock(return_value=['Ian', 'Ianson', False, 'ENG', EC])
        with patch('menu.main.add_employee', return_value=True):
            self.assertTrue(menu.add_employee())
        
        with patch('menu.main.add_employee', return_value=False):
            self.assertFalse(menu.add_employee())

    def test_ae_update_employee(self):
        '''Test modifying and employee in menu'''
        menu.input = Mock(return_value=[0, 'Ian', 'Ianson', False, 'ENG', EC])
        with patch('menu.main.modify_employee', return_value=True):
            self.assertTrue(menu.modify_employee())

        with patch('menu.main.modify_employee', return_value=False):
            self.assertFalse(menu.modify_employee())
    
    def test_af_search_employee(self):
        '''Test Searching for an employee in menu'''
        menu.input = Mock(return_value=[0])
        with patch('menu.main.search_employee', return_value=[0, 'Ian', 'Ianson', False, 'ENG']):
            self.assertTrue(menu.search_employee())

        with patch('menu.main.search_employee', return_value=False):
            self.assertFalse(menu.search_employee())

    def test_ag_inactivate_employee(self):
        '''Test inactivating an employee in menu'''
        menu.input = Mock(return_value=[0])
        with patch('menu.main.inactivate_employee', return_value=[0, 'Ian', 'Ianson', True, 'ENG']):
            self.assertTrue(menu.inactivate_employee())

        with patch('menu.main.inactivate_employee', return_value=False):
            self.assertFalse(menu.inactivate_employee())

    def test_ah_add_job(self):
        '''Test adding a job in menu'''
        mock.input = Mock(return_value= ['123456-1-1', 0, '2021-11-25'])
        with patch('menu.main.add_job', return_value= True):
            self.assertTrue(menu.add_job())

        with patch('menu.main.add_job', return_value= False):
            self.assertFalse(menu.add_job())

    def test_aq_quit(self):
        '''Test quitting in the menu'''
        with self.assertRaises(SystemExit):
            menu.quit_program()

"""
add_employee(emp_num, emp_first, emp_last, emp_inactive, emp_depart, database):
A: Load Employees into database
B: Load Installers into database
C: Load Jobs into database
I: Update Job
J: Search Job
K: Search Job by Range
L: Add Installer
"""