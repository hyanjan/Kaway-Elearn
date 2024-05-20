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

        # Load the ui
        uic.loadUi("Kaway-GUI/pages/hometab.ui", self)
        self.setFixedSize(1910, 950)

        # define buttons
        self.lessontabButton = self.findChild(QPushButton, "Lessons")
        self.tutorialButton = self.findChild(QPushButton, "Tutorial")
        self.userLabel = self.findChild(QLabel, "User")
        self.homegif = self.findChild(QLabel, 'GIF')
        self.movie = QMovie(r"Kaway-GUI\linear\home.gif") 
        self.homegif.setMovie(self.movie)
        self.movie.start()

        # Define what buttons do
        self.lessontabButton.clicked.connect(self.gotoLessons)
        self.tutorialButton.clicked.connect(self.gotoTutorial)

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

    def gotoTutorial(self):
        
        from tutorial import Modules
        modules = Modules(self.widget)
        self.widget.addWidget(modules)
        self.widget.setCurrentWidget(modules)

# initialize the app
app = QApplication(sys.argv)
MainWindowApp = Home()
MainWindowApp.widget = QStackedWidget()
MainWindowApp.widget.addWidget(MainWindowApp)
MainWindowApp.widget.show()
sys.exit(app.exec_())