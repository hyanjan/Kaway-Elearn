# Pyqt import
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets, QtTest
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import warnings
import os
import time
import mediapipe


from db import database


# initialize files and warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
path = os.getcwd()

# Initialize Classes
class Home(QMainWindow):
    def __init__(self):
        super(Home, self).__init__()
        self.setWindowTitle("Kaway - FSL Learning App") 
    
        # Load the ui
        uic.loadUi("Kaway-GUI/pages/login.ui", self)
        self.setFixedSize(1910, 950)

        self.emailfield = self.findChild(QLineEdit, "username")
        self.passwordfield = self.findChild(QLineEdit, "password")
        self.login = self.findChild(QPushButton, "Login")
        self.error = self.findChild(QLabel, "error")
        self.logingif = self.findChild(QLabel, 'Check')
        self.loadinggif = self.findChild(QLabel, 'Check_2')

        self.movie = QMovie(r"Kaway-GUI\linear\login.gif") 
        self.movieloading = QMovie(r"Kaway-GUI\linear\loading.gif")
        self.logingif.setMovie(self.movie)
        self.movie.start()
        self.loadinggif.hide()
        self.error.hide()


        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.clicked.connect(self.loginfunction)

    def loginfunction(self):
        user = self.emailfield.text()
        password = self.passwordfield.text()

        if len(user)==0 or len(password)==0:
            print("Please input all fields.")
            self.error.show()
            self.error.setText("Please input all fields.")

        else:
            if user == 'admin' and password == 'admin':
                self.error.setText("Successfully logged in.")
                self.loadinggif.show()
                self.loadinggif.setMovie(self.movieloading)
                self.movieloading.start() 
                QtTest.QTest.qWait(3000)

                
                from home import Home
                
                print("Button clicked!")
                home = Home(self.widget)
                self.widget.addWidget(home)
                self.widget.setCurrentWidget(home)
            else:
                self.error.show()
                self.error.setText("Invalid username or password")



# initialize the app
app = QApplication(sys.argv)
MainWindowApp = Home()
MainWindowApp.widget = QStackedWidget()
MainWindowApp.widget.addWidget(MainWindowApp)
MainWindowApp.widget.show()
sys.exit(app.exec_())