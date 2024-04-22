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
from assessments_static import UI


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
        video_path = "Kaway-GUI/videos/test.mp4"
        self.loadVideo(video_path)
        # self.play()  # Play the video automatically when page loads

        # define buttons
        self.practiceButton = self.findChild(QPushButton, "PracticeNow")
        self.homeButton = self.findChild(QPushButton, "Home")

        # Define what buttons do
        # self.practiceButton.clicked.connect(self.gotoAssessment)
        self.homeButton.clicked.connect(self.gotoHome)
        self.playButton.clicked.connect(self.play)
        self.pauseButton.clicked.connect(self.pause)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

        
    
    # define side tab buttons
    def gotoLessons(self):
        #import functions
        from lessonstab import Lessons
        
        print("Button clicked!")
        lessons = Lessons(self.stacked_widget)
        self.stacked_widget.addWidget(lessons)
        self.stacked_widget.setCurrentWidget(lessons)

    def gotoHome(self):
        from home import Home
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

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

    def loadVideo(self, video_path):
        media = QMediaContent(QUrl.fromLocalFile(video_path))
        self.mediaPlayer.setMedia(media)
        self.mediaPlayer.play()

