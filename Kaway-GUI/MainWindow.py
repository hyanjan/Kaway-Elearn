from PyQt5.QtWidgets import QApplication,QMainWindow, QWidget, QFrame, QLabel, QPushButton, QVBoxLayout, QStatusBar
from PyQt5 import uic
import sys
import warnings
import os

warnings.filterwarnings("ignore", category=DeprecationWarning) 
path = "C:/Users/hyanx/Documents/Thesis/Kaway-GUI/"
os.chdir(path)


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        #Load the ui
        uic.loadUi("interface.ui", self)

        #show app
        self.show()

#initialize the app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()

