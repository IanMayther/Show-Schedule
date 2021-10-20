'''Each Model class will correspond to a table in the database'''
import os
import logging
from datetime import date
import peewee as pw

# pylint: disable=R0903
# pylint: disable=C0200

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

def db_create():
    '''Creates tables from classes'''

    db.connect()
    db.execute_sql('PRAGMA foreign_keys = ON;')
    db.create_tables([
        Employee,
        Installer,
        JobOper,
    ])

    db.close()

def db_delete():
    '''Deletes tables'''
    db.close()
    if os.path.exists(FILE_NAME):
        os.remove(FILE_NAME)
