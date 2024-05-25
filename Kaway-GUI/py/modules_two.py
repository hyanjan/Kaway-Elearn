# Pyqt import
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import warnings
import os
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget


#import functions
from db import database


# initialize files and warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
path = os.getcwd()

class Modules(QWidget):
    def __init__(self, stacked_widget):
        super(Modules, self).__init__()
        self.stacked_widget = stacked_widget

        # Load the ui
        uic.loadUi("Kaway-GUI/pages/modules.ui", self)
        self.setFixedSize(1910, 950)

        # initialize mediaplayer 
        self.mediaPlayer = QMediaPlayer(self)
        self.videoWidget = self.findChild(QVideoWidget, "Player")
        self.playButton = self.findChild(QPushButton, "Play")
        self.pauseButton = self.findChild(QPushButton, "Pause")
        self.positionSlider = self.findChild(QSlider, "Slider")

        # Load video file
        video_path = f"Kaway-GUI/videos/{database.getChosenLesson()}.mp4"
        self.loadVideo(video_path)

        # Define labels
        self.moduleLabel = self.findChild(QLabel, "Module")
        self.subtopicLabel = self.findChild(QLabel, "subtopic")
        self.answerText = self.findChild(QLabel, 'AnswerText')
        self.practiceButton = self.findChild(QLabel, 'PracticeNow')
        lesson = database.getChosenLesson()

        # Rename labels
        self.subtopicLabel.setText(database.getValue('module', database.findRowIDValue('right_answer', lesson)))
        self.answerText.setText(lesson)
        self.changeModule()


        # define buttons
        self.practiceButton = self.findChild(QPushButton, "PracticeNow")
        self.homeButton = self.findChild(QPushButton, "Home")
        self.lessonsButton = self.findChild(QPushButton, "Lessons")


        # Define what buttons do
        # self.practiceButton.clicked.connect(self.gotoAssessment)
        self.homeButton.clicked.connect(self.gotoHome)
        self.lessonsButton.clicked.connect(self.gotoLessons)
        self.playButton.clicked.connect(self.play)
        self.pauseButton.clicked.connect(self.pause)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.practiceButton.clicked.connect(self.practiceNow)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.mediaStatusChanged.connect(self.handleMediaStatusChanged)

    def handleMediaStatusChanged(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.mediaPlayer.setPosition(0)
            self.mediaPlayer.play()


    def practiceNow(self):
        from assessments import UI

        practice = UI(self.stacked_widget)
        self.stacked_widget.addWidget(practice)
        self.stacked_widget.setCurrentWidget(practice)
        self.mediaPlayer.stop()

    # def getLesson(self):
    #     from lessonsAlphabet import LessonsAlphabet
    #     lesson = LessonsAlphabet.lessonName
    #     return lesson      
    
    # define side tab buttons
    def gotoLessons(self):
        #import functions
        from lessonstab import Lessons
        self.mediaPlayer.stop()
        print("Button clicked!")
        lessons = Lessons(self.stacked_widget)
        self.stacked_widget.addWidget(lessons)
        self.stacked_widget.setCurrentWidget(lessons)

    def gotoHome(self):
        from home import Home
        self.mediaPlayer.stop()
        print("Button clicked!")
        home = Home(self.stacked_widget)
        self.stacked_widget.addWidget(home)
        self.stacked_widget.setCurrentWidget(home)    

    # def gotoAssessment(self, value):
    #     LessonsAlphabet.lessonName = value
    #     print(LessonsAlphabet.lessonName)

    #     assessment = UI()
    #     self.stacked_widget.addWidget(assessment)
    #     self.stacked_widget.setCurrentWidget(assessment)

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PausedState:
            self.mediaPlayer.play()

    def pause(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def loadVideo(self, video_path):
        media = QMediaContent(QUrl.fromLocalFile(video_path))
        self.mediaPlayer.setMedia(media)
        self.mediaPlayer.play()

    def changeModule(self):
        lesson = database.findRowIDValue('right_answer', database.getChosenLesson())
        if lesson < 33:
            self.moduleLabel.setText("Module 2")
        elif lesson < 42 and lesson > 33:
            self.moduleLabel.setText("Module 3")
        elif lesson > 41:
            self.moduleLabel.setText("Module 4") 
