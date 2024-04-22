import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QThread, Qt, pyqtSignal

class WebcamThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def run(self):
        cap = cv2.VideoCapture(1)
        while True:
            ret, frame = cap.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                p = convert_to_qt_format.scaled(640, 480, Qt.KeepAspectRatio)
                self.change_pixmap_signal.emit(p)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        lay = QVBoxLayout(self.central_widget)
        self.label = QLabel(self)
        lay.addWidget(self.label)

        self.thread = WebcamThread(self)
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    def closeEvent(self, event):
        self.thread.quit()
        self.thread.wait()

    def update_image(self, img):
        self.label.setPixmap(QPixmap.fromImage(img))

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.setWindowTitle('Webcam Viewer')
    win.setGeometry(100, 100, 640, 480)
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
