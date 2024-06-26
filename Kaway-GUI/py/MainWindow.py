# Pyqt import
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import warnings
import os

from db import database


# initialize files and warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
path = os.getcwd()

# Initialize Classes
class Home(QMainWindow):
    def __init__(self):
        super(Home, self).__init__()
        self.setWindowTitle("Kaway - FSL Learning App") 
    
        # Load the ui
        uic.loadUi("Kaway-GUI/pages/hometab.ui", self)
        self.setFixedSize(1910, 950)

        # define buttons
        self.lessontabButton = self.findChild(QPushButton, "Lessons")
        self.userLabel = self.findChild(QLabel, "User")

        # Define what buttons do
        self.lessontabButton.clicked.connect(self.gotoLessons)

        # Set username to page
        username = database.loadUser()
        self.userLabel.setText(username)

    def gotoLessons(self):
        #import functions
        from lessonstab import Lessons
        
        print("Button clicked!")
        lessons = Lessons(self.widget)
        self.widget.addWidget(lessons)
        self.widget.setCurrentWidget(lessons)

# initialize the app
app = QApplication(sys.argv)
MainWindowApp = Home()
MainWindowApp.widget = QStackedWidget()
MainWindowApp.widget.addWidget(MainWindowApp)
MainWindowApp.widget.show()
sys.exit(app.exec_())