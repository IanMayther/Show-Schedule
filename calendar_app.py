'''Creating the GUI for the Install Calendar'''
import sys
import datetime
import random
from typing import Text
import main
from PyQt5.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel, QPushButton,
                            QVBoxLayout, QWidget, QFileDialog, QGridLayout,
                            QMainWindow, QGroupBox, QWidgetItem)
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
from calendar import monthrange

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Install Calendar")
        
        #Constants
        self.DATABASE = main.init_job_database('Install_Calendar.db')
        self.WEEKDAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        self.day_dict = self.reset_day_dict()
        self.colors = ["#023be8", "#f90798", "#423a96", "#4aadfa", "#e6e704"]

        # Create a QGridLayout instance
        outerlayout = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()
        self.b_layout = QGridLayout()
        
        #Create Widgets
        self.view = QLabel()
        self.time_frame = QComboBox()    
        self.time_scope = QComboBox()    
        self.ins_grp = QLabel()
        self.ins_type = QComboBox()
        self.refresh = QPushButton("Refresh")
        self.logo = QLabel()
        self.calendar = QLabel()
        self.details = QLabel()
        self.week_detail = QLabel()

        #View Definition
        self.view.setStyleSheet(
            "font-size: 35px;" + 
            "color: black;" +
            "padding: 25px 0px;"
        )
        self.view.setText("View:")

        #Combo Box for time_frame
        self.time_frame.addItem("Month", [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'])
        self.time_frame.addItem("Work Week", self.work_weeks())
        self.time_frame.activated.connect(self.tf_clicker)

        #Combo Box for View Scope
        self.time_scope.addItem("Item Item Item", ['Item[0][0]', 'Item[0][1]'])

        #Install Grp Label
        self.ins_grp.setStyleSheet(
            "font-size: 35px;" + 
            "color: black;"
        )
        self.ins_grp.setText("Install Group:")

        #Combo Box for Install Type
        self.ins_type.addItem("All")

        #Refresh Button
        self.refresh.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        # self.refresh.setStyleSheet(
        #     "*{border: 4px solid '#BC006C';" +
        #     "border-radius: 45px;" +
        #     "font-size: 35px;" + 
        #     "color: black;" +
        #     "padding: 25px 25px;" +
        #     "margin: 100px 200px;}" +
        #     "*:hover{background: '#BC006C';}"
        # )
        self.refresh.clicked.connect(self.refresh_manager)


        #Display logo
        image = QPixmap("logo.png")
        self.logo.setPixmap(image)
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        self.logo.setStyleSheet("margin-top: 100px;")

        #Calendar Setup
        self.calendar.setText("Calendar")
        self.calendar.setAlignment(QtCore.Qt.AlignCenter)

        #Details Setup
        self.details.setText("Details")
        self.details.setAlignment(QtCore.Qt.AlignCenter)

        # Add widgets to the layout
        row1.addWidget(self.view)
        row1.addWidget(self.time_frame)
        row1.addWidget(self.time_scope)
        row1.addWidget(self.ins_grp)
        row1.addWidget(self.ins_type)
        row1.addWidget(self.refresh)
        row1.addWidget(self.logo)
        row2.addLayout(self.b_layout)
        self.set_b_header()

        # Set the layout on the application's window
        outerlayout.addLayout(row1)
        outerlayout.addLayout(row2)
        outerlayout.addLayout(self.row3)
        self.setLayout(outerlayout)

    def reset_day_dict(self):
        '''Reset the day dictionary to default values, return dictionary'''
        return {'0': 2, '1': 2, '2': 2, '3': 2, '4': 2, '5': 2, '6': 2}

    def set_b_header(self):
        '''Reset the calendar and week_detail'''
        self.b_layout.addWidget(self.calendar, 0, 0, 1, 7)
        self.b_layout.addWidget(self.details, 0, 8, 1, 1)
        self.b_layout.addWidget(self.week_detail, 1, 8, 1, 1)
        for count, ele in enumerate(self.WEEKDAYS):
            self.b_layout.addWidget(QLabel(ele), 1, count, 1, 1)
    
    def tf_clicker(self, index):
        self.time_scope.clear()
        self.time_scope.addItems(self.time_frame.itemData(index))

    def work_weeks(self):
        today = datetime.datetime.today().date()
        week_num = datetime.date.isocalendar(today).week
        year = str(today.year)
        week_for = "{}-W{}".format(year, week_num)
        date = datetime.datetime.strptime(week_for + '-1', "%Y-W%W-%w")
        week_list = []
        for x in range(52):
            week_list.append(str(date.date() + datetime.timedelta(days=(7 * x))))

        return week_list

    def refresh_manager(self):
        '''Manage which methods to use on refresh'''
        self.calendar.setText("{} - {}".format(self.time_frame.currentText(),
                        self.time_scope.currentText()))
        
        self.clear_grid()
        if self.time_frame.currentText() == "Work Week":
            self.get_jobs_week()
        else:
            self.get_jobs_month()

        self.set_b_header()
        self.day_dict = self.reset_day_dict()

    def clear_grid(self):
        for item in reversed(range(self.b_layout.count())):
            self.b_layout.itemAt(item).widget().setParent(None)
            
        self.week_detail.clear()

    def get_jobs_week(self):
        date_start = datetime.datetime.strptime(self.time_scope.currentData(0), "%Y-%m-%d")
        date_1 = date_start + datetime.timedelta(days=-1)
        date_2 = date_start + datetime.timedelta(days=5)
        query = main.search_job_range(datetime.datetime.strftime(date_1, "%Y-%m-%d"),
                                      datetime.datetime.strftime(date_2, "%Y-%m-%d"),
                                      self.DATABASE)

        installers = []
        for item in query:
            if item.ResourceID not in installers:
                installers.append(item.ResourceID)
                
        for installer in installers:
            inst = self.installer_key(installer)
            self.row3.addWidget(inst[0])
            self.row3.addWidget(inst[1])

        for item in query:
            self.day_dict[self.get_day_of_week(item.DueDateOverride)] +=1
            self.b_layout.addWidget(
                self.create_job_button(item.JobNum, item.DueDateOverride, item.ResourceID),
                self.day_dict[self.get_day_of_week(item.DueDateOverride)],
                int(datetime.datetime.strptime(item.DueDateOverride, "%Y-%m-%d").strftime('%w'))
            )

        self.b_layout.update()

    def get_day_of_week(self, input_date):
        '''Get Day of week from DueDateOverride, returns string'''
        return datetime.datetime.strptime(input_date, "%Y-%m-%d").strftime('%w')
    
    def create_job_button(self, JobNum, DDO, Res_ID):
        '''Create the button's for each job, return button'''
        job_num = QPushButton(JobNum)
        job_num.clicked.connect(lambda: self.job_button_click(JobNum, DDO))
        return job_num

    def job_button_click(self, JobNum, DDO):
        '''Set Text of Week_detail'''
        self.week_detail.clear()
        self.week_detail.setText("Job: {} \nDue Date: {} \nComments: ".format(JobNum, DDO))

    def get_jobs_month(self):
        today = datetime.datetime.today()
        # get month 
        month = datetime.datetime.strptime(self.time_scope.currentData(0), "%B").month
        # get year
        if today.month <= month:
            year = today.year
        else:
            year = today.year + 1
        # get the first day of the month
        first_day = 1
        # get the last day of the month
        last_day = monthrange(year, month)
        # iterate over days
        day_1 = "{}-{}-01".format(year, month)
        day_x = "{}-{}-{}".format(year, month, last_day[1])
        
        query = main.search_job_range(day_1, day_x, self.DATABASE)
        
        for keys in self.day_dict:
            if int(keys) < int(self.get_day_of_week(day_1)):
                self.day_dict[keys] += 1
                self.b_layout.addWidget(
                    self.create_label(),
                    self.day_dict[keys],
                    int(keys),
                )

        due_dates = [item.DueDateOverride for item in query]

        x = first_day
        
        while x <= last_day[1]:
            if month < 10:
                target_date = "{}-0{}-{}".format(year,month, x)
            else:
                target_date = "{}-{}-{}".format(year,month, x)
            
            if target_date in due_dates:
                text = "{} \n Job Due".format(x)
                job_list = [item.JobNum for item in query if target_date == item.DueDateOverride]

                self.day_dict[self.get_day_of_week(target_date)] += 1
                self.b_layout.addWidget(
                    self.create_day_button(x, job_list),
                    self.day_dict[self.get_day_of_week(target_date)],
                    int(self.get_day_of_week(target_date))
                )
            else:
                text = "{} \n No Data".format(x)
                label = QLabel(str(x))
                label.setText(text)
                self.day_dict[self.get_day_of_week(target_date)] += 1
                self.b_layout.addWidget(
                    label,
                    self.day_dict[self.get_day_of_week(target_date)],
                    int(self.get_day_of_week(target_date))
                )
            x +=1

        self.b_layout.update()

        return True

    def create_label(self):
        '''Creates place holder labels, returns label'''
        place_holder = QLabel("No Data")
        return place_holder

    def create_day_button(self, day, jobs=list):
        '''Creates a button for jobs on same day, returns button'''
        text = "{} \n Job Due".format(day)
        button = QPushButton(text)
        button.clicked.connect(lambda: self.day_button_click(day, jobs))
        return button

    def day_button_click(self, day, jobs):
        '''Set Text of Week_detail'''
        self.week_detail.clear()
        text = "{} \n".format(day)
        for job in jobs:
            #Opportunity speed up code
            text += "{} \n".format(job)

        self.week_detail.setText(text)

    def installer_key(self, Res_ID):
        '''Create a label pair for installers, returns tuple of labels'''
        color_block = "cb{}".format(Res_ID)
        install_num = "inst{}".format(Res_ID)
        label_1 = QLabel(color_block)
        ran_num = random.randint(0, 5)
        bg_color = "background-color: {};".format(self.colors[ran_num])
        label_1.setStyleSheet(bg_color)
        label_1.setText("")
        label_2 = QLabel(install_num)
        return (label_1, label_2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
