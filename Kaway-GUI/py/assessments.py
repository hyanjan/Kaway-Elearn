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
from db import database

#initialize mediapipe
mp_holistic = mp.solutions.holistic # Holistic model
mp_drawing = mp.solutions.drawing_utils # Drawing utilities

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
        self.nextModuleButton.clicked.connect(self.gotoSubtopics)
        self.Error.hide()

        # Initialize Detection
        self.initDetection()

        # Instance variable for capturing camera frames
        self.cap = None
        self.Detection = Detection()
        self.Detection.CameraFrame.connect(self.UpdateFrame)
        
        self.Detection.start()

        # change page details
        lesson = database.getChosenLesson()
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
        self.changeModule()
        

        # Define side buttons
        self.homeButton = self.findChild(QPushButton, "Home")
        self.homeButton.clicked.connect(self.gotoHome)
        self.lessontabButton = self.findChild(QPushButton, "Lessons")
        self.lessontabButton.clicked.connect(self.gotoLessons)

        #check module
        moduleCheck = False

    def initDetection(self):
        self.Detection = Detection()
        self.Detection.CameraFrame.connect(self.UpdateFrame)
        self.Detection.LabelTextChanged.connect(self.updateLabelText)
        self.Detection.CheckAnswer.connect(self.checkAnswer)
        self.Detection.loading.connect(self.loading)
        self.Detection.start()

    def closeEvent(self, event):
        self.Detection.stopCamera()
        self.Detection.quit()
        self.Detection.wait()
        event.accept()

        
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
        print("Button clicked!")
        lessons = Lessons(self.stacked_widget)
        self.stacked_widget.addWidget(lessons)
        self.stacked_widget.setCurrentWidget(lessons) 

    def changeModule(self):
        if database.findRowIDValue('right_answer', database.getChosenLesson()) < 33:
            self.moduleLabel.setText("Module 2")
        elif database.findRowIDValue('right_answer', database.getChosenLesson()) < 42 and database.findRowIDValue('right_answer', database.getChosenLesson()) > 33:
            self.moduleLabel.setText("Module 3")
        elif database.findRowIDValue('right_answer', database.getChosenLesson()) > 41:
            self.moduleLabel.setText("Module 4") 

    def gotoSubtopics(self):
        if database.findRowIDValue('right_answer', database.getChosenLesson()) == database.getLatestLesson():
            database.updateLatest()

        if database.findRowIDValue('right_answer', database.getChosenLesson()) < 33:
            self.Detection.stopCamera()
            from introduction import Introduction
            introduction = Introduction(self.stacked_widget)
            self.stacked_widget.addWidget(introduction)
            self.stacked_widget.setCurrentWidget(introduction) 
        elif database.findRowIDValue('right_answer', database.getChosenLesson()) < 42 and database.findRowIDValue('right_answer', database.getChosenLesson()) > 32:
            self.Detection.stopCamera()
            from greetings import Greetings
            greetings = Greetings(self.stacked_widget)
            self.stacked_widget.addWidget(greetings)
            self.stacked_widget.setCurrentWidget(greetings) 
        elif database.findRowIDValue('right_answer', database.getChosenLesson()) > 41:
            self.Detection.stopCamera()
            from vocab import Vocab
            vocab = Vocab(self.stacked_widget)
            self.stacked_widget.addWidget(vocab)
            self.stacked_widget.setCurrentWidget(vocab) 
    

            

class Detection(QThread):
    #Initialize Class UI
    CameraFrame = pyqtSignal(QImage)
    LabelTextChanged = pyqtSignal(str)
    CheckAnswer = pyqtSignal(bool)
    loading = pyqtSignal(bool)
    global threadCamera
    threadCamera = False

    def __init__(self):
        super(Detection, self).__init__()
        self.cap = None  # Initialize cap to None
        self.running = False  # Flag to indicate if the thread should be running
        self.actions = self.defineWords()
        self.model = self.initializeModel()
        

    def startCamera(self):
        self.cap = cv2.VideoCapture(database.getCam('camera', 1))  # Open the camera
        if not self.cap.isOpened():
            print("Error: Couldn't open camera.")
            return

        self.running = True  # Set the running flag to True

        # Set up timer to read frames and update GUI
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.run)
        global threadCamera
        threadCamera = True
        self.timer.start(1000 // 20)  # Read frames every 33 ms (30 fps)
    
    def stopCamera(self):
        self.running = False  # Set the running flag to False
        if self.cap and self.cap.isOpened():
            self.cap.release()
            self.timer.stop()
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
        self.wait()  # Wait for the thread to finish
            
        

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



    def mediapipe_detection(self, image, model):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # COLOR CONVERSION BGR 2 RGB
        image.flags.writeable = False                  # Image is no longer writeable
        results = model.process(image)                 # Make prediction
        image.flags.writeable = True                   # Image is now writeable 
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # COLOR COVERSION RGB 2 BGR
        return image, results

    def draw_landmarks(self, image, results):
        mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION) # Draw face connections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS) # Draw pose connections
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS) # Draw left hand connections
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS) # Draw right hand connections

    def draw_styled_landmarks(self, image, results):
        # Draw face connections
        mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION, 
                                mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1), 
                                mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                                ) 
        # Draw pose connections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4), 
                                mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                                ) 
        # Draw left hand connections
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4), 
                                mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
                                ) 
        # Draw right hand connections  
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                ) 
    
    def defineWords(self):
        vocabA = [42, 44, 45]
        vocabB = [48, 49, 50]
        vocabC = [43, 46, 47]
        lesson = database.findRowIDValue('right_answer', database.getChosenLesson())
        if lesson < 33:
            actions = np.array(['Ako si', 'Ano ang pangalan mo', 'Ilang taon ka na', 'Sino'])
        elif lesson < 42 and lesson > 32:
            actions = np.array(['Ingat ka', 'Kumusta ka', 'Magandang Araw', 'Magandang Gabi', 'Magandang Hapon', 'Magandang Umaga', 'Maraming Salamat', 'Paalam', 'Pasensya na'])
        elif lesson in vocabA:
            actions = np.array(['Bahay', 'Sala', 'Silid'])
        elif lesson in vocabB:
            actions = np.array(['Dilaw', 'Kusina', 'Ube'])
        elif lesson in vocabC:
            actions = np.array(['Guro', 'Kailan', 'Pinto'])
        
        return actions
    
    def definemodel(self):
        vocabA = [42, 44, 45]
        vocabB = [48, 49, 50]
        vocabC = [43, 46, 47]
        lesson = database.findRowIDValue('right_answer', database.getChosenLesson())
        if lesson < 33:
            model = 'Kaway-GUI/model/introduction.h5'
            return model
        elif lesson < 42 and lesson > 32:
            model = 'Kaway-GUI/model/greetings.h5'
            return model
        elif lesson in vocabA:
            model = 'Kaway-GUI/model/vocabA.h5'
            return model
        elif lesson in vocabB:
            model = 'Kaway-GUI/model/vocabB.h5'
            return model
        elif lesson in vocabC:
            model = 'Kaway-GUI/model/vocabC.h5'
            return model
        
        

    def initializeModel(self):
        model = Sequential()
        model.add(LSTM(64, return_sequences=False, activation='relu', input_shape=(40, 1662)))
        model.add(Dense(16, activation='relu'))
        model.add(Dense(self.actions.shape[0], activation='softmax'))
        model.load_weights(self.definemodel())
        return model

    colors = [(245,117,16), (117,245,16), (16,117,245)]
    def prob_viz(self, res, actions, input_frame, colors):
        output_frame = input_frame.copy()
        return output_frame

    def extract_keypoints(self, results):
        pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
        face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
        lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
        rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
        return np.concatenate([pose, face, lh, rh])

    def run(self):
        # 1. New detection variables
        sequence = []
        sentence = []
        predictions = []
        threshold = 0.5
        global startDetection
        startDetection = 0
        global threadCamera

        if self.cap is None:
            return  # Exit if the camera was not successfully initialized

        if threadCamera == True:



            with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
                while self.cap.isOpened() and self.running:
                    
                    TIMER = int(3) 
                    # Read feed
                    ret, frame = self.cap.read()
                    image, results = self.mediapipe_detection(frame, holistic)
                    # self.draw_styled_landmarks(image, results)


                    # Show to screen and wait for key to be pressed
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
                    k = cv2.waitKey(125) 
                    
                    
                    
                    while (startDetection == 1):
                        # Make detections
                        ret, frame = self.cap.read()
                        image, results = self.mediapipe_detection(frame, holistic)
                        # self.draw_styled_landmarks(image, results)
                        
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
                        k = cv2.waitKey(1)

                        # 2. Prediction logic
                        keypoints = self.extract_keypoints(results)

                        sequence.append(keypoints)
                        sequence = sequence[-40:]

                        
                        if len(sequence) == 40:
        
                            res = self.model.predict(np.expand_dims(sequence, axis=0))[0]
                            print(self.actions[np.argmax(res)])

                            if self.actions[np.argmax(res)] == database.getChosenLesson():
                                print('correct')
                                self.LabelTextChanged.emit(self.actions[np.argmax(res)])
                                self.CheckAnswer.emit(True)
                            else:
                                self.LabelTextChanged.emit(self.actions[np.argmax(res)])
                                self.CheckAnswer.emit(False)
                                
                            

                            predictions.append(np.argmax(res))
                            startDetection = 0
                            sequence = []
                            
                            
                        #3. Viz logic
                            if np.unique(predictions[-10:])[0]==np.argmax(res): 
                                if res[np.argmax(res)] > threshold: 
                                    
                                    if len(sentence) > 0: 
                                        if self.actions[np.argmax(res)] != sentence[-1]:
                                            sentence.append(self.actions[np.argmax(res)])
                                    else:
                                        sentence.append(self.actions[np.argmax(res)])

                            if len(sentence) > 5: 
                                sentence = sentence[-5:]
                                

                            # Viz probabilities
                            image = self.prob_viz(res, self.actions, image, self.colors)

                        # ret, image = self.cap.read()  # Read frame from camera
            # Release the video capture and destroy OpenCV windows
            if self.cap and self.cap.isOpened():
                self.cap.release()
                            