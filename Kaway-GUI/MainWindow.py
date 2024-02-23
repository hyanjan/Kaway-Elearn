# Pyqt import
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFrame, QLabel, QPushButton, QVBoxLayout, QStatusBar
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
import sys
import warnings
import os
import cv2

# initialize files and warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
path = "C:/Users/hyanx/Documents/Thesis/Kaway-GUI/"
os.chdir(path)


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load the ui
        uic.loadUi("interface.ui", self)

        # Define the widgets here
        self.HomeButton = self.findChild(QPushButton, "Home")
        self.cameraFrame = self.findChild(QLabel, "CameraFrame")

        # Define what widgets do
        self.HomeButton.clicked.connect(self.startCamera)

        # Instance variable for capturing camera frames
        self.cap = None

        # Show app
        self.show()

    def startCamera(self):
        self.cap = cv2.VideoCapture(1)  # Open the camera(value depends on camera used, 0 for integrated camera. Check device list to confirm)
        if not self.cap.isOpened():
            print("Error: Couldn't open camera.")
            return

        # Set camera resolution (adjust as needed)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Set up timer to read frames and update GUI
        timer = QTimer(self)
        timer.timeout.connect(self.updateFrame)
        timer.start(1000 // 40)  # Read frames every 33 ms (30 fps)
    
    def updateFrame(self):
        ret, frame = self.cap.read()  # Read frame from camera
        if ret:
             # Resize frame
            frame = cv2.resize(frame, (640, 360))  # Adjust the dimensions as needed
            # Convert frame to RGB format
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            
            # Convert RGB image to QImage
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            qImg = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            # Convert QImage to QPixmap to display in QLabel
            pixmap = QPixmap.fromImage(qImg)
            self.cameraFrame.setPixmap(pixmap)


# initialize the app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
