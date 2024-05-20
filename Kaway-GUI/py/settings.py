# Pyqt import
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import warnings
import os

from db import database

# initialize files and warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
path = os.getcwd()

# Initialize Classes
class Settings(QMainWindow):
    def __init__(self, stacked_widget):
        super(Settings, self).__init__()
        self.stacked_widget = stacked_widget

        # Load the ui
        uic.loadUi("Kaway-GUI/pages/settings.ui", self)
        self.setFixedSize(1910, 950)

        # define buttons
        self.lessontabButton = self.findChild(QPushButton, "Lessons")
        self.homeButton = self.findChild(QPushButton, "Home")
        self.tutorialButton = self.findChild(QPushButton, "Tutorial")
        self.userLabel = self.findChild(QLabel, "User")

        # Define what buttons do
        self.lessontabButton.clicked.connect(self.gotoLessons)
        self.homeButton.clicked.connect(self.gotoHome)

        # Set username to page
        username = database.loadUser()
        self.userLabel.setText(username)

        self.profile = self.findChild(QPushButton, "Profile")
        self.profile.clicked.connect(self.gotoProfile)

    def gotoLessons(self):
        #import functions
        from lessonstab import Lessons
        
        print("Button clicked!")
        lessons = Lessons(self.stacked_widget)
        self.stacked_widget.addWidget(lessons)
        self.stacked_widget.setCurrentWidget(lessons)

    def gotoHome(self):
        from home import Home
        home = Home(self.stacked_widget)
        self.stacked_widget.addWidget(home)
        self.stacked_widget.setCurrentWidget(home)

    def gotoProfile(self):
        from profile import Profile
        print("Button clicked!")
        profile = Profile(self.stacked_widget)
        self.stacked_widget.addWidget(profile)
        self.stacked_widget.setCurrentWidget(profile)