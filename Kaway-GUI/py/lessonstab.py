# Pyqt import
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import warnings
import os
import cv2
from functools import partial

#Detection req import
import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
import time
import datetime
import mediapipe as mp
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.callbacks import TensorBoard
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from scipy import stats

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
        self.homeButton.clicked.connect(self.gotoHome)

        
        self.hideModule(database.getLatestLesson())
         
    
    # define side tab buttons
    def gotoLessonsAlphabet(self):
        print("Button clicked!")
        lessonsalphabet = LessonsAlphabet(self.stacked_widget)
        self.stacked_widget.addWidget(lessonsalphabet)
        self.stacked_widget.setCurrentWidget(lessonsalphabet)

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

    def hideModule(self, lesson):
        if lesson < 29:
            self.moduleTwo.hide()
            self.moduleThree.hide()
            self.moduleFour.hide()

            self.subTwo.setText("Module 2: Complete previous modules to unlock")
            self.subThree.setText("Module 3: Complete previous modules to unlock")
            self.subFour.setText("Module 4: Complete previous modules to unlock")