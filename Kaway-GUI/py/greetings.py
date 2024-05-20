# Pyqt import
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from functools import partial


from db import database
from modules_two import Modules

class Greetings(QWidget):
    def __init__(self, stacked_widget):
        super(Greetings, self).__init__()
        self.stacked_widget = stacked_widget

        # Load the ui
        uic.loadUi("Kaway-GUI/pages/lessons_greetings_tab.ui", self)

        # define a-z buttons
        self.umagaButton = self.findChild(QPushButton, "UMAGA")
        self.haponButton = self.findChild(QPushButton, "HAPON")
        self.gabiButton = self.findChild(QPushButton, "GABI")
        self.arawButton = self.findChild(QPushButton, "ARAW")
        self.kumustaButton = self.findChild(QPushButton, "KUMUSTA")
        self.paalamButton = self.findChild(QPushButton, "PAALAM")
        self.ingatButton = self.findChild(QPushButton, "INGAT")
        self.salamatButton = self.findChild(QPushButton, "SALAMAT")
        self.pasensyaButton = self.findChild(QPushButton, "PASENSYA")

        # Define side buttons
        self.homeButton = self.findChild(QPushButton, "Home")
        self.homeButton.clicked.connect(self.gotoHome)
        self.lessontabButton = self.findChild(QPushButton, "Lessons")
        self.lessontabButton.clicked.connect(self.gotoLessons)

        # Define what buttons do 
        self.umagaButton.clicked.connect(partial(self.gotoAssessment, 'Magandang Umaga'))
        self.haponButton.clicked.connect(partial(self.gotoAssessment, 'Magandang Hapon'))
        self.gabiButton.clicked.connect(partial(self.gotoAssessment, 'Magandang Gabi'))
        self.arawButton.clicked.connect(partial(self.gotoAssessment, 'Magandang araw'))
        self.kumustaButton.clicked.connect(partial(self.gotoAssessment, 'Kumusta ka'))
        self.paalamButton.clicked.connect(partial(self.gotoAssessment, 'Paalam'))
        self.ingatButton.clicked.connect(partial(self.gotoAssessment, 'Ingat ka'))
        self.salamatButton.clicked.connect(partial(self.gotoAssessment, 'Maraming Salamat'))
        self.pasensyaButton.clicked.connect(partial(self.gotoAssessment, 'Pasensya na'))

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
        buttons = [self.umagaButton, self.haponButton, self.gabiButton, self.arawButton, self.kumustaButton, self.paalamButton, self.ingatButton, self.salamatButton, self.pasensyaButton]

        for index, button in enumerate(buttons):
            comp = index + 32
            if comp < latest:
                button.setEnabled(True)
            else:
                button.setEnabled(False)
                button.setText("Complete previous subtopics first")
                button.setStyleSheet('color: rgb(128, 128, 128)')