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
    def __init__(self):
        super(UI, self).__init__()

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

        # Define what widgets do
        self.cameraButton.clicked.connect(self.startCameraGUI)
        self.detectionButton.clicked.connect(self.startTimer)
        self.answerLogo.hide()
        self.nextModuleButton.hide()
        self.reviewButton.hide()
        

        # Instance variable for capturing camera frames
        self.cap = None
        self.Detection = Detection()
        self.Detection.CameraFrame.connect(self.UpdateFrame)
        
        self.Detection.start()

        # change page details
        lesson = self.getLesson()
        self.rightAnswer = self.findChild(QLabel, 'UserAnswer')
        self.rightAnswer.hide()
        self.Detection.LabelTextChanged.connect(self.updateLabelText)
        self.Detection.CheckAnswer.connect(self.checkAnswer)

        # Define labels
        self.moduleLabel = self.findChild(QLabel, "Module")
        self.subtopicLabel = self.findChild(QLabel, "subtopic")
        self.answerText = self.findChild(QLabel, 'AnswerText')

        # Rename labels
        self.subtopicLabel.setText(database.getValue('module', database.findRowIDValue('right_answer', lesson)))
        self.answerText.setText(lesson)

    def updateLabelText(self, text):
        self.rightAnswer.setText(text)

    def checkAnswer(self, bool):
        if bool == False:
            self.rightAnswer.setStyleSheet('color: rgb(255, 0, 0)')
            self.answerLogo.setPixmap(QPixmap.fromImage(QImage("Kaway-GUI\linear\cross.png")))
            self.rightAnswer.show()
            self.answerLogo.show()
            self.reviewButton.show()
        else:
            self.rightAnswer.setStyleSheet('color: rgb(0, 255, 0)')
            self.answerLogo.setPixmap(QPixmap.fromImage(QImage("Kaway-GUI\linear\check.png")))
            self.nextModuleButton.show()
            self.rightAnswer.show()
            self.answerLogo.show()
            self.reviewButton.hide()


    def startCameraGUI(self):
        self.Detection.startCamera()
        
    def UpdateFrame(self, img):
        self.cameraFrame.setPixmap(QPixmap.fromImage(img))

    def startTimer(self):
        self.Detection.startTimer()

    def getLesson(self):
        from lessonsAlphabet import LessonsAlphabet
        lesson = LessonsAlphabet.lessonName
        return lesson

        

class Detection(QThread):
    #Initialize Class UI
    CameraFrame = pyqtSignal(QImage)
    LabelTextChanged = pyqtSignal(str)
    CheckAnswer = pyqtSignal(bool)
    global threadCamera
    threadCamera = False

    def startCamera(self):
        self.cap = cv2.VideoCapture(0)  # Open the camera(value depends on camera used, 0 for integrated camera. Check device list to confirm)
        if not self.cap.isOpened():
            print("Error: Couldn't open camera.")
            return

        # Set camera resolution (adjust as needed)
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Set up timer to read frames and update GUI
        timer = QTimer(self)
        timer.timeout.connect(self.run)
        global threadCamera
        threadCamera = True
        timer.start(1000 // 20)  # Read frames every 33 ms (30 fps)

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

    def getLesson(self):
        from lessonsAlphabet import LessonsAlphabet
        lesson = LessonsAlphabet.lessonName
        return lesson

    def run(self):
        answer = []
        answer_character = []


        if threadCamera == True:
            while self.cap.isOpened():
                
                TIMER = int(3) 
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
                        for hand_landmarks in results.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(
                                frame,  # image to draw
                                hand_landmarks,  # model output
                                mp_hands.HAND_CONNECTIONS,  # hand connections
                                mp_drawing_styles.get_default_hand_landmarks_style(),
                                mp_drawing_styles.get_default_hand_connections_style())

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

                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                        cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                                    cv2.LINE_AA)
                    
                        answer.append(prediction)
                        answer_character.append(predicted_character)
                        count+=1
                        print(answer[-1])

                        if len(answer) == 10:
                            if answer[3] == answer[9]:
                                print(answer_character[9])
                                # Emit the character string
                                self.LabelTextChanged.emit(answer_character[9])

                                if self.getLesson() == answer_character[9]:
                                    self.CheckAnswer.emit(True)
                                else:
                                    self.CheckAnswer.emit(False)
                            elif answer_character[3] == '13' and answer_character[9] == '6':
                                print('NG')
                                # Emit the 'NG' string
                                self.LabelTextChanged.emit('NG')

                                if self.getLesson() == 'NG':
                                    self.CheckAnswer.emit(True)
                                else:
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
            self.cap.release()
            cv2.destroyAllWindows()

                                                    