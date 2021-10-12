'''
CRUD File for employees
'''

import table_setup
import peewee as pw
import logging

class EmployeeCollection():
    '''
    Contains a collection of employee objects
    '''

    def __init__(self, employee_database):
        self.database = pw.SqliteDatabase(employee_database)

    def add(self, emp_num, emp_first, emp_last, emp_inactive, emp_depart):
        '''Adding an employee to the database'''
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

    def modify(self, emp_num, emp_first, emp_last, emp_inactive, emp_depart):
        '''Modifying an employee to the database'''
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

#delete
#search

