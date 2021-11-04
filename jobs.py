'''
CRUD File for Jobs
'''

import datetime
import logging
from datetime import date
import peewee as pw
import table_setup

# pylint: disable=E1120

class JobCollection():
    '''
    Contains collection for Job objects
    '''

    def __init__(self, employee_database):
        self.database = pw.SqliteDatabase(employee_database)
        logging.info("New Job Table Created")

    def validate_input(self, job_num, ins_res, due_date):
        '''
        Validate the inputs into the job table
        '''
        self.database.connect(reuse_if_open= True)

        if (len(job_num) < 11 and
            table_setup.Installer.get_or_none(ResourceID = ins_res)):
            try:
                date(int(due_date[0:4]),int(due_date[5:7]),int(due_date[8:]))
                self.database.close()
                return True
            except ValueError:
                logging.error("Date incorrect")
                self.database.close()
                return False

        self.database.close()
        return False

    def add_job(self, job_num, ins_res, due_date):
        '''Add a job to the tables'''
        if self.validate_input(job_num, ins_res, due_date):
            self.database.connect(reuse_if_open=True)
            try:
                with self.database.transaction():
                    new_job = table_setup.JobOper.create(
                        JobNum = job_num,
                        ResourceID = ins_res,
                        DueDateOverride = due_date
                    )
                    new_job.save()
                self.database.close()
                logging.info("Job %s created", job_num)
                return True
            except pw.IntegrityError:
                logging.error("Failed to create Job: %s", job_num)
                logging.info(pw.IntegrityError)
                self.database.close()
                return False
        return False

    def modify_job(self, job_num, ins_res, due_date):
        '''Modifying job op resource and due date'''
        if self.validate_input(job_num, ins_res, due_date):
            self.database.connect(reuse_if_open=True)
            try:
                if table_setup.JobOper.get_or_none(JobNum = job_num):
                    with self.database.transaction():
                        mod_job = table_setup.JobOper.update(
                            JobNum = job_num,
                            ResourceID = ins_res,
                            DueDateOverride = due_date
                        )
                        mod_job.execute()
                    self.database.close()
                    logging.info('Data updated for Job: %s', job_num)
                    return True

                raise pw.IntegrityError

            except pw.IntegrityError:
                self.database.close()
                logging.info('Error updating Job: %s', job_num)
                logging.info(pw.IntegrityError)
                return False

        return False

    def delete_job(self, job_num):
        '''Deletes existing job'''
        self.database.connect(reuse_if_open= True)
        try:
            if table_setup.JobOper.get_or_none(JobNum = job_num):
                with self.database.transaction():
                    del_user = table_setup.JobOper.delete().where(
                        table_setup.JobOper.JobNum == job_num)
                    del_user.execute()
                self.database.close()
                logging.warning('%s was DELETED', job_num)
                return True

            raise pw.IntegrityError
        except pw.IntegrityError:
            logging.info('Error deleting Job: %s', job_num)
            logging.info(pw.IntegrityError)
            self.database.close()
            return False

    def search_job(self, job_num):
        '''Search for job in the table'''
        self.database.connect(reuse_if_open= True)

        if table_setup.JobOper.get_or_none(JobNum = job_num):
            job = table_setup.JobOper.get(
                table_setup.JobOper.JobNum == job_num).JobNum
            res = table_setup.JobOper.get(
                table_setup.JobOper.JobNum == job_num).ResourceID
            due_date = table_setup.JobOper.get(
                table_setup.JobOper.JobNum == job_num).DueDateOverride
            results = [job, res, due_date]
            logging.info('%s FOUND in Collection', job_num)
            self.database.close()
            return results

        logging.info('%s NOT found in Collection', job_num)
        self.database.close()
        return False

    def job_dates(self, date_1, date_2):
        '''
        Return all the jobs between two dates, as list of peewee ModelObjects
        '''
        self.database.connect(reuse_if_open= True)

        first_date = datetime.datetime.strptime(date_1, '%Y-%m-%d')
        second_date = datetime.datetime.strptime(date_2, '%Y-%m-%d')
        date_diff = first_date.date() - second_date.date()

        if date_diff.days > 0:
            first_date = date_2
            second_date = date_1

        query = (table_setup.JobOper
            .select()
            .where(
                (table_setup.JobOper.DueDateOverride >= first_date) &
                (table_setup.JobOper.DueDateOverride <= second_date)
            )
            .limit(200)
        )

        self.database.close()
        return query
