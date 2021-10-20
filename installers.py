'''
CRUD File for installers
'''

import logging
import peewee as pw
import table_setup

class InstallerCollection():
    '''
    Contains collection of installer objects
    '''

    def __init__(self, employee_database):
        self.database = pw.SqliteDatabase(employee_database)
        self.conunter = 0

    def validate_input(self, emp_num):
        '''Validate that the employee exists conforms to table'''
        self.database.connect(reuse_if_open= True)
        
        if table_setup.Employee.get_or_none(EmployeeNum = emp_num):
            self.database.close()
            return True
        
        return False
    
    def add_ins(self):
        '''Add an installer to the tables'''
        pass

    def modify_ins(self):
        '''Modify installer row in table'''
        pass

    def delete_ins(self):
        '''Delete an installer out of the table'''
        pass

    def search_ins(self):
        '''Search for an installer my resource number'''
        pass