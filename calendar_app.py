'''Creating the GUI for the Install Calendar'''
import sys
import datetime
from PyQt5.QtWidgets import (QApplication, QComboBox, QLabel, QPushButton,
                            QVBoxLayout, QWidget, QFileDialog, QGridLayout,
                            QMainWindow, QGroupBox)
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Install Calendar")
        # Create a QGridLayout instance
        layout = QGridLayout()
        
        #Create Widgets
        self.view = QLabel()
        self.time_frame = QComboBox()    
        self.time_scope = QComboBox()    
        self.ins_grp = QLabel()
        self.ins_type = QComboBox()
        self.refresh = QPushButton("Refresh")
        self.logo = QLabel()
        self.calendar = QGroupBox("Calendar")

        #View Definition
        self.view.setStyleSheet(
            "font-size: 35px;" + 
            "color: black;"
        )
        self.view.setText("View:")

        #Combo Box for time_frame
        self.time_frame.addItem("Month", [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'])
        self.time_frame.addItem("Work Week", [])

        #Combo Box for View Scope
        self.time_scope.addItem("Item 1", ['Item[0][0]', 'Item[0][1]'])
        self.time_scope.addItem("Item 2", ['Item[1][0]', 'Item[1][1]'])

        #Install Grp Label
        self.ins_grp.setStyleSheet(
            "font-size: 35px;" + 
            "color: black;"
        )
        self.ins_grp.setText("Install Group:")

        #Combo Box for Install Type
        self.ins_type.addItem("Install Group", ['Residential', 'Commercial', 'Display'])

        #Refresh Button
        self.refresh.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.refresh.setStyleSheet(
            "*{border: 4px solid '#BC006C';" +
            "border-radius: 45px;" +
            "font-size: 35px;" + 
            "color: black;" +
            "padding: 25px 0;" +
            "margin: 100px 200px;}" +
            "*:hover{background: '#BC006C';}"
        )

        #Display logo
        image = QPixmap("logo.png")
        self.logo.setPixmap(image)
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        self.logo.setStyleSheet("margin-top: 100px;")

        # Add widgets to the layout
        layout.addWidget(self.view, 0, 0)
        layout.addWidget(self.time_frame, 0, 1)
        layout.addWidget(self.time_scope, 0, 2)
        layout.addWidget(self.ins_grp, 0, 3)
        layout.addWidget(self.ins_type, 0, 4)
        layout.addWidget(self.refresh, 0, 5)
        layout.addWidget(self.logo, 0, 6)
        layout.addWidget(self.calendar, 1, 0, 2, 5)
        # Set the layout on the application's window
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())