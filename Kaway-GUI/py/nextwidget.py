from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

class NextWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Load the UI file
        loadUi("Kaway-GUI\pages\lessons_alphabet_tab.ui", self)
