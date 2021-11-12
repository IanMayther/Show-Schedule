'''
CRD (Create, Read, Delete) File for installers
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
        logging.info("New Installer Table Created")

    def validate_input(self, emp_num):
        '''Validate that the employee exists conforms to table'''
        self.database.connect(reuse_if_open= True)

        if table_setup.Employee.get_or_none(EmployeeNum = emp_num):
            self.database.close()
            return True

        self.database.close()
        return False

    def add_ins(self, emp_num):
        '''Add an installer to the tables'''
        if self.validate_input(emp_num):
            self.database.connect(reuse_if_open=True)
            try:
                if table_setup.Installer.get_or_none(InstallerName = emp_num):
                    raise pw.IntegrityError
                with self.database.transaction():
                    new_installer = table_setup.Installer.create(
                        ResourceID = self.counter,
                        InstallerName = emp_num
                    )
                    new_installer.save()
                self.database.close()
                logging.info("Install Resource: %s created", emp_num)
                self.counter = self.counter + 1
                return True
            except pw.IntegrityError:
                logging.error("Failed to create Install Resource: %s", emp_num)
                logging.info(pw.IntegrityError)
                self.database.close()
                return False

        return False

    def delete_ins(self, resource_id):
        '''Delete an installer out of the resource table'''
        self.database.connect(reuse_if_open= True)
        try:
            if table_setup.Installer.get_or_none(ResourceID = resource_id):
                with self.database.transaction():
                    del_installer = table_setup.Installer.delete().where(
                        table_setup.Installer.ResourceID == resource_id)
                    del_installer.execute()
                self.database.close()
                logging.warning('Resource: %s was DELETED', resource_id)
                return True

            raise pw.IntegrityError
        except pw.IntegrityError:
            logging.info('Error deleting Resource: %s', resource_id)
            logging.info(pw.IntegrityError)
            self.database.close()
            return False

    def search_ins(self, resource_id):
        '''Search for an installer my resource number'''
        self.database.connect(reuse_if_open= True)

        if table_setup.Installer.get_or_none(ResourceID = resource_id):
            res_id = table_setup.Installer.get(
                table_setup.Installer.ResourceID == resource_id).ResourceID
            emp_num = table_setup.Installer.get(
                table_setup.Installer.ResourceID == resource_id).InstallerName
            name = table_setup.Employee.get(
                table_setup.Employee.EmployeeNum == emp_num).FirstName
            last_name = table_setup.Employee.get(
                table_setup.Employee.EmployeeNum == emp_num).LastName
            results = [res_id, emp_num, name, last_name]
            logging.info('%s FOUND in Collection', emp_num)
            self.database.close()
            return results

        logging.info('%s NOT found in Collection', resource_id)
        self.database.close()
        return False
