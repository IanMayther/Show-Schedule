'''
Testing for database functionality for Employees, Resources, JobOper
'''

import os
from unittest import TestCase

# from mock import Mock
# from mock import patch
import table_setup as ts
from employees import EmployeeCollection as EC
from installers import InstallerCollection as IC
from jobs import JobCollection as JC

emp_table = EC('Install_Calendar.db')
ins_table = IC('Install_Calendar.db')
job_table = JC('Install_Calendar.db')

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
        emp_table.counter = 0

    def test_aa_val_input(self):
        '''Test the validity of input info'''
        self.assertTrue(emp_table.validate_input('Ian','Igor',False,'ENG'))
        self.assertFalse(emp_table.validate_input('IanIanIanIanIanIanIanIanIanIanI',
                                            'Igor',False,'ENG'))
        self.assertFalse(emp_table.validate_input('Ian', 'IgorIgorIgorIgorIgorIgorIgorIgor',
                                            False,'ENG'))
        self.assertFalse(emp_table.validate_input('Ian','Igor',False,'Engineering'))

    def test_ab_add_emp(self):
        '''Add an employee to the table'''
        self.assertTrue(emp_table.add_emp('Ian','Igor',False,'ENG'))
        self.assertFalse(emp_table.add_emp('Ian','Igor',False,'ENG'))
        self.assertFalse(emp_table.add_emp('Ian', 'IgorIgorIgorIgorIgorIgorIgorIgor',
                                    False,'ENG'))
        emp_table.counter = 0
        self.assertFalse(emp_table.add_emp('Ian','Igor',False,'ENG'))

    def test_ac_modify_emp(self):
        '''Modify an employee'''
        emp_table.add_emp('Ian','Igor',False,'ENG')
        self.assertTrue(emp_table.modify_emp(0,'Ivan','Olmanov',False,'METAL'))
        self.assertFalse(emp_table.modify_emp(15,'Ivan','Olmanov',False,'METAL'))
        self.assertTrue(emp_table.modify_emp(0,'Ivan','Olmanov',True,'METAL'))
        self.assertFalse(emp_table.modify_emp(0,'Ian', 'IgorIgorIgorIgorIgorIgorIgorIgor',
                            False,'ENG'))

    def test_ad_delete_emp(self):
        '''Delete an employee'''
        emp_table.add_emp('Ian','Igor',False,'ENG')
        self.assertTrue(emp_table.delete_emp(0))
        self.assertFalse(emp_table.delete_emp(0))

    def test_ae_search_emp(self):
        '''Search for an employee'''
        emp_table.add_emp('Ian','Igor',False,'ENG')
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
        emp_table.counter = 0
        emp_table.add_emp('Tim','Timerson',False,'INSTALL')
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
        emp_table.add_emp('Dan','Wells',False,'INSTALL')
        self.assertTrue(ins_table.add_ins(1))
        self.assertEqual(ins_table.counter, 2)

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

class JobTest(TestCase):
    '''
    Test functionality of Job Collection with Job Table in table_setup
    '''

    def setUp(self):
        '''Set up tables'''
        ts.db_create()
        emp_table.counter = 0
        emp_table.add_emp('Tim','Timerson',False,'INSTALL')
        ins_table.counter = 0
        ins_table.add_ins(0)

    def test_aj_val_job(self):
        '''Test the validation of inputs'''
        self.assertFalse(job_table.validate_input('12345678901', 0, '2021-10-15'))
        self.assertFalse(job_table.validate_input('123456-1-1', 1, '2021-10-15'))
        self.assertFalse(job_table.validate_input('123456-1-1', 0, 'boom'))
        self.assertTrue(job_table.validate_input('123456-1-1', 0, '2021-10-15'))

    def test_ak_add_job(self):
        '''Test adding a job to the table'''
        self.assertTrue(job_table.add_job('123456-1-1', 0, '2021-10-15'))
        self.assertFalse(job_table.add_job('123456-1-1', 0, '2021-10-15'))
        self.assertFalse(job_table.add_job('123456-1-1', 0, 'boom'))

    def test_al_modify_job(self):
        '''Test modifying a job due date or resource in the tables'''
        self.assertTrue(job_table.add_job('123456-1-1', 0, '2021-10-15'))
        self.assertFalse(job_table.modify_job('123456-1-1', 1, '2021-10-15'))
        self.assertFalse(job_table.modify_job('123456-1-2', 0, '2021-10-25'))
        self.assertTrue(job_table.modify_job('123456-1-1', 0, '2021-10-25'))
        emp_table.add_emp('Ken', 'Kenerson', False, 'INSTALL')
        ins_table.add_ins(1)
        self.assertTrue(job_table.modify_job('123456-1-1', 1, '2021-10-25'))

    def test_am_delete_jobs(self):
        '''Test deleting a job from the table'''
        self.assertTrue(job_table.add_job('123456-1-1', 0, '2021-10-15'))
        self.assertTrue(job_table.delete_job('123456-1-1'))
        self.assertFalse(job_table.delete_job('123456-1-1'))

    def test_an_search_jobs(self):
        '''Test searching for jobs in the table'''
        self.assertTrue(job_table.add_job('123456-1-1', 0, '2021-10-15'))
        self.assertFalse(job_table.search_job('123456-2-1'))
        self.assertIsInstance(job_table.search_job('123456-1-1'), list)

    def tearDown(self):
        '''Delete table'''
        ts.db_delete()

class SearchJob(TestCase):
    '''Test job search functionality with a range of dates'''
    def setUp(self):
        '''Set up tables'''
        ts.db_create()
        emp_table.counter = 0
        emp_table.add_emp('Tim','Timerson',False,'INSTALL')
        ins_table.counter = 0
        ins_table.add_ins(0)

    def test_ao_jobs_search(self):
        '''Test getting multiple jobs from a between 2 dates'''
        self.assertTrue(job_table.add_job('111111-1-1', 0, '2021-10-15'))
        self.assertTrue(job_table.add_job('222222-2-2', 0, '2021-12-23'))
        query = job_table.job_dates('2021-10-01', '2021-11-01')
        self.assertEqual(len(query), 1)
        query = job_table.job_dates('2021-10-01', '2022-01-01')
        self.assertEqual(len(query), 2)
        query = job_table.job_dates('2021-10-16', '2021-12-22')
        self.assertEqual(len(query), 0)
        query = job_table.job_dates('2021-11-01', '2021-10-01')
        self.assertEqual(len(query), 1)
        query = job_table.job_dates('2021-12-25', '2022-01-01')   
        self.assertFalse(query)        
        job_num = 100000
        counter = 0
        while counter < 202:
            job_num = job_num + counter
            input_1 = str(job_num) + '-1-1'
            job_table.add_job(input_1, 0, '2021-11-15')
            counter += 1

        query = job_table.job_dates('2021-11-01', '2021-12-01')
        self.assertEqual(len(query), 200)


    def tearDown(self):
        '''Delete table'''
        ts.db_delete()
