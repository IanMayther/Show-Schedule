'''
Tests main's functionality to control employees, installers, jobs
'''

from unittest import TestCase
import peewee as pw

import table_setup as ts
import employees
import installers
import jobs
import main

DATABASE = 'Install_Calendar.db'
EC = main.init_employee_database(DATABASE)
IC = main.init_installer_database(DATABASE)
JC = main.init_job_database(DATABASE)

class DBTest(TestCase):
    '''Test initializing of the tables'''

    def test_aa_employee_init(self):
        '''Test initalizing employee table'''
        self.assertIsInstance(
            main.init_employee_database(DATABASE), employees.EmployeeCollection
            )

    def test_ab_installer_init(self):
        '''Test initalizing installer table'''
        self.assertIsInstance(
            main.init_installer_database(DATABASE), installers.InstallerCollection
            )

    def test_ac_job_init(self):
        '''Test initializing job table'''
        self.assertIsInstance(main.init_job_database(DATABASE), jobs.JobCollection)

class EmpTest(TestCase):
    '''Test Employee functionality of main.py'''
    def setUp(self):
        '''Create database for each test'''
        ts.db_create()
        EC.counter = 0

    def test_ad_add_emp(self):
        '''Test adding employee to an existing collection'''
        self.assertTrue(main.add_employee('Ian', 'Ianson', False, 'ENG', EC))
        self.assertFalse(main.add_employee('Ian', 'Ianson', False, 'ENG', EC))

    def test_ae_modify_emp(self):
        '''Test modifying information for an employee'''
        main.add_employee('Ian', 'Ianson', False, 'ENG', EC)
        self.assertTrue(main.modify_employee(0, 'Ted', 'Tederson', False, 'INSTALL', EC))
        self.assertFalse(main.modify_employee(0, 'Ted', 'Tederson', True, 'INSTALL', EC))
        self.assertFalse(main.modify_employee(1, 'Ted', 'Tederson', False, 'INSTALL', EC))

    def test_af_inactivate_emp(self):
        '''Test inactivating an employee'''
        main.add_employee('Ian', 'Ianson', False, 'ENG', EC)
        self.assertTrue(main.inactivate_employee(0, EC))
        self.assertFalse(main.inactivate_employee(1, EC))
        self.assertFalse(main.inactivate_employee(0, EC))

    def test_ag_search_emp(self):
        '''Test searching for an employee'''
        main.add_employee('Ian', 'Ianson', False, 'ENG', EC)
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

class InsTest(TestCase):
    '''Test Installer functionality of main.py'''
    def setUp(self):
        '''Create database for each test'''
        ts.db_create()
        EC.counter = 0
        main.add_employee('Ian', 'Ianson', False, 'ENG', EC)
        IC.counter = 0

    def test_ah_add_ins(self):
        '''Test adding an installer to the database'''
        self.assertTrue(main.add_installer(0, IC))
        self.assertFalse(main.add_installer(0, IC))

    def test_ai_del_ins(self):
        '''Test deleting an installer from the install table'''
        self.assertTrue(main.add_installer(0, IC))
        self.assertTrue(main.delete_installer(0, IC))
        self.assertFalse(main.delete_installer(0, IC))
        self.assertEqual(main.search_employee(0, EC)[0], 0)

    def test_aj_search_ins(self):
        '''Test searching an installer from the install table'''
        self.assertTrue(main.add_installer(0, IC))
        self.assertFalse(main.search_installer(1, IC))
        self.assertIsInstance(main.search_installer(0, IC), list)
        results = main.search_installer(0, IC)
        self.assertEqual(len(results), 4)
        self.assertEqual(results[0], 0)
        self.assertIsInstance(results[1], ts.Employee)
        self.assertEqual(results[2], 'Ian')
        self.assertEqual(results[3], 'Ianson')

    def tearDown(self):
        ts.db_delete()

class JobTest(TestCase):
    '''Test Job functionality of main.py'''
    def setUp(self):
        '''Create database for each test'''
        ts.db_create()
        EC.counter = 0
        main.add_employee('Ian', 'Ianson', False, 'ENG', EC)
        IC.counter = 0
        main.add_installer(0, IC)

    def test_ak_job_add(self):
        '''Adding a job to the job table'''
        self.assertTrue(main.add_job('123456-1-1', 0, '2021-10-31', JC))
        self.assertFalse(main.add_job('123456-1-1', 0, '2021-10-15', JC))

    def test_al_job_ser(self):
        '''Search for a single job in table'''
        self.assertTrue(main.add_job('123456-1-1', 0, '2021-10-31', JC))
        self.assertFalse(main.search_job('111111-1-1', JC))
        results = main.search_job('123456-1-1', JC)
        self.assertEqual(results[0], '123456-1-1')
        self.assertIsInstance(results[1], ts.Installer)
        self.assertEqual(results[2], '2021-10-31')

    def test_am_ser_jobs(self):
        '''Search for a set of jobs between two dates'''
        self.assertTrue(main.add_job('111111-1-1', 0, '2021-10-31', JC))
        self.assertTrue(main.add_job('222222-2-2', 0, '2021-11-15', JC))
        query = main.search_job_range('2021-10-01', '2022-01-01', JC)
        self.assertEqual(len(query), 2)
        self.assertIsInstance(query, pw.ModelSelect)

    def test_an_modfy_job(self):
        '''Test modifying a job in the table'''
        self.assertTrue(main.add_job('111111-1-1', 0, '2021-10-31', JC))
        self.assertTrue(main.modify_job('111111-1-1', 0, '2021-11-01', JC))
        self.assertFalse(main.modify_job('111112-1-1', 0, '2021-10-31', JC))

    def tearDown(self):
        ts.db_delete()
