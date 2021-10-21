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
        self.counter = 0

    def validate_input(self, emp_num):
        '''Validate that the employee exists conforms to table'''
        self.database.connect(reuse_if_open= True)
        
        if (table_setup.Employee.get_or_none(EmployeeNum = emp_num) and not
            table_setup.Installer.get_or_none(InstallerName = emp_num)):
            self.database.close()
            return True
        
        self.database.close()
        return False
    
    def add_ins(self, emp_num):
        '''Add an installer to the tables'''
        if self.validate_input(emp_num):
            self.database.connect(reuse_if_open=True)
            try:
                with self.database.transaction():
                    new_installer = table_setup.Installer.create(
                        ResourceID = self.counter,
                        InstallerName = emp_num
                    )
                    new_installer.save()
                self.database.close()
                logging.info("Install Resource: %s created", emp_num)
                self.counter =+ 1
                return True
            except pw.IntegrityError:
                logging.error("Failed to create Install Resource: %s", emp_num)
                logging.info(pw.IntegrityError)
                self.database.close()
                return False
        
        return False

    def modify_ins(self):
        '''Modify installer row in table'''
        pass

    def delete_ins(self):
        '''Delete an installer out of the table'''
        pass

    def search_ins(self):
        '''Search for an installer my resource number'''
        pass