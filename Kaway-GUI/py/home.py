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
class Home(QMainWindow):
    def __init__(self, stacked_widget):
        super(Home, self).__init__()
        self.stacked_widget = stacked_widget

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


        self.FrameTwo = self.findChild(QFrame, 'UpperFrame_5')
        self.ContinueOneButton = self.findChild(QPushButton, "ContinueOne")
        self.ContinueTwoButton = self.findChild(QPushButton, "ContinueTwo")
        self.ContinueOneLabel = self.findChild(QLabel, "SubContinueOne")
        self.ContinueTwoLabel = self.findChild(QLabel, "SubContinueTwo")
        self.loadModules()

        self.Notif = self.findChild(QFrame, "NotifFrame")
        self.NotifButton = self.findChild(QPushButton, "NotifButton")
        self.NotifNum = self.findChild(QLabel, "NotifNum")
        self.NotifText = self.findChild(QLabel, "NotifText")

        self.Notif.hide()
        database.setValue()
        self.NotifButton.clicked.connect(self.gotoNotif)
        self.updateNotif()


        
        # Define what buttons do
        self.lessontabButton.clicked.connect(self.gotoLessons)
        self.tutorialButton.clicked.connect(self.gotoTutorial)
        self.ContinueOneButton.clicked.connect(self.gotoContinueOne)
        self.ContinueTwoButton.clicked.connect(self.gotoContinueTwo)

        # Set username to page
        username = database.loadUser()
        self.userLabel.setText(username)

        self.profile = self.findChild(QPushButton, "Profile")
        self.profile.clicked.connect(self.gotoProfile)
        self.settings = self.findChild(QPushButton, "Settings")
        self.settings.clicked.connect(self.gotoSettings)

    def gotoSettings(self):
        from settings import Settings
        print("Button clicked!")
        settings = Settings(self.stacked_widget)
        self.stacked_widget.addWidget(settings)
        self.stacked_widget.setCurrentWidget(settings)

    def gotoProfile(self):
        from profile import Profile
        print("Button clicked!")
        profile = Profile(self.stacked_widget)
        self.stacked_widget.addWidget(profile)
        self.stacked_widget.setCurrentWidget(profile)

    def gotoLessons(self):
        #import functions
        from lessonstab import Lessons
        
        print("Button clicked!")
        lessons = Lessons(self.stacked_widget)
        self.stacked_widget.addWidget(lessons)
        self.stacked_widget.setCurrentWidget(lessons)

    def gotoNotif(self):
        notif = database.getCam('notif', 1)
        trigger = database.getCam('trigger', 1)

        if trigger == 'True':
            if notif == 1:
                self.NotifText.setText('You have accomplished 1 module!')
            elif notif == 2:
                self.NotifText.setText('You have accomplished 2 modules!')
            elif notif == 3:
                self.NotifText.setText('You have accomplished 3 modules!')
            elif notif == 4:
                self.NotifText.setText('You have accomplished 4 modules!')
            self.Notif.show()
            
        else:
            self.Notif.hide()
        database.setValue()

    def updateNotif(self):
        notif = database.getLatestLesson()
        if notif < 29:
            self.NotifNum.setText('1')
            database.updateNotif(1)
        elif notif < 33 and notif > 28:
            self.NotifNum.setText('2')
            database.updateNotif(2)
        elif notif < 42 and notif > 32:
            self.NotifNum.setText('3')
            database.updateNotif(3)
        elif notif > 42:
            self.NotifNum.setText('4')
            database.updateNotif(4)



    def gotoTutorial(self):
        
        from tutorial import Modules
        modules = Modules(self.stacked_widget)
        self.stacked_widget.addWidget(modules)
        self.stacked_widget.setCurrentWidget(modules)

    def loadModules(self):
        lessons = database.getLatestLesson()
        if lessons < 29:
            self.FrameTwo.hide()
        elif lessons > 28 and lessons < 33:
            self.FrameTwo.show()
            self.ContinueOneButton.setText('Module 2: Introduction')
            self.ContinueOneLabel.setText('Learn the basics in proper expressions in introducing oneself')
            self.ContinueTwoButton.setText('Module 1: Alphabets')
            self.ContinueTwoLabel.setText('Learn how the basic alphabets are done in Filipino Sign Language')

        elif lessons > 32 and lessons < 42:
            self.FrameTwo.show()
            self.ContinueOneButton.setText('Module 3: Greetings')
            self.ContinueOneLabel.setText('Learn the basics in polite greetings and courteous expressions')
            self.ContinueTwoButton.setText('Module 2: Introduction')
            self.ContinueTwoLabel.setText('Learn the basics in proper expressions in introducing oneself')
        
        elif lessons > 41:
            self.FrameTwo.show()
            self.ContinueOneButton.setText('Module 4: Vocabulary')
            self.ContinueOneLabel.setText('Learn the basic vocabulary in Filipino Sign Language')
            self.ContinueTwoButton.setText('Module 3: Greetings')
            self.ContinueTwoLabel.setText('Learn the basics in polite greetings and courteous expressions')

    def gotoContinueOne(self):
        lessons = database.getLatestLesson()
        if lessons < 29:
            from lessonsAlphabet import LessonsAlphabet
            lessonsalphabet = LessonsAlphabet(self.stacked_widget)
            self.stacked_widget.addWidget(lessonsalphabet)
            self.stacked_widget.setCurrentWidget(lessonsalphabet)
        elif lessons > 28 and lessons < 33:
            from introduction import Introduction
            introduction = Introduction(self.stacked_widget)
            self.stacked_widget.addWidget(introduction)
            self.stacked_widget.setCurrentWidget(introduction)
        elif lessons > 32 and lessons < 42:
            from greetings import Greetings
            greetings = Greetings(self.stacked_widget)
            self.stacked_widget.addWidget(greetings)
            self.stacked_widget.setCurrentWidget(greetings)   
        elif lessons > 41:
            from vocab import Vocab
            vocab = Vocab(self.stacked_widget)
            self.stacked_widget.addWidget(vocab)
            self.stacked_widget.setCurrentWidget(vocab)   

    def gotoContinueTwo(self):
        lessons = database.getLatestLesson()
        if lessons > 28 and lessons < 33:            
            from lessonsAlphabet import LessonsAlphabet
            lessonsalphabet = LessonsAlphabet(self.stacked_widget)
            self.stacked_widget.addWidget(lessonsalphabet)
            self.stacked_widget.setCurrentWidget(lessonsalphabet)
        elif lessons > 32 and lessons < 42:
            from introduction import Introduction
            introduction = Introduction(self.stacked_widget)
            self.stacked_widget.addWidget(introduction)
            self.stacked_widget.setCurrentWidget(introduction)
        elif lessons > 41:
            from greetings import Greetings
            greetings = Greetings(self.stacked_widget)
            self.stacked_widget.addWidget(greetings)
            self.stacked_widget.setCurrentWidget(greetings)  