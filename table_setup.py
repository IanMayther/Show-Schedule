'''Each Model class will correspond to a table in the database'''
import os
import peewee as pw
import logging
from datetime import date

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

today = date.today()
log_name = today.strftime("%m_%d_%Y")

formatter = logging.Formatter(LOG_FORMAT)

file_handler = logging.FileHandler('log_' + log_name + '.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

FILE_NAME = 'Install_Calendar.db'

if os.path.exists(FILE_NAME):
    os.remove(FILE_NAME)

db = pw.SqliteDatabase(FILE_NAME)

employee_names = [
        [0, 'Ian', 'Ianerson', False, 'ENG'],
        [0, 'Tim', 'Timerson', False, 'INSTALL'],
        [0, 'Ken', 'Kenerson', False, 'INSTALL'],
        [0, 'Paul', 'Paulerson', False, 'INSTALL'],
        [0, 'Russell', 'Russellson', True, 'INSTALL'],
        [0, 'Alex', 'Alexson', False, 'SALES'],
        [0, 'Darrell', 'Darrellson', False, 'INSTALL']
    ]

JobBacklog = [
        ['123456-1-1', 0, '2021-10-15'],
        ['234567-1-1', 1, '2021-10-15'],
        ['345678-1-1', 2, '2021-10-14'],
        ['456789-1-1', 2, '2021-10-13'],
        ['890123-1-1', 3, '2021-10-13'],
        ['567890-1-1', 0, '2021-10-20'],
        ['678901-1-1', 1, '2021-10-27'],
        ['789012-1-1', 3, '2021-10-20']
    ]

class BaseModel(pw.Model):
    '''
    Base Model for all tables in the Install_Calendar.db
    '''

    class Meta:
        '''Setting Meta data'''
        database = db

class Employee(BaseModel):
    '''Employees that work at the company'''

    EmployeeNum = pw.CharField(primary_key = True, max_length = 6)
    FirstName = pw.CharField(max_length = 30)
    LastName = pw.CharField(max_length = 30)
    Inactive = pw.BooleanField(default = False)
    Department = pw.CharField(max_length = 10)

class Installer(BaseModel):
    '''
    This class defines installers who can be used as a resource
    '''

    ResourceID = pw.IntegerField(primary_key = True)
    InstallerName = pw.ForeignKeyField(
        Employee, related_name = 'Given_Name', null = False
        )

class JobOper(BaseModel):
    '''
    This class defines the job operation details
    '''

    JobNum = pw.CharField(primary_key = True, max_length = 10)
    ResourceID = pw.ForeignKeyField(
        Installer, related_name = 'Installer_to_do_work', null = False
        )
    DueDateOverride = pw.DateField(formats = 'YYYY-MM-DD')

def fill_employees(input_list):
    '''
    returns the list of employees that will fill the Employee Table
    '''
    output_list = []

    emp_count = 000000

    emp_names = input_list

    for i in range(len(emp_names)):
        emp_names[i][0] = (emp_count + i)
        output_list.append(emp_names[i])

    return output_list

def fill_installers(input_list):
    '''
    Creates a list of active installers to populate the Installer table
    '''

    output_list = []

    for i in range(len(input_list)):
        if input_list[i][3] is False and input_list[i][4] == 'INSTALL':
            temp_list = [i, input_list[i][0]]
            output_list.append(temp_list)

    for i in range(len(output_list)):
        output_list[i][0] = i

    return output_list

def main():
    '''Creates tables from classes'''

    db.connect()
    db.execute_sql('PRAGMA foreign_keys = ON;')
    db.create_tables([
        Employee,
        Installer,
        JobOper,
    ])

    employees = fill_employees(employee_names)

    for person in employees:
        try:
            with db.transaction():
                new_employee = Employee.create(
                    EmployeeNum = person[0],
                    FirstName = person[1],
                    LastName = person[2],
                    Inactive = person[3],
                    Department = person[4]
                )
                new_employee.save()
                logging.info("Employee: %s created", person[1])

        except pw.IntegrityError:
            logging.error("Failed to create Employee: %s", person[1])

    installers = fill_installers(employees)

    for installer in installers:
        try:
            with db.transaction():
                new_installer = Installer.create(
                    ResourceID = installer[0],
                    InstallerName = installer[1]
                )
                new_installer.save()
                logging.info("Installer Resource: %s created", installer[0])
        except pw.IntegrityError:
                logging.error("Failed to create Install Resource: %s", installer[0])

    for job in JobBacklog:
        try:
            with db.transaction():
                new_job = JobOper.create(
                    JobNum = job[0],
                    ResourceID = job[1],
                    DueDateOverride = job[2]
                )
                new_job.save()
                logging.info("JobOper #: %s created", job[0])
        except pw.IntegrityError:
            logging.error("Failed to create JobOper #: %s", job[0])

    db.close()

if __name__ == "__main__":
    main()
