# Pyqt import
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets, QtTest
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
import sys
import warnings
import os
import mediapipe as mp

# initialize files and warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
path = os.getcwd()

# Initialize Classes
class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
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

        # Setup background music
        self.setup_background_music()


    def setup_background_music(self):
        # Create a QMediaPlayer object
        self.mediaPlayer = QMediaPlayer()
        
        # Create a QMediaPlaylist object
        self.playlist = QMediaPlaylist()
        
        # Add a music file to the playlist
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile("Kaway-GUI/audio/music.mp3")))
        
        # Set the playlist to loop
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
        
        # Set the playlist to the media player
        self.mediaPlayer.setPlaylist(self.playlist)
        
        # Set volume (0 to 100)
        self.mediaPlayer.setVolume(50)
        
        # Play the music
        self.mediaPlayer.play()

    def setVolume(self, volume):
        # Set the volume of the media player
        self.mediaPlayer.setVolume(volume)
        print(f"Volume set to: {volume}")
        

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
MainWindowApp = Login()
MainWindowApp.widget = QStackedWidget()
MainWindowApp.widget.setWindowTitle("Kaway - FSL Learning App") 
MainWindowApp.widget.addWidget(MainWindowApp)
MainWindowApp.widget.show()
sys.exit(app.exec_())