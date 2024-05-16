# Pyqt import
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from functools import partial

from assessments_static import *
from db import database
from modules_two import Modules

class Vocab(QWidget):
    def __init__(self, stacked_widget):
        super(Vocab, self).__init__()
        self.stacked_widget = stacked_widget

        # Load the ui
        uic.loadUi("Kaway-GUI/pages/lessons_vocab_tab.ui", self)

        # define a-z buttons
        self.bahayButton = self.findChild(QPushButton, "BAHAY")
        self.pintoButton = self.findChild(QPushButton, "PINTO")
        self.silidButton = self.findChild(QPushButton, "SILID")
        self.salaButton = self.findChild(QPushButton, "SALA")
        self.kusinaButton = self.findChild(QPushButton, "KUSINA")
        self.guroButton = self.findChild(QPushButton, "GURO")
        self.kailanButton = self.findChild(QPushButton, "KAILAN")
        self.dilawButton = self.findChild(QPushButton, "DILAW")
        self.ubeButton = self.findChild(QPushButton, "UBE")

        # Define side buttons
        self.homeButton = self.findChild(QPushButton, "Home")
        self.homeButton.clicked.connect(self.gotoHome)
        self.lessontabButton = self.findChild(QPushButton, "Lessons")
        self.lessontabButton.clicked.connect(self.gotoLessons)

        # Define what buttons do 
        self.bahayButton.clicked.connect(partial(self.gotoAssessment, 'Bahay'))
        self.pintoButton.clicked.connect(partial(self.gotoAssessment, 'Pinto'))
        self.silidButton.clicked.connect(partial(self.gotoAssessment, 'Silid'))
        self.salaButton.clicked.connect(partial(self.gotoAssessment, 'Sala'))
        self.kusinaButton.clicked.connect(partial(self.gotoAssessment, 'Kusina'))
        self.guroButton.clicked.connect(partial(self.gotoAssessment, 'Guro'))
        self.kailanButton.clicked.connect(partial(self.gotoAssessment, 'Kailan'))
        self.dilawButton.clicked.connect(partial(self.gotoAssessment, 'Dilaw'))
        self.ubeButton.clicked.connect(partial(self.gotoAssessment, 'Ube'))

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
        buttons = [self.bahayButton, self.pintoButton, self.silidButton, self.salaButton, self.kusinaButton, self.guroButton, self.kailanButton, self.dilawButton, self.ubeButton]

        for index, button in enumerate(buttons):
            comp = index + 41
            if comp < latest:
                button.setEnabled(True)
            else:
                button.setEnabled(False)
                button.setText("Complete previous subtopics first")
                button.setStyleSheet('color: rgb(128, 128, 128)')