'''
CRUD File for employees
'''

from os import name
import table_setup
import peewee as pw
import logging

class EmployeeCollection():
    '''
    Contains a collection of employee objects
    '''

    def __init__(self, employee_database):
        self.database = pw.SqliteDatabase(employee_database)

    def add_emp(self, emp_num, emp_first, emp_last, emp_inactive, emp_depart):
        '''Creating a new employee record'''
        self.database.connect(reuse_if_open=True)
        try:
            with self.database.transaction():
                new_employee = table_setup.Employee.create(
                    EmployeeNum = emp_num,
                    FirstName = emp_first,
                    LastName = emp_last,
                    Inactive = emp_inactive,
                    Department = emp_depart
                )
                new_employee.save()
                logging.info("Employee: %s created", emp_first)
                return True
        except pw.IntegrityError:
            logging.error("Failed to create Employee: %s", emp_first)
            logging.info(pw.IntegrityError)
            return False

    def modify_emp(self, emp_num, emp_first, emp_last, emp_inactive, emp_depart):
        '''Updating an employee record'''
        self.database.connect(reuse_if_open=True)
        try:
            if table_setup.Employee.get_or_none(EmployeeNum = emp_num):
                with self.database.transaction():
                    mod_emp = table_setup.Employee.update(
                        EmployeeNum = emp_num,
                        FirstName = emp_first,
                        LastName = emp_last,
                        Inactive = emp_inactive,
                        Department = emp_depart
                    )
                    mod_emp.execute()
                logging.info('Data updated for Employee: %s', emp_num)
                return True
            else:
                raise pw.IntegrityError
        except pw.IntegrityError:
            logging.info('Error updating Employee: %s', emp_num)
            logging.info(pw.IntegrityError)
            return False

    def delete_emp(self, emp_num):
        '''Deletes an existing employee'''
        self.database.connect(reuse_if_open= True)
        try:
            if table_setup.Employee.get_or_none(EmployeeNum = emp_num):
                with self.database.transaction():
                    del_user = table_setup.Employee.delete().where(
                        table_setup.Employee.EmployeeNum == emp_num)
                    del_user.execute()
                    logging.warning('%s was DELETED', emp_num)
                    return True
            else:
                raise pw.IntegrityError
        except pw.IntegrityError:
            logging.info('Error deleting employee: %s', emp_num)
            logging.info(pw.IntegrityError)
            return False

    def search_emp(self, emp_num):
        '''Searches for employee data'''
        self.database.connect(reuse_if_open= True)

        if table_setup.Employee.get_or_none(EmployeeNum = emp_num):
            name = table_setup.Employee.get(
                table_setup.Employee.EmployeeNum == emp_num).FirstName
            last_name = table_setup.Employee.get(
                table_setup.Employee.EmployeeNum == emp_num).LastName
            active = table_setup.Employee.get(
                table_setup.Employee.EmployeeNum == emp_num).Inactive
            dept = table_setup.Employee.get(
                table_setup.Employee.EmployeeNum == emp_num).Department
            results = [emp_num, name, last_name, active, dept]
            logging.info('%s FOUND in Collection', emp_num)
            return results

        logging.info('%s NOT found in Collection', emp_num)
        return False
