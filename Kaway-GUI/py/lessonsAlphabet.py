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

from assessments_static import *
from db import database
from modules import Modules



class LessonsAlphabet(QWidget):
    def __init__(self, stacked_widget):
        super(LessonsAlphabet, self).__init__()
        self.stacked_widget = stacked_widget

        # Load the ui
        uic.loadUi("Kaway-GUI/pages/lessons_alphabet_tab.ui", self)

        lessonName = ''

        # define a-z buttons
        self.aButton = self.findChild(QPushButton, "A")
        self.bButton = self.findChild(QPushButton, "B")
        self.cButton = self.findChild(QPushButton, "C")
        self.dButton = self.findChild(QPushButton, "D")
        self.eButton = self.findChild(QPushButton, "E")
        self.fButton = self.findChild(QPushButton, "F")
        self.gButton = self.findChild(QPushButton, "G")
        self.hButton = self.findChild(QPushButton, "H")
        self.iButton = self.findChild(QPushButton, "I")
        self.jButton = self.findChild(QPushButton, "J")
        self.kButton = self.findChild(QPushButton, "K")
        self.lButton = self.findChild(QPushButton, "L")
        self.mButton = self.findChild(QPushButton, "M")
        self.nButton = self.findChild(QPushButton, "N")
        self.enyeButton = self.findChild(QPushButton, "ENYE")
        self.ngButton = self.findChild(QPushButton, "NG")
        self.oButton = self.findChild(QPushButton, "O")
        self.pButton = self.findChild(QPushButton, "P")
        self.qButton = self.findChild(QPushButton, "Q")
        self.rButton = self.findChild(QPushButton, "R")
        self.sButton = self.findChild(QPushButton, "S")
        self.tButton = self.findChild(QPushButton, "T")
        self.uButton = self.findChild(QPushButton, "U")
        self.vButton = self.findChild(QPushButton, "V")
        self.wButton = self.findChild(QPushButton, "W")
        self.xButton = self.findChild(QPushButton, "X")
        self.yButton = self.findChild(QPushButton, "Y")
        self.zButton = self.findChild(QPushButton, "Z")

        # Define side buttons
        self.homeButton = self.findChild(QPushButton, "Home")
        self.homeButton.clicked.connect(self.gotoHome)

        # Define what buttons do 
        self.aButton.clicked.connect(partial(self.gotoAssessment, 'A'))
        self.bButton.clicked.connect(partial(self.gotoAssessment, 'B'))
        self.cButton.clicked.connect(partial(self.gotoAssessment, 'C'))
        self.dButton.clicked.connect(partial(self.gotoAssessment, 'D'))
        self.eButton.clicked.connect(partial(self.gotoAssessment, 'E'))
        self.fButton.clicked.connect(partial(self.gotoAssessment, 'F'))
        self.gButton.clicked.connect(partial(self.gotoAssessment, 'G'))
        self.hButton.clicked.connect(partial(self.gotoAssessment, 'H'))
        self.iButton.clicked.connect(partial(self.gotoAssessment, 'I'))
        self.jButton.clicked.connect(partial(self.gotoAssessment, 'J'))
        self.kButton.clicked.connect(partial(self.gotoAssessment, 'K'))
        self.lButton.clicked.connect(partial(self.gotoAssessment, 'L'))
        self.mButton.clicked.connect(partial(self.gotoAssessment, 'M'))
        self.nButton.clicked.connect(partial(self.gotoAssessment, 'N'))
        self.enyeButton.clicked.connect(partial(self.gotoAssessment, 'Ñ'))
        self.ngButton.clicked.connect(partial(self.gotoAssessment, 'NG'))
        self.oButton.clicked.connect(partial(self.gotoAssessment, 'O'))
        self.pButton.clicked.connect(partial(self.gotoAssessment, 'P'))
        self.qButton.clicked.connect(partial(self.gotoAssessment, 'Q'))
        self.rButton.clicked.connect(partial(self.gotoAssessment, 'R'))
        self.sButton.clicked.connect(partial(self.gotoAssessment, 'S'))
        self.tButton.clicked.connect(partial(self.gotoAssessment, 'T'))
        self.uButton.clicked.connect(partial(self.gotoAssessment, 'U'))
        self.vButton.clicked.connect(partial(self.gotoAssessment, 'V'))
        self.wButton.clicked.connect(partial(self.gotoAssessment, 'W'))
        self.xButton.clicked.connect(partial(self.gotoAssessment, 'X'))
        self.yButton.clicked.connect(partial(self.gotoAssessment, 'Y'))
        self.zButton.clicked.connect(partial(self.gotoAssessment, 'Z'))

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
        lessons = Lessons(self.widget)
        self.widget.addWidget(lessons)
        self.widget.setCurrentWidget(lessons) 

    def gotoAssessment(self, value):
        LessonsAlphabet.lessonName = value
        print(LessonsAlphabet.lessonName)

        modules = Modules(self.stacked_widget)
        self.stacked_widget.addWidget(modules)
        self.stacked_widget.setCurrentWidget(modules)
