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


# initialize files and warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
path = os.getcwd()

class Common:
    def __init__(self, stacked_widget):
        self.stacked_widget = stacked_widget

    def gotoLessons(self):
        # Import lessons to avoid circular import
        from lessonstab import Lessons
        
        # Create an instance of the Common class
        self.lessons = Lessons(self.stacked_widget)
        print("Button clicked!")
        lessons = self.Lessons(self.stacked_widget)
        self.stacked_widget.addWidget(lessons)
        self.stacked_widget.setCurrentWidget(lessons)

    def gotoHome(self):
        # Import lessons to avoid circular import
        from home import Home
        
        # Create an instance of the Common class
        self.home = Home(self.stacked_widget)

        print("Button clicked!")
        home = self.home(self.stacked_widget)
        self.stacked_widget.addWidget(home)
        self.stacked_widget.setCurrentWidget(home)
