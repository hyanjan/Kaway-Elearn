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

#initialize mediapipe
mp_holistic = mp.solutions.holistic # Holistic model
mp_drawing = mp.solutions.drawing_utils # Drawing utilities

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load the ui
        uic.loadUi("Kaway-GUI\interface.ui", self)

        # Define the widgets here
        self.cameraButton = self.findChild(QPushButton, "StartCamera")
        self.cameraFrame = self.findChild(QLabel, "CameraFrame")
        self.detectionButton = self.findChild(QPushButton, "StartDetection")

        # Define what widgets do
        self.cameraButton.clicked.connect(self.startCameraGUI)
        self.detectionButton.clicked.connect(self.startTimer)

        # Instance variable for capturing camera frames
        self.cap = None
        self.Detection = Detection()
        self.Detection.CameraFrame.connect(self.UpdateFrame)
        self.Detection.start()

        
        # Show app
        self.show()

    def startCameraGUI(self):
        self.Detection.startCamera()
        
    def UpdateFrame(self, img):
        self.cameraFrame.setPixmap(QPixmap.fromImage(img))

    def startTimer(self):
        self.Detection.startTimer()

        

class Detection(QThread):
    #Initialize Class UI
    CameraFrame = pyqtSignal(QImage)
    global threadCamera
    threadCamera = False

    def startCamera(self):
        self.cap = cv2.VideoCapture(1)  # Open the camera(value depends on camera used, 0 for integrated camera. Check device list to confirm)
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

    actions = np.array(['Ako si', 'Ilang taon ka na', 'Sino', 'Sino ka'])
    model = Sequential()
    model.add(LSTM(64, return_sequences=False, activation='relu', input_shape=(40,1662)))
    # model.add(LSTM(128, return_sequences=True, activation='relu'))
    # model.add(LSTM(64, return_sequences=False, activation='relu'))
    # model.add(Dense(64, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(actions.shape[0], activation='softmax'))
    model.load_weights('MP_Hyan/introduction.h5')

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

        if threadCamera == True:

            with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
                while self.cap.isOpened():
                    
                    TIMER = int(3) 
                    # Read feed
                    ret, frame = self.cap.read()
                    image, results = self.mediapipe_detection(frame, holistic)
                    self.draw_styled_landmarks(image, results)


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
                        self.draw_styled_landmarks(image, results)
                        
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

                            