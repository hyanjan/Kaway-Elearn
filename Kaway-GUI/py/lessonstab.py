# Pyqt import
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import warnings
import os

#import functions
from lessonsAlphabet import LessonsAlphabet
from db import database


# initialize files and warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
path = os.getcwd()

class Lessons(QWidget):
    def __init__(self, stacked_widget):
        super(Lessons, self).__init__()
        self.stacked_widget = stacked_widget

        # Load the ui
        uic.loadUi("Kaway-GUI/pages/lessonstab.ui", self)
        self.setFixedSize(1910, 950)

        # define buttons
        self.lessonAlphabetButton = self.findChild(QPushButton, "ModuleOne")
        self.homeButton = self.findChild(QPushButton, "Home")
        self.moduleOne = self.findChild(QPushButton, 'ModuleOne')
        self.moduleTwo = self.findChild(QPushButton, 'ModuleTwo')
        self.moduleThree = self.findChild(QPushButton, 'ModuleThree')
        self.moduleFour = self.findChild(QPushButton, 'ModuleFour')
        self.subOne = self.findChild(QLabel, 'Subtopic1')
        self.subTwo = self.findChild(QLabel, 'Subtopic2')
        self.subThree = self.findChild(QLabel, 'Subtopic3')
        self.subFour = self.findChild(QLabel, 'Subtopic4')

        # Define what buttons do
        self.lessonAlphabetButton.clicked.connect(self.gotoLessonsAlphabet)
        self.moduleTwo.clicked.connect(self.gotoIntroduction)
        self.moduleThree.clicked.connect(self.gotoGreetings)
        self.moduleFour.clicked.connect(self.gotoVocab)
        self.homeButton.clicked.connect(self.gotoHome)

        
        self.hideModule(database.getLatestLesson())
         
    
    # define side tab buttons
    def gotoLessonsAlphabet(self):
        lessonsalphabet = LessonsAlphabet(self.stacked_widget)
        self.stacked_widget.addWidget(lessonsalphabet)
        self.stacked_widget.setCurrentWidget(lessonsalphabet)

    def gotoIntroduction(self):
        from introduction import Introduction
        introduction = Introduction(self.stacked_widget)
        self.stacked_widget.addWidget(introduction)
        self.stacked_widget.setCurrentWidget(introduction)

    def gotoGreetings(self):
        from greetings import Greetings
        greetings = Greetings(self.stacked_widget)
        self.stacked_widget.addWidget(greetings)
        self.stacked_widget.setCurrentWidget(greetings)    

    def gotoVocab(self):
        from vocab import Vocab
        vocab = Vocab(self.stacked_widget)
        self.stacked_widget.addWidget(vocab)
        self.stacked_widget.setCurrentWidget(vocab)      

    def gotoHome(self):
        from home import Home
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

    def hideModule(self, lesson):
        if lesson < 29:
            self.moduleTwo.hide()
            self.moduleThree.hide()
            self.moduleFour.hide()

            self.subTwo.setText("Module 2: Complete previous modules to unlock")
            self.subTwo.setStyleSheet('color: rgb(128, 128, 128)')
            self.subThree.setText("Module 3: Complete previous modules to unlock")
            self.subThree.setStyleSheet('color: rgb(128, 128, 128)')
            self.subFour.setText("Module 4: Complete previous modules to unlock")
            self.subFour.setStyleSheet('color: rgb(128, 128, 128)')

        elif lesson > 28 and lesson < 33:
            self.moduleThree.hide()
            self.moduleFour.hide()

            self.subThree.setText("Module 3: Complete previous modules to unlock")
            self.subThree.setStyleSheet('color: rgb(128, 128, 128)')
            self.subFour.setText("Module 4: Complete previous modules to unlock")
            self.subFour.setStyleSheet('color: rgb(128, 128, 128)')

        elif lesson > 32 and lesson < 42:
            self.moduleFour.hide()

            self.subFour.setText("Module 4: Complete previous modules to unlock")
            self.subFour.setStyleSheet('color: rgb(128, 128, 128)')

        elif lesson > 41:
            return



        