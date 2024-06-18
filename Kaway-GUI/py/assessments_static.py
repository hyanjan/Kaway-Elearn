# Pyqt import
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2
from playsound import playsound

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
import pickle

from db import database

#initialize mediapipe
model_dict = pickle.load(open('./data_letters/model.p', 'rb'))
model = model_dict['model']
startDetection = 0
threadCamera = False

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

labels_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'Ñ', 15: 'O', 16: 'P', 17: 'Q', 18: 'R', 19: 'S', 20: 'T', 21: 'U', 22: 'V', 23: 'W', 24: 'X', 25: 'Y', 26: 'Z'}

class UI(QMainWindow):
    def __init__(self, stacked_widget):
        super(UI, self).__init__()
        self.stacked_widget = stacked_widget
        # Load the ui
        uic.loadUi("Kaway-GUI\pages\Assessments.ui", self)
        # Define the widgets here
        self.cameraButton = self.findChild(QPushButton, "StartCamera")
        self.cameraFrame = self.findChild(QLabel, "CameraFrame")
        self.detectionButton = self.findChild(QPushButton, "StartDetection")
        self.nextModuleButton = self.findChild(QPushButton, 'NextModule')
        self.answerLogo = self.findChild(QLabel, 'Check')
        self.reviewButton = self.findChild(QPushButton, 'ReviewButton')
        self.cameraFrame = self.findChild(QLabel, "CameraFrame")
        self.Error = self.findChild(QFrame, "Error")
        self.ErrorText = self.findChild(QLabel, "ErrorText")

        # Define what widgets do
        self.cameraButton.clicked.connect(self.startCameraGUI)
        self.detectionButton.clicked.connect(self.startTimer)
        self.answerLogo.hide()
        self.nextModuleButton.hide()
        self.reviewButton.hide()
        self.nextModuleButton.clicked.connect(self.gotoLessonsAlphabet)
        self.Error.hide()

        # Instance variable for capturing camera frames
        self.cap = None
        self.Detection = Detection()
        self.Detection.CameraFrame.connect(self.UpdateFrame)
        self.Detection.error.connect(self.CameraError)

        self.Detection.start()

        # change page details
        lesson = self.getLesson()
        self.rightAnswer = self.findChild(QLabel, 'UserAnswer')
        self.rightAnswer.hide()
        self.Detection.LabelTextChanged.connect(self.updateLabelText)
        self.Detection.CheckAnswer.connect(self.checkAnswer)
        self.Detection.loading.connect(self.loading)
        self.reviewButton.clicked.connect(self.goReview)


        # Define labels
        self.moduleLabel = self.findChild(QLabel, "Module")
        self.subtopicLabel = self.findChild(QLabel, "subtopic")
        self.answerText = self.findChild(QLabel, 'AnswerText')

  
        # Rename labels
        self.subtopicLabel.setText(database.getValue('module', database.findRowIDValue('right_answer', lesson)))
        self.answerText.setText(lesson)

        # Define side buttons
        self.homeButton = self.findChild(QPushButton, "Home")
        self.homeButton.clicked.connect(self.gotoHome)
        self.lessontabButton = self.findChild(QPushButton, "Lessons")
        self.lessontabButton.clicked.connect(self.gotoLessons)


    def goReview(self):
        from modules import Modules

        self.Detection.stopCamera()
        modules = Modules(self.stacked_widget)
        self.stacked_widget.addWidget(modules)
        self.stacked_widget.setCurrentWidget(modules)
    
    def loading(self, bool):
        # Loading the GIF 
        self.movie = QMovie(r"Kaway-GUI\linear\loading.gif") 
        self.answerLogo.setMovie(self.movie)
        self.movie.start()
        self.answerLogo.show()
        self.rightAnswer.show()
        self.reviewButton.hide()
        self.rightAnswer.setStyleSheet('color: rgb(0, 255, 0)')
        self.rightAnswer.setText("Detecting")
        self.answerLogo.setMovie(self.movie)
        self.movie.start()

    def updateLabelText(self, text):
        self.rightAnswer.setText(text)

    def CameraError(self):
        self.answerLogo.hide()
        self.rightAnswer.hide()
        self.ErrorText.setText('Use only one hand')
        self.Error.show()

    def checkAnswer(self, bool):
        if not bool:
            self.rightAnswer.setStyleSheet('color: rgb(255, 0, 0)')
            self.answerLogo.setPixmap(QPixmap.fromImage(QImage("Kaway-GUI\linear\cross.png")))
            self.rightAnswer.show()
            self.answerLogo.show()
            self.reviewButton.show()
            playsound('Kaway-GUI/audio/incorrect.wav')  # Play the "incorrect" sound
        else:
            self.rightAnswer.setStyleSheet('color: rgb(0, 255, 0)')
            self.answerLogo.setPixmap(QPixmap.fromImage(QImage("Kaway-GUI\linear\check.png")))
            self.nextModuleButton.show()
            self.rightAnswer.show()
            self.answerLogo.show()
            self.reviewButton.hide()
            playsound('Kaway-GUI/audio/correct.wav')  # Play the "correct" sound

    def startCameraGUI(self):
        self.Error.hide()
        self.Detection.startCamera()

    def UpdateFrame(self, img):
        self.cameraFrame.setPixmap(QPixmap.fromImage(img))

    def startTimer(self):
        if not self.Detection.cap or not self.Detection.cap.isOpened():
            self.Error.show()
            self.ErrorText.setText("Error: Open Camera First")
            return
        else:
            self.Detection.startTimer()

    def getLesson(self):
        from lessonsAlphabet import LessonsAlphabet
        lesson = LessonsAlphabet.lessonName
        return lesson

    def gotoHome(self):
        from home import Home
        print("Button clicked!")
        self.Detection.stopCamera()
        home = Home(self.stacked_widget)
        self.stacked_widget.addWidget(home)
        self.stacked_widget.setCurrentWidget(home)

    def gotoLessons(self):
        #import functions
        from lessonstab import Lessons


        self.Detection.stopCamera()
        lessons = Lessons(self.stacked_widget)
        self.stacked_widget.addWidget(lessons)
        self.stacked_widget.setCurrentWidget(lessons)

    def gotoLessonsAlphabet(self):
        if database.findRowIDValue('right_answer', database.getChosenLesson()) == database.getLatestLesson():
            database.updateLatest()

        self.Detection.stopCamera()
        from lessonsAlphabet import LessonsAlphabet
        lessonsalphabet = LessonsAlphabet(self.stacked_widget)
        self.stacked_widget.addWidget(lessonsalphabet)
        self.stacked_widget.setCurrentWidget(lessonsalphabet)




class Detection(QThread):
    # Initialize Class UI
    CameraFrame = pyqtSignal(QImage)
    LabelTextChanged = pyqtSignal(str)
    CheckAnswer = pyqtSignal(bool)
    loading = pyqtSignal(bool)
    error = pyqtSignal(bool)
    global threadCamera
    threadCamera = False

    def __init__(self):
        super().__init__()
        self.cap = None

    def startCamera(self):
        self.cap = cv2.VideoCapture(database.getCam('camera', 1))  # Open the camera (0 for integrated camera, check device list to confirm)
        if not self.cap.isOpened():
            print("Error: Couldn't open camera.")
            return

        # Set camera resolution (adjust as needed)
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Set up timer to read frames and update GUI
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.run)
        global threadCamera
        threadCamera = True
        self.timer.start(1000 // 20)  # Read frames every 33 ms (30 fps)

    def stopCamera(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()
        self.timer.stop()

    def startTimer(self):
        TIMER = int(3)
        prev = time.time()
        while TIMER >= 0:
            ret, image = self.cap.read()
            # Display countdown on each frame
            # specify the font and draw the
            # countdown using puttext
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(image, str(TIMER),
                        (200, 250), font,
                        7, (0, 255, 255),
                        4, cv2.LINE_AA)
            if ret:
                # Resize frame
                # image = cv2.resize(image, (960, 540))  # Adjust the dimensions as needed
                # Convert frame to RGB format
                rgbImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # Convert RGB image to QImage
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                qImg = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                # Convert QImage to QPixmap to display in QLabel
                pixmap = qImg.scaled(960, 540, aspectRatioMode=Qt.KeepAspectRatio)
                self.CameraFrame.emit(pixmap)
            cv2.waitKey(125)

            # current time
            cur = time.time()

            # Update and keep track of Countdown
            # if time elapsed is one second
            # then decrease the counter
            if cur-prev >= 1:
                prev = cur
                TIMER = TIMER-1
                global startDetection
                startDetection = 1

        self.loading.emit(True)    
                
                

    def getLesson(self):
        from lessonsAlphabet import LessonsAlphabet
        lesson = LessonsAlphabet.lessonName
        return lesson

    def run(self):
        answer = []
        answer_character = []

        try:
            if threadCamera == True:
                while self.cap and self.cap.isOpened():
                    # Read feed
                    ret, frame = self.cap.read()

                    # Show to screen and wait for key to be pressed
                    if ret:
                        # Resize frame
                        # image = cv2.resize(image, (960, 540))  # Adjust the dimensions as needed
                        # Convert frame to RGB format
                        rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                        # Convert RGB image to QImage
                        h, w, ch = rgbImage.shape
                        bytesPerLine = ch * w
                        qImg = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                        # Convert QImage to QPixmap to display in QLabel
                        pixmap = qImg.scaled(960, 540, aspectRatioMode=Qt.KeepAspectRatio)
                        self.CameraFrame.emit(pixmap)
                    k = cv2.waitKey(125)

                    data_aux = []
                    x_ = []
                    y_ = []
                    count = 0

                    global startDetection
                    if startDetection == 1:
                        ret, frame = self.cap.read()
                        H, W, _ = frame.shape

                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                        results = hands.process(frame_rgb)
                        if results.multi_hand_landmarks:
                            # for hand_landmarks in results.multi_hand_landmarks:
                            #     mp_drawing.draw_landmarks(
                            #         frame,  # image to draw
                            #         hand_landmarks,  # model output
                            #         mp_hands.HAND_CONNECTIONS,  # hand connections
                            #         mp_drawing_styles.get_default_hand_landmarks_style(),
                            #         mp_drawing_styles.get_default_hand_connections_style())

                            for hand_landmarks in results.multi_hand_landmarks:
                                for i in range(len(hand_landmarks.landmark)):
                                    x = hand_landmarks.landmark[i].x
                                    y = hand_landmarks.landmark[i].y

                                    x_.append(x)
                                    y_.append(y)

                                for i in range(len(hand_landmarks.landmark)):
                                    x = hand_landmarks.landmark[i].x
                                    y = hand_landmarks.landmark[i].y
                                    data_aux.append(x - min(x_))
                                    data_aux.append(y - min(y_))

                            x1 = int(min(x_) * W) - 10
                            y1 = int(min(y_) * H) - 10

                            x2 = int(max(x_) * W) - 10
                            y2 = int(max(y_) * H) - 10

                            prediction = model.predict([np.asarray(data_aux)])

                            predicted_character = labels_dict[int(prediction[0])]

                            # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                            # cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                            #             cv2.LINE_AA)
                        
                            answer.append(prediction)
                            answer_character.append(predicted_character)
                            count+=1
                            print(answer[-1])

                            if len(answer) == 15:
                                
                                if answer[3] == answer[9]:
                                    print(answer_character[9])
                                    # Emit the character string
                                    self.LabelTextChanged.emit(answer_character[9])

                                    if self.getLesson() == answer_character[9]:
                                        self.CheckAnswer.emit(True)
                                    else:
                                        self.LabelTextChanged.emit(answer_character[9])
                                        self.CheckAnswer.emit(False)
                                elif answer[3] == '13' and answer[9] == '6':
                                    print('NG')
                                    # Emit the 'NG' string
                                    self.LabelTextChanged.emit('NG')

                                    if self.getLesson() == 'NG':
                                        self.CheckAnswer.emit(True)
                                    else:
                                        self.CheckAnswer.emit(False)
                                
                                elif answer[12] == '14':
                                    print('Ñ')
                                    self.LabelTextChanged.emit('Ñ')

                                    if self.getLesson() == 'Ñ':
                                        self.CheckAnswer.emit(True)
                                    else:
                                        self.CheckAnswer.emit(False)

                                elif answer[12] == '9':
                                    print('Ñ')
                                    self.LabelTextChanged.emit('J')

                                    if self.getLesson() == 'J':
                                        self.CheckAnswer.emit(True)
                                    else:
                                        self.CheckAnswer.emit(False)

                                elif answer[12] == '26':
                                    print('Ñ')
                                    self.LabelTextChanged.emit('Z')

                                    if self.getLesson() == 'Z':
                                        self.CheckAnswer.emit(True)
                                    else:
                                        self.CheckAnswer.emit(False)   
                                else:
                                    self.LabelTextChanged.emit('Can not detect')
                                    self.CheckAnswer.emit(False)                          


                            if len(answer) == 15:
                                print("get out")
                                startDetection = 0
                                answer = []
                                answer_character = []


                            if ret:
                                # Resize frame
                                # image = cv2.resize(image, (960, 540))  # Adjust the dimensions as needed
                                # Convert frame to RGB format
                                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                
                                
                                # Convert RGB image to QImage
                                h, w, ch = rgbImage.shape
                                bytesPerLine = ch * w
                                qImg = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                                # Convert QImage to QPixmap to display in QLabel
                                pixmap = qImg.scaled(960, 540, aspectRatioMode=Qt.KeepAspectRatio)
                                self.CameraFrame.emit(pixmap)
                            cv2.waitKey(1)

                # Release the video capture and destroy OpenCV windows
                if self.cap and self.cap.isOpened():
                    self.cap.release()

        except ValueError:
            print('two hands')
            self.stopCamera()
            self.error.emit(True)                      