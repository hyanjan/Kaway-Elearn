# Pyqt import
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from functools import partial

from assessments_static import *
from db import database
from modules_two import Modules



class Introduction(QWidget):
    def __init__(self, stacked_widget):
        super(Introduction, self).__init__()
        self.stacked_widget = stacked_widget

        # Load the ui
        uic.loadUi("Kaway-GUI/pages/lessons_introduce_tab.ui", self)

        lessonName = ''

        # define a-z buttons
        self.akosiButton = self.findChild(QPushButton, "AKOSI")
        self.pangalanButton = self.findChild(QPushButton, "PANGALAN")
        self.sinoButton = self.findChild(QPushButton, "SINO")
        self.taonButton = self.findChild(QPushButton, "TAON")

        # Define side buttons
        self.homeButton = self.findChild(QPushButton, "Home")
        self.homeButton.clicked.connect(self.gotoHome)
        self.lessontabButton = self.findChild(QPushButton, "Lessons")
        self.lessontabButton.clicked.connect(self.gotoLessons)

        # Define what buttons do 
        self.akosiButton.clicked.connect(partial(self.gotoAssessment, 'Ako si'))
        self.pangalanButton.clicked.connect(partial(self.gotoAssessment, 'Ano ang pangalan mo'))
        self.sinoButton.clicked.connect(partial(self.gotoAssessment, 'Sino'))
        self.taonButton.clicked.connect(partial(self.gotoAssessment, 'Ilang taon ka na'))

        self.hideSubtopic(database.getLatestLesson())

    def gotoHome(self):
        from home import Home
        print("Button clicked!")
        home = Home(self.stacked_widget)
        self.stacked_widget.addWidget(home)
        self.stacked_widget.setCurrentWidget(home)   

    def gotoLessons(self):
        #import functions
        from lessonstab import Lessons
        
        print("Button clicked!")
        lessons = Lessons(self.stacked_widget)
        self.stacked_widget.addWidget(lessons)
        self.stacked_widget.setCurrentWidget(lessons) 

    def gotoAssessment(self, value):
        print(value)
        database.putChosenLesson(value)
        print(database.getChosenLesson)

        modules = Modules(self.stacked_widget)
        self.stacked_widget.addWidget(modules)
        self.stacked_widget.setCurrentWidget(modules)

    def hideSubtopic(self, latest):
        buttons = [self.akosiButton, self.pangalanButton, self.sinoButton, self.taonButton]

        for index, button in enumerate(buttons):
            comp = index + 28
            if comp < latest:
                button.setEnabled(True)
            else:
                button.setEnabled(False)
                button.setText("Complete previous subtopics first")
                button.setStyleSheet('color: rgb(128, 128, 128)')