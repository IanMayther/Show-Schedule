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
        self.setFixedHeight(1500)
        self.setFixedWidth(1900)
        
        #Constants
        self.DATABASE = 'Install_Calendar.db'
        self.job_database= main.init_job_database(self.DATABASE)
        self.install_database = main.init_installer_database(self.DATABASE)
        self.WEEKDAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        self.day_dict = self.reset_day_dict()
        self.colors = ["#005073","#107dac","#189ad3","#1ebbd7","#71c7ec"]
        self.install_colors = ["#cb2424","#ff99cc","#6bb120","#a88c4f","#fdf25d",
                               "#fe2e2e","#ffbbee","#8ae429","#e1d5b1","#fcff83",
                               "#fe5757","#ff5588","#9afe2e","#e1e1d3","#fbfd9e"]
        self.query = 0
        self.installers = 0

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
            "padding: 25px 0px;" +
            "margin: 10px 10px"
        )
        self.view.setText("View:")
        self.view.resize(100,100)
        self.view.setFixedSize(150,100)
        self.view.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        #Combo Box for time_frame
        self.time_frame.addItem("Month", [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'])
        self.time_frame.addItem("Work Week", self.work_weeks())
        self.time_frame.activated.connect(self.tf_clicker)
        self.time_frame.setStyleSheet(
            "font-size: 35px;" + 
            "color: black;" +
            "padding: 0px 0px;" +
            "margin: 0px 0px"
        )
        self.time_frame.setFixedSize(220, 50)

        #Combo Box for View Scope
        self.time_scope.addItem("Item Item Item", ['Item[0][0]', 'Item[0][1]'])

        #Install Grp Label
        self.ins_grp.setStyleSheet(
            "font-size: 35px;" + 
            "color: black;"
        )
        self.ins_grp.setText("Install Group:")
        self.ins_grp.setVisible(False)

        #Combo Box for Install Type
        self.ins_type.addItem("All")
        self.ins_type.setVisible(False)

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
        self.logo.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
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
        outerlayout.setContentsMargins(40,40,40,40)
        self.setLayout(outerlayout)

    def reset_day_dict(self):
        '''Reset the day dictionary to default values, return dictionary'''
        return {'0': 2, '1': 2, '2': 2, '3': 2, '4': 2, '5': 2, '6': 2, 8: 2}

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

        for item in reversed(range(self.row3.count())):
            self.row3.itemAt(item).widget().setParent(None)

        self.week_detail.clear()
        self.week_detail.setStyleSheet("background-color: {}".format(self.colors[2]))

    def get_jobs_week(self):
        date_start = datetime.datetime.strptime(self.time_scope.currentData(0), "%Y-%m-%d")
        date_1 = date_start + datetime.timedelta(days=-1)
        date_2 = date_start + datetime.timedelta(days=5)
        self.query = main.search_job_range(datetime.datetime.strftime(date_1, "%Y-%m-%d"),
                                      datetime.datetime.strftime(date_2, "%Y-%m-%d"),
                                      self.job_database)

        installers = self.process_installers(self.query)

        for item in self.query:
            self.day_dict[self.get_day_of_week(item.DueDateOverride)] +=1
            temp_button = self.create_job_button(item.JobNum, item.DueDateOverride, installers[item.ResourceID][4])
            temp_button.setStyleSheet("background-color: {}".format(installers[item.ResourceID][4]))
            self.b_layout.addWidget(
                temp_button,
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
        job_num.clicked.connect(lambda: self.job_button_click(JobNum, DDO, Res_ID))
        return job_num

    def job_button_click(self, JobNum, DDO, Color):
        '''Set Text of Week_detail'''
        self.week_detail.clear()
        self.week_detail.setStyleSheet("background-color: {}".format(Color))
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
        
        self.query = main.search_job_range(day_1, day_x, self.job_database)

        self.installers = self.process_installers(self.query)
        
        for keys in self.day_dict:
            if int(keys) < int(self.get_day_of_week(day_1)):
                self.b_layout.addWidget(
                    self.create_label(),
                    self.day_dict[keys],
                    int(keys),
                )
                self.day_dict[keys] += 1

        due_dates = [item.DueDateOverride for item in self.query]

        x = first_day
        
        while x <= last_day[1]:
            if month < 10:
                target_date = "{}-0{}-{}".format(year,month, x)
            else:
                target_date = "{}-{}-{}".format(year,month, x)
            
            if target_date in due_dates:
                text = "{} \n Job Due".format(x)
                job_list = [item for item in self.query if target_date == item.DueDateOverride]
                self.b_layout.addWidget(
                    self.create_day_button(x, job_list),
                    self.day_dict[self.get_day_of_week(target_date)],
                    int(self.get_day_of_week(target_date))
                )
            else:
                text = "{} \n No Data".format(x)
                label = QLabel(str(x))
                label.setText(text)
                label.setStyleSheet("border: 1px solid black;")
                label.setAlignment(QtCore.Qt.AlignCenter)
                self.b_layout.addWidget(
                    label,
                    self.day_dict[self.get_day_of_week(target_date)],
                    int(self.get_day_of_week(target_date))
                )
            self.day_dict[self.get_day_of_week(target_date)] += 1                
            x +=1

        self.b_layout.update()

        return True

    def create_label(self):
        '''Creates place holder labels, returns label'''
        place_holder = QLabel("No Data")
        place_holder.setStyleSheet("border: 1px solid black;")
        place_holder.setAlignment(QtCore.Qt.AlignCenter)
        return place_holder

    def create_day_button(self, day, jobs=list):
        '''Creates a button for jobs on same day, returns button'''
        text = "{} \n Job Due".format(day)
        button = QPushButton(text)
        button.setStyleSheet("border: 1px solid black;")
        button.setStyleSheet("background-color: {}".format(self.colors[2]))
        button.clicked.connect(lambda: self.day_button_click(day, jobs))
        return button

    def day_button_click(self, day, jobs):
        '''Set Text of Week_detail'''
        self.week_detail.clear()
        text = "{} \n".format(day)
        self.week_detail.setText(text)
        if self.day_dict[8] > 2:
            self.b_layout.itemAtPosition(2, 8).widget().setParent(None)
            while self.day_dict[8] > 2:
                try:
                    self.b_layout.itemAtPosition(self.day_dict[8], 8).widget().setParent(None)
                except AttributeError:
                    pass

                self.day_dict[8] -= 1

        for count, job in enumerate(jobs):
            text = "{} \n".format(job)
            job_num = QLabel(text)
            location = count + self.day_dict[8]
            self.b_layout.addWidget(job_num, location,8)
            if job in self.query:
                job_num.setStyleSheet("background-color: {}".format(self.installers[job.ResourceID][4]))

    def process_installers(self, query):
        '''Process the install resources in a query, return dictionary'''
        installers = {}
        for count, item in enumerate(query):
            if item.ResourceID not in installers:
                installers[item.ResourceID] = main.search_installer(item.ResourceID, self.install_database)
                installers[item.ResourceID].append(self.install_colors[count])

        for key in installers:
            inst = self.installer_key(installers[key])
            self.row3.addWidget(inst[0])
            self.row3.addWidget(inst[1])
        
        return installers

    def installer_key(self, input_list):
        '''Create a label pair for installers, returns tuple of labels'''
        color_block = "cb{}".format(input_list[0])
        install_num = "{}".format(input_list[2])
        label_1 = QLabel(color_block)
        bg_color = "background-color: {};".format(input_list[4])
        padding = "padding: 0px 0px 0px 0px;"
        label_1.setStyleSheet(bg_color + padding)
        label_1.setText("")
        label_1.setFixedSize(50, 50)
        label_2 = QLabel(install_num)
        return (label_1, label_2)

    def random_color(self):
        '''Generates a random color for installers, returns a string'''
        hexadecimal = '#'+''.join([random.choice('ABCDEF56789') for i in range(6)])
        if hexadecimal in self.colors:
            self.random_color()
        return "{}".format(hexadecimal)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
