# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interfacexUKuVm.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 700)
        MainWindow.setStyleSheet(u"\n"
"background-color: rgb(1, 37, 55);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.MainBar = QWidget(self.centralwidget)
        self.MainBar.setObjectName(u"MainBar")
        self.MainBar.setGeometry(QRect(30, 20, 1141, 651))
        self.MainBar.setStyleSheet(u"")
        self.SideTab = QWidget(self.MainBar)
        self.SideTab.setObjectName(u"SideTab")
        self.SideTab.setGeometry(QRect(0, 0, 281, 651))
        self.SideTabFrame = QFrame(self.SideTab)
        self.SideTabFrame.setObjectName(u"SideTabFrame")
        self.SideTabFrame.setGeometry(QRect(0, 0, 291, 651))
        self.SideTabFrame.setStyleSheet(u"background-color: rgb(33, 158, 188);\n"
"border-top-left-radius: 32px;\n"
"border-bottom-left-radius: 32px;")
        self.SideTabFrame.setFrameShape(QFrame.StyledPanel)
        self.SideTabFrame.setFrameShadow(QFrame.Raised)
        self.Settings = QPushButton(self.SideTabFrame)
        self.Settings.setObjectName(u"Settings")
        self.Settings.setGeometry(QRect(50, 550, 191, 41))
        font = QFont()
        font.setFamily(u"Inter")
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.Settings.setFont(font)
        self.Settings.setStyleSheet(u"color:rgb(255, 255, 255)")
        icon = QIcon()
        icon.addFile(u"../../../AppData/Local/Programs/Python/Python311/Lib/site-packages/qt6_applications/Qt/bin/setting-3.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Settings.setIcon(icon)
        self.Settings.setIconSize(QSize(35, 35))
        self.verticalLayoutWidget = QWidget(self.SideTabFrame)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(-1, 150, 281, 341))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.Home = QPushButton(self.verticalLayoutWidget)
        self.Home.setObjectName(u"Home")
        self.Home.setFont(font)
        self.Home.setLayoutDirection(Qt.LeftToRight)
        self.Home.setAutoFillBackground(False)
        self.Home.setStyleSheet(u"color:rgb(255, 255, 255)")
        icon1 = QIcon()
        icon1.addFile(u"../../../AppData/Local/Programs/Python/Python311/Lib/site-packages/qt6_applications/Qt/bin/element-3.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Home.setIcon(icon1)
        self.Home.setIconSize(QSize(30, 30))

        self.verticalLayout.addWidget(self.Home)

        self.Lessons = QPushButton(self.verticalLayoutWidget)
        self.Lessons.setObjectName(u"Lessons")
        self.Lessons.setFont(font)
        self.Lessons.setStyleSheet(u"color:rgb(255, 255, 255)")
        icon2 = QIcon()
        icon2.addFile(u"../../../AppData/Local/Programs/Python/Python311/Lib/site-packages/qt6_applications/Qt/bin/note-2.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Lessons.setIcon(icon2)
        self.Lessons.setIconSize(QSize(40, 40))

        self.verticalLayout.addWidget(self.Lessons)

        self.Profile = QPushButton(self.verticalLayoutWidget)
        self.Profile.setObjectName(u"Profile")
        self.Profile.setFont(font)
        self.Profile.setStyleSheet(u"color:rgb(255, 255, 255)")
        icon3 = QIcon()
        icon3.addFile(u"../../../AppData/Local/Programs/Python/Python311/Lib/site-packages/qt6_applications/Qt/bin/user-square.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Profile.setIcon(icon3)
        self.Profile.setIconSize(QSize(35, 35))

        self.verticalLayout.addWidget(self.Profile)

        self.Kaway = QLabel(self.SideTabFrame)
        self.Kaway.setObjectName(u"Kaway")
        self.Kaway.setGeometry(QRect(50, 30, 221, 71))
        font1 = QFont()
        font1.setFamily(u"Poppins")
        font1.setPointSize(36)
        font1.setBold(True)
        font1.setWeight(75)
        self.Kaway.setFont(font1)
        self.Kaway.setStyleSheet(u"color:rgb(255, 255, 255)")
        self.Period = QLabel(self.SideTabFrame)
        self.Period.setObjectName(u"Period")
        self.Period.setGeometry(QRect(220, 40, 49, 61))
        self.Period.setFont(font1)
        self.Period.setStyleSheet(u"color: rgb(255, 124, 93);")
        self.RightContainer = QWidget(self.MainBar)
        self.RightContainer.setObjectName(u"RightContainer")
        self.RightContainer.setGeometry(QRect(279, -1, 861, 651))
        self.frame = QFrame(self.RightContainer)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(40, 450, 791, 81))
        self.frame.setStyleSheet(u"background-color: rgb(82, 126, 147);\n"
"border-radius: 32px")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame_2 = QFrame(self.RightContainer)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(30, 170, 811, 331))
        self.frame_2.setStyleSheet(u"background-color: rgb(103, 153, 176);\n"
"border-radius: 32px")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(390, 280, 31, 41))
        font2 = QFont()
        font2.setFamily(u"Inter")
        font2.setPointSize(28)
        font2.setBold(True)
        font2.setWeight(75)
        self.label_2.setFont(font2)
        self.label_2.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.frame_3 = QFrame(self.RightContainer)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(20, 120, 831, 321))
        self.frame_3.setStyleSheet(u"background-color: rgb(142, 202, 230);\n"
"border-radius: 32px\n"
"")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.frame_4 = QFrame(self.RightContainer)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setGeometry(QRect(20, 540, 831, 101))
        self.frame_4.setStyleSheet(u"background-color: rgb(142, 202, 230);\n"
"border-radius: 32px\n"
"")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(230, 0, 51, 51))
        self.label_3.setFont(font2)
        self.label_3.setStyleSheet(u"color: rgb(0, 255, 0);")
        self.mainframe = QFrame(self.RightContainer)
        self.mainframe.setObjectName(u"mainframe")
        self.mainframe.setGeometry(QRect(0, 0, 861, 651))
        self.mainframe.setStyleSheet(u"background-color: rgb(3, 72, 106);\n"
"border-top-right-radius: 32px;\n"
"border-bottom-right-radius: 32px;")
        self.mainframe.setFrameShape(QFrame.StyledPanel)
        self.mainframe.setFrameShadow(QFrame.Raised)
        self.verticalLayoutWidget_2 = QWidget(self.mainframe)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(20, 10, 325, 101))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.Module = QLabel(self.verticalLayoutWidget_2)
        self.Module.setObjectName(u"Module")
        font3 = QFont()
        font3.setFamily(u"Inter")
        font3.setPointSize(32)
        font3.setBold(True)
        font3.setWeight(75)
        self.Module.setFont(font3)
        self.Module.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.verticalLayout_2.addWidget(self.Module)

        self.subtopic = QLabel(self.verticalLayoutWidget_2)
        self.subtopic.setObjectName(u"subtopic")
        self.subtopic.setFont(font)
        self.subtopic.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.verticalLayout_2.addWidget(self.subtopic)

        self.pushButton = QPushButton(self.mainframe)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(760, 40, 61, 61))
        self.pushButton.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(33, 158, 188);\n"
"    border-radius: 30px;\n"
"    }\n"
"")
        icon4 = QIcon()
        icon4.addFile(u"../../../AppData/Local/Programs/Python/Python311/Lib/site-packages/qt6_applications/Qt/bin/notification-bing.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(icon4)
        self.pushButton.setIconSize(QSize(40, 40))
        self.label = QLabel(self.mainframe)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(810, 30, 41, 41))
        font4 = QFont()
        font4.setFamily(u"Inter")
        font4.setPointSize(16)
        font4.setBold(True)
        font4.setWeight(75)
        self.label.setFont(font4)
        self.label.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(251, 133, 0);\n"
"    border-radius: 20px;\n"
"  ")
        self.label.setAlignment(Qt.AlignCenter)
        self.mainframe.raise_()
        self.frame.raise_()
        self.frame_2.raise_()
        self.frame_3.raise_()
        self.frame_4.raise_()
        self.MainFrame = QFrame(self.MainBar)
        self.MainFrame.setObjectName(u"MainFrame")
        self.MainFrame.setGeometry(QRect(0, 0, 1141, 651))
        self.MainFrame.setStyleSheet(u"background-color: rgb(2, 48, 71);\n"
"border-radius: 32px\n"
"")
        self.MainFrame.setFrameShape(QFrame.StyledPanel)
        self.MainFrame.setFrameShadow(QFrame.Raised)
        self.MainFrame.raise_()
        self.RightContainer.raise_()
        self.SideTab.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.Settings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.Home.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.Lessons.setText(QCoreApplication.translate("MainWindow", u"Lessons", None))
        self.Profile.setText(QCoreApplication.translate("MainWindow", u"Profile", None))
        self.Kaway.setText(QCoreApplication.translate("MainWindow", u"Kaway", None))
        self.Period.setText(QCoreApplication.translate("MainWindow", u".", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"A", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"A", None))
        self.Module.setText(QCoreApplication.translate("MainWindow", u"Module 1:", None))
        self.subtopic.setText(QCoreApplication.translate("MainWindow", u"Subtopic 1: Letters", None))
        self.pushButton.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"1", None))
    # retranslateUi

