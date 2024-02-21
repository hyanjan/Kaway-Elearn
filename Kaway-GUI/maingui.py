import sys
import os

from PyQt5.uic import loadUi
from PySide2 import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

from M1S1_test import *

#MAIN WINDOW CLASS
class Ui_Dialog(QDialog):
    def __init__(self):
        super(Ui_Dialog, self).__init__()
        loadUi("C:/Users/hyanx/Documents/Thesis/Kaway-GUI/interface.ui", self)

#EXECUTE aPP
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_Dialog()
    ui.show()
    sys.exit(app.exec_())
    
