import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStackedWidget
from PyQt5.uic import loadUi
from nextwidget import NextWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")

        # Load the UI file
        loadUi("Kaway-GUI\pages\lessonstab.ui", self)

        # Create a stacked widget
        self.stacked_widget = QStackedWidget(self.centralwidget)

        # Create pages
        self.page1 = QWidget()
        self.page1_layout = QVBoxLayout(self.page1)
        self.pushButton = QPushButton("Go to Next Page")
        self.page1_layout.addWidget(self.pushButton)
        self.pushButton.clicked.connect(self.go_to_next_page)
        self.stacked_widget.addWidget(self.page1)

        # Show the main window
        self.show()

    def go_to_next_page(self):
        self.next_widget = NextWidget()
        self.stacked_widget.addWidget(self.next_widget)
        self.stacked_widget.setCurrentWidget(self.next_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
