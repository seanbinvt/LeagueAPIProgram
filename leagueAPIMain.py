'''
NOTE: In keys.json is the my working API key as of submission. Every 24hrs the key will be deactived and a new
key will be required. If I am needed to send an API key when you review the assignment I will do so. 
- bsb11100@vsc.edu


Test Cases:
Account exists + 7 day history: 'mccloudi' (as of date)
Account exists + NO 7 day history: 'seantehscrub' (as of date)
Account doesn't exist + NO 7 day history: 'cdshncdsacndsa' (random chars)

Searching from one to the next shows adaptibility of GUI player window objects
regardless of revious search results.
    Ex: A search for a nonexistant account will make almost all labels cleared and account exists+ 7 day history
    will have to make them reappear. 
'''


import json
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
import urllib
import time

from threading import Thread

from PlayerInfo import PlayerInfo
import RequestMatchlist.requestMatchlists as RequestMatchlists

# Library for ease of Riot Game API use.
# https://riot-watcher.readthedocs.io/en/latest/
from riotwatcher import RiotWatcher, ApiError

api = RiotWatcher(
    json.load(open("keys.json", encoding="UTF-8"))['apiKey'])

# Creates a JSON object with all champion names and other information given in championID.json
# Credit of json file to https://github.com/ngryman/lol-champions/blob/master/champions.json - By ngryman
with open("./Information/championID.json", encoding="UTF-8") as f:
    championsInfo = json.load(f)

class Ui_MainWindow(object):
    '''
    Below setupUi and retranslateUi are copy and pasted code from turning the untitled.ui file created in
    the PyQt5 Designer application.

    _x indicates what window the given object is for. example: 
        Player One Window: 'rankLabel'
        Player Two Window: 'rankLabel_2'
        Player Three Window: 'rankLabel_3'
        Player Four WindowL 'rankLabel_4'
    All GUI objects within player information windows follows this naming scheme

    Each player information window has objects: rankLabel(_x), rankWinLabel(_x), rankLossLabel(_x), staticLabel(_x), ovrWinLossLabel(_x),
    mostPlayedLabel(_x), champIcon(_x), topWLLabel(_x), jungWLLabel(_x), midWLLabel(_x), adcWLLabel(_x), suppWLLabel(_x)
    '''
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(668, 638)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        MainWindow.setPalette(palette)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lolImage = QtWidgets.QLabel(self.centralwidget)
        self.lolImage.setGeometry(QtCore.QRect(210, 0, 251, 101))
        self.lolImage.setScaledContents(True)
        self.lolImage.setObjectName("lolImage")
        self.inputsCanvas = QtWidgets.QTabWidget(self.centralwidget)
        self.inputsCanvas.setGeometry(QtCore.QRect(20, 230, 631, 341))
        self.inputsCanvas.setObjectName("inputsCanvas")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.tab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 631, 82))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.rankLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.rankLabel.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.rankLabel.setFont(font)
        self.rankLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.rankLabel.setObjectName("rankLabel")
        self.verticalLayout.addWidget(self.rankLabel)
        self.rankWinLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.rankWinLabel.setFont(font)
        self.rankWinLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.rankWinLabel.setObjectName("rankWinLabel")
        self.verticalLayout.addWidget(self.rankWinLabel)
        self.rankLossLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.rankLossLabel.setFont(font)
        self.rankLossLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.rankLossLabel.setObjectName("rankLossLabel")
        self.verticalLayout.addWidget(self.rankLossLabel)
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.tab)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(10, 130, 301, 71))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.statsLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.statsLayout.setContentsMargins(0, 0, 0, 0)
        self.statsLayout.setObjectName("statsLayout")
        self.ovrWinLossLabel = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.ovrWinLossLabel.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.ovrWinLossLabel.setFont(font)
        self.ovrWinLossLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.ovrWinLossLabel.setObjectName("ovrWinLossLabel")
        self.statsLayout.addWidget(self.ovrWinLossLabel)
        self.mostPlayedLabel = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.mostPlayedLabel.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.mostPlayedLabel.setFont(font)
        self.mostPlayedLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.mostPlayedLabel.setObjectName("mostPlayedLabel")
        self.statsLayout.addWidget(self.mostPlayedLabel)
        self.staticLabel = QtWidgets.QLabel(self.tab)
        self.staticLabel.setEnabled(True)
        self.staticLabel.setGeometry(QtCore.QRect(120, 80, 391, 32))
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.staticLabel.setFont(font)
        self.staticLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.staticLabel.setObjectName("staticLabel")
        self.champIcon = QtWidgets.QLabel(self.tab)
        self.champIcon.setGeometry(QtCore.QRect(110, 210, 75, 75))
        self.champIcon.setText("")
        self.champIcon.setObjectName("champIcon")
        self.verticalLayoutWidget_6 = QtWidgets.QWidget(self.tab)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(334, 120, 291, 131))
        self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
        self.laneLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
        self.laneLayout.setContentsMargins(0, 0, 0, 0)
        self.laneLayout.setObjectName("laneLayout")
        self.topWLLabel = QtWidgets.QLabel(self.verticalLayoutWidget_6)
        self.topWLLabel.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.topWLLabel.setFont(font)
        self.topWLLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.topWLLabel.setObjectName("topWLLabel")
        self.laneLayout.addWidget(self.topWLLabel)
        self.jungWLLabel = QtWidgets.QLabel(self.verticalLayoutWidget_6)
        self.jungWLLabel.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.jungWLLabel.setFont(font)
        self.jungWLLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.jungWLLabel.setObjectName("jungWLLabel")
        self.laneLayout.addWidget(self.jungWLLabel)
        self.midWLLabel = QtWidgets.QLabel(self.verticalLayoutWidget_6)
        self.midWLLabel.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.midWLLabel.setFont(font)
        self.midWLLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.midWLLabel.setObjectName("midWLLabel")
        self.laneLayout.addWidget(self.midWLLabel)
        self.adcWLLabel = QtWidgets.QLabel(self.verticalLayoutWidget_6)
        self.adcWLLabel.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.adcWLLabel.setFont(font)
        self.adcWLLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.adcWLLabel.setObjectName("adcWLLabel")
        self.laneLayout.addWidget(self.adcWLLabel)
        self.suppWLLabel = QtWidgets.QLabel(self.verticalLayoutWidget_6)
        self.suppWLLabel.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.suppWLLabel.setFont(font)
        self.suppWLLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.suppWLLabel.setObjectName("suppWLLabel")
        self.laneLayout.addWidget(self.suppWLLabel)
        self.inputsCanvas.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.tab_2)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 631, 82))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.rankLabel_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.rankLabel_2.setFont(font)
        self.rankLabel_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.rankLabel_2.setObjectName("rankLabel_2")
        self.verticalLayout_2.addWidget(self.rankLabel_2)
        self.rankWinLabel_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.rankWinLabel_2.setFont(font)
        self.rankWinLabel_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.rankWinLabel_2.setObjectName("rankWinLabel_2")
        self.verticalLayout_2.addWidget(self.rankWinLabel_2)
        self.rankLossLabel_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.rankLossLabel_2.setFont(font)
        self.rankLossLabel_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.rankLossLabel_2.setObjectName("rankLossLabel_2")
        self.verticalLayout_2.addWidget(self.rankLossLabel_2)
        self.staticLabel_2 = QtWidgets.QLabel(self.tab_2)
        self.staticLabel_2.setEnabled(True)
        self.staticLabel_2.setGeometry(QtCore.QRect(120, 80, 391, 32))
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.staticLabel_2.setFont(font)
        self.staticLabel_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.staticLabel_2.setObjectName("staticLabel_2")
        self.verticalLayoutWidget_7 = QtWidgets.QWidget(self.tab_2)
        self.verticalLayoutWidget_7.setGeometry(QtCore.QRect(10, 130, 301, 71))
        self.verticalLayoutWidget_7.setObjectName("verticalLayoutWidget_7")
        self.statsLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_7)
        self.statsLayout_2.setContentsMargins(0, 0, 0, 0)
        self.statsLayout_2.setObjectName("statsLayout_2")
        self.ovrWinLossLabel_2 = QtWidgets.QLabel(self.verticalLayoutWidget_7)
        self.ovrWinLossLabel_2.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.ovrWinLossLabel_2.setFont(font)
        self.ovrWinLossLabel_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.ovrWinLossLabel_2.setObjectName("ovrWinLossLabel_2")
        self.statsLayout_2.addWidget(self.ovrWinLossLabel_2)
        self.mostPlayedLabel_2 = QtWidgets.QLabel(self.verticalLayoutWidget_7)
        self.mostPlayedLabel_2.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.mostPlayedLabel_2.setFont(font)
        self.mostPlayedLabel_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.mostPlayedLabel_2.setObjectName("mostPlayedLabel_2")
        self.statsLayout_2.addWidget(self.mostPlayedLabel_2)
        self.verticalLayoutWidget_8 = QtWidgets.QWidget(self.tab_2)
        self.verticalLayoutWidget_8.setGeometry(QtCore.QRect(334, 120, 291, 131))
        self.verticalLayoutWidget_8.setObjectName("verticalLayoutWidget_8")
        self.laneLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_8)
        self.laneLayout_2.setContentsMargins(0, 0, 0, 0)
        self.laneLayout_2.setObjectName("laneLayout_2")
        self.topWLLabel_2 = QtWidgets.QLabel(self.verticalLayoutWidget_8)
        self.topWLLabel_2.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.topWLLabel_2.setFont(font)
        self.topWLLabel_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.topWLLabel_2.setObjectName("topWLLabel_2")
        self.laneLayout_2.addWidget(self.topWLLabel_2)
        self.jungWLLabel_2 = QtWidgets.QLabel(self.verticalLayoutWidget_8)
        self.jungWLLabel_2.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.jungWLLabel_2.setFont(font)
        self.jungWLLabel_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.jungWLLabel_2.setObjectName("jungWLLabel_2")
        self.laneLayout_2.addWidget(self.jungWLLabel_2)
        self.midWLLabel_2 = QtWidgets.QLabel(self.verticalLayoutWidget_8)
        self.midWLLabel_2.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.midWLLabel_2.setFont(font)
        self.midWLLabel_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.midWLLabel_2.setObjectName("midWLLabel_2")
        self.laneLayout_2.addWidget(self.midWLLabel_2)
        self.adcWLLabel_2 = QtWidgets.QLabel(self.verticalLayoutWidget_8)
        self.adcWLLabel_2.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.adcWLLabel_2.setFont(font)
        self.adcWLLabel_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.adcWLLabel_2.setObjectName("adcWLLabel_2")
        self.laneLayout_2.addWidget(self.adcWLLabel_2)
        self.suppWLLabel_2 = QtWidgets.QLabel(self.verticalLayoutWidget_8)
        self.suppWLLabel_2.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.suppWLLabel_2.setFont(font)
        self.suppWLLabel_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.suppWLLabel_2.setObjectName("suppWLLabel_2")
        self.laneLayout_2.addWidget(self.suppWLLabel_2)
        self.champIcon_2 = QtWidgets.QLabel(self.tab_2)
        self.champIcon_2.setGeometry(QtCore.QRect(110, 210, 75, 75))
        self.champIcon_2.setText("")
        self.champIcon_2.setObjectName("champIcon_2")
        self.inputsCanvas.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.tab_3)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 631, 82))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.rankLabel_3 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.rankLabel_3.setFont(font)
        self.rankLabel_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.rankLabel_3.setObjectName("rankLabel_3")
        self.verticalLayout_3.addWidget(self.rankLabel_3)
        self.rankWinLabel_3 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.rankWinLabel_3.setFont(font)
        self.rankWinLabel_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.rankWinLabel_3.setObjectName("rankWinLabel_3")
        self.verticalLayout_3.addWidget(self.rankWinLabel_3)
        self.rankLossLabel_3 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.rankLossLabel_3.setFont(font)
        self.rankLossLabel_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.rankLossLabel_3.setObjectName("rankLossLabel_3")
        self.verticalLayout_3.addWidget(self.rankLossLabel_3)
        self.verticalLayoutWidget_9 = QtWidgets.QWidget(self.tab_3)
        self.verticalLayoutWidget_9.setGeometry(QtCore.QRect(334, 120, 291, 131))
        self.verticalLayoutWidget_9.setObjectName("verticalLayoutWidget_9")
        self.laneLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_9)
        self.laneLayout_3.setContentsMargins(0, 0, 0, 0)
        self.laneLayout_3.setObjectName("laneLayout_3")
        self.topWLLabel_3 = QtWidgets.QLabel(self.verticalLayoutWidget_9)
        self.topWLLabel_3.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.topWLLabel_3.setFont(font)
        self.topWLLabel_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.topWLLabel_3.setObjectName("topWLLabel_3")
        self.laneLayout_3.addWidget(self.topWLLabel_3)
        self.jungWLLabel_3 = QtWidgets.QLabel(self.verticalLayoutWidget_9)
        self.jungWLLabel_3.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.jungWLLabel_3.setFont(font)
        self.jungWLLabel_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.jungWLLabel_3.setObjectName("jungWLLabel_3")
        self.laneLayout_3.addWidget(self.jungWLLabel_3)
        self.midWLLabel_3 = QtWidgets.QLabel(self.verticalLayoutWidget_9)
        self.midWLLabel_3.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.midWLLabel_3.setFont(font)
        self.midWLLabel_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.midWLLabel_3.setObjectName("midWLLabel_3")
        self.laneLayout_3.addWidget(self.midWLLabel_3)
        self.adcWLLabel_3 = QtWidgets.QLabel(self.verticalLayoutWidget_9)
        self.adcWLLabel_3.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.adcWLLabel_3.setFont(font)
        self.adcWLLabel_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.adcWLLabel_3.setObjectName("adcWLLabel_3")
        self.laneLayout_3.addWidget(self.adcWLLabel_3)
        self.suppWLLabel_3 = QtWidgets.QLabel(self.verticalLayoutWidget_9)
        self.suppWLLabel_3.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.suppWLLabel_3.setFont(font)
        self.suppWLLabel_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.suppWLLabel_3.setObjectName("suppWLLabel_3")
        self.laneLayout_3.addWidget(self.suppWLLabel_3)
        self.verticalLayoutWidget_11 = QtWidgets.QWidget(self.tab_3)
        self.verticalLayoutWidget_11.setGeometry(QtCore.QRect(10, 130, 301, 71))
        self.verticalLayoutWidget_11.setObjectName("verticalLayoutWidget_11")
        self.statsLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_11)
        self.statsLayout_3.setContentsMargins(0, 0, 0, 0)
        self.statsLayout_3.setObjectName("statsLayout_3")
        self.ovrWinLossLabel_3 = QtWidgets.QLabel(self.verticalLayoutWidget_11)
        self.ovrWinLossLabel_3.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.ovrWinLossLabel_3.setFont(font)
        self.ovrWinLossLabel_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.ovrWinLossLabel_3.setObjectName("ovrWinLossLabel_3")
        self.statsLayout_3.addWidget(self.ovrWinLossLabel_3)
        self.mostPlayedLabel_3 = QtWidgets.QLabel(self.verticalLayoutWidget_11)
        self.mostPlayedLabel_3.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.mostPlayedLabel_3.setFont(font)
        self.mostPlayedLabel_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.mostPlayedLabel_3.setObjectName("mostPlayedLabel_3")
        self.statsLayout_3.addWidget(self.mostPlayedLabel_3)
        self.staticLabel_3 = QtWidgets.QLabel(self.tab_3)
        self.staticLabel_3.setEnabled(True)
        self.staticLabel_3.setGeometry(QtCore.QRect(120, 80, 391, 32))
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.staticLabel_3.setFont(font)
        self.staticLabel_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.staticLabel_3.setObjectName("staticLabel_3")
        self.champIcon_3 = QtWidgets.QLabel(self.tab_3)
        self.champIcon_3.setGeometry(QtCore.QRect(110, 210, 75, 75))
        self.champIcon_3.setText("")
        self.champIcon_3.setObjectName("champIcon_3")
        self.inputsCanvas.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.tab_4)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(0, 0, 631, 82))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.rankLabel_4 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.rankLabel_4.setFont(font)
        self.rankLabel_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.rankLabel_4.setObjectName("rankLabel_4")
        self.verticalLayout_4.addWidget(self.rankLabel_4)
        self.rankWinLabel_4 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.rankWinLabel_4.setFont(font)
        self.rankWinLabel_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.rankWinLabel_4.setObjectName("rankWinLabel_4")
        self.verticalLayout_4.addWidget(self.rankWinLabel_4)
        self.rankLossLabel_4 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.rankLossLabel_4.setFont(font)
        self.rankLossLabel_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.rankLossLabel_4.setObjectName("rankLossLabel_4")
        self.verticalLayout_4.addWidget(self.rankLossLabel_4)
        self.verticalLayoutWidget_10 = QtWidgets.QWidget(self.tab_4)
        self.verticalLayoutWidget_10.setGeometry(QtCore.QRect(334, 120, 291, 131))
        self.verticalLayoutWidget_10.setObjectName("verticalLayoutWidget_10")
        self.laneLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_10)
        self.laneLayout_4.setContentsMargins(0, 0, 0, 0)
        self.laneLayout_4.setObjectName("laneLayout_4")
        self.topWLLabel_4 = QtWidgets.QLabel(self.verticalLayoutWidget_10)
        self.topWLLabel_4.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.topWLLabel_4.setFont(font)
        self.topWLLabel_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.topWLLabel_4.setObjectName("topWLLabel_4")
        self.laneLayout_4.addWidget(self.topWLLabel_4)
        self.jungWLLabel_4 = QtWidgets.QLabel(self.verticalLayoutWidget_10)
        self.jungWLLabel_4.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.jungWLLabel_4.setFont(font)
        self.jungWLLabel_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.jungWLLabel_4.setObjectName("jungWLLabel_4")
        self.laneLayout_4.addWidget(self.jungWLLabel_4)
        self.midWLLabel_4 = QtWidgets.QLabel(self.verticalLayoutWidget_10)
        self.midWLLabel_4.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.midWLLabel_4.setFont(font)
        self.midWLLabel_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.midWLLabel_4.setObjectName("midWLLabel_4")
        self.laneLayout_4.addWidget(self.midWLLabel_4)
        self.adcWLLabel_4 = QtWidgets.QLabel(self.verticalLayoutWidget_10)
        self.adcWLLabel_4.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.adcWLLabel_4.setFont(font)
        self.adcWLLabel_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.adcWLLabel_4.setObjectName("adcWLLabel_4")
        self.laneLayout_4.addWidget(self.adcWLLabel_4)
        self.suppWLLabel_4 = QtWidgets.QLabel(self.verticalLayoutWidget_10)
        self.suppWLLabel_4.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.suppWLLabel_4.setFont(font)
        self.suppWLLabel_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.suppWLLabel_4.setObjectName("suppWLLabel_4")
        self.laneLayout_4.addWidget(self.suppWLLabel_4)
        self.verticalLayoutWidget_12 = QtWidgets.QWidget(self.tab_4)
        self.verticalLayoutWidget_12.setGeometry(QtCore.QRect(10, 130, 301, 71))
        self.verticalLayoutWidget_12.setObjectName("verticalLayoutWidget_12")
        self.statsLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_12)
        self.statsLayout_4.setContentsMargins(0, 0, 0, 0)
        self.statsLayout_4.setObjectName("statsLayout_4")
        self.ovrWinLossLabel_4 = QtWidgets.QLabel(self.verticalLayoutWidget_12)
        self.ovrWinLossLabel_4.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.ovrWinLossLabel_4.setFont(font)
        self.ovrWinLossLabel_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.ovrWinLossLabel_4.setObjectName("ovrWinLossLabel_4")
        self.statsLayout_4.addWidget(self.ovrWinLossLabel_4)
        self.mostPlayedLabel_4 = QtWidgets.QLabel(self.verticalLayoutWidget_12)
        self.mostPlayedLabel_4.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.mostPlayedLabel_4.setFont(font)
        self.mostPlayedLabel_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.mostPlayedLabel_4.setObjectName("mostPlayedLabel_4")
        self.statsLayout_4.addWidget(self.mostPlayedLabel_4)
        self.staticLabel_4 = QtWidgets.QLabel(self.tab_4)
        self.staticLabel_4.setEnabled(True)
        self.staticLabel_4.setGeometry(QtCore.QRect(120, 80, 391, 32))
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.staticLabel_4.setFont(font)
        self.staticLabel_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.staticLabel_4.setObjectName("staticLabel_4")
        self.champIcon_4 = QtWidgets.QLabel(self.tab_4)
        self.champIcon_4.setGeometry(QtCore.QRect(110, 210, 75, 75))
        self.champIcon_4.setText("")
        self.champIcon_4.setObjectName("champIcon_4")
        self.inputsCanvas.addTab(self.tab_4, "")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(160, 100, 241, 121))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.summoner1Input = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.summoner1Input.setObjectName("summoner1Input")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.summoner1Input)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.summoner2Input = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.summoner2Input.setObjectName("summoner2Input")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.summoner2Input)
        self.summoner3Input = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.summoner3Input.setObjectName("summoner3Input")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.summoner3Input)
        self.summoner4Input = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.summoner4Input.setObjectName("summoner4Input")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.summoner4Input)
        self.searchButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchButton.setGeometry(QtCore.QRect(410, 140, 91, 31))
        self.searchButton.setStyleSheet("")
        self.searchButton.setObjectName("searchButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.inputsCanvas.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Below is GUI initialization required this is not defined in the UI file.
        MainWindow.setFixedSize(668, 638)

        # This causes "libpng warning: iCCP: known incorrect sRGB profile" warning but works
        # Research on warning shows people saying not to worry about it and that it changes based on compilation
        self.lolImage.setPixmap(QtGui.QPixmap("./Images/lol-logo.png"))

        # Summoner search button click method call
        self.searchButton.clicked.connect(self.clicked)

        # When the application is newly launched, each information tab should be disabled due lack of specified inputs.
        for x in range(0, 4):
            self.inputsCanvas.setTabEnabled(x, False)

        self.playerOneN = None
        self.playerTwoN = None
        self.playerThreeN = None
        self.playerFourN = None
        self._translate = QtCore.QCoreApplication.translate
        
        self.summoner1Input.setStyleSheet("background-color: white")
        self.summoner2Input.setStyleSheet("background-color: white")
        self.summoner3Input.setStyleSheet("background-color: white")
        self.summoner4Input.setStyleSheet("background-color: white")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowIcon(QtGui.QIcon("./Images/tyler1.jpg"))
        MainWindow.setWindowTitle(_translate("MainWindow", "Sean\'s League Program"))
        self.rankLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.rankWinLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.rankLossLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.ovrWinLossLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.mostPlayedLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.staticLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.topWLLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.jungWLLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.midWLLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.adcWLLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.suppWLLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.inputsCanvas.setTabText(self.inputsCanvas.indexOf(self.tab), _translate("MainWindow", "Summoner 1"))
        self.rankLabel_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.rankWinLabel_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.rankLossLabel_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.staticLabel_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.ovrWinLossLabel_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.mostPlayedLabel_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.topWLLabel_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.jungWLLabel_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.midWLLabel_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.adcWLLabel_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.suppWLLabel_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.inputsCanvas.setTabText(self.inputsCanvas.indexOf(self.tab_2), _translate("MainWindow", "Summoner 2"))
        self.rankLabel_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.rankWinLabel_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.rankLossLabel_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.topWLLabel_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.jungWLLabel_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.midWLLabel_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.adcWLLabel_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.suppWLLabel_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.ovrWinLossLabel_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.mostPlayedLabel_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.staticLabel_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.inputsCanvas.setTabText(self.inputsCanvas.indexOf(self.tab_3), _translate("MainWindow", "Summoner 3"))
        self.rankLabel_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.rankWinLabel_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.rankLossLabel_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.topWLLabel_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.jungWLLabel_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.midWLLabel_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.adcWLLabel_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.suppWLLabel_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.ovrWinLossLabel_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.mostPlayedLabel_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.staticLabel_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#146366;\"></span></p></body></html>"))
        self.inputsCanvas.setTabText(self.inputsCanvas.indexOf(self.tab_4), _translate("MainWindow", "Summoner 4"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Summoner #1:</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Summoner #2:</span></p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Summoner #3:</span></p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Summoner #4:</span></p></body></html>"))
        self.searchButton.setText(_translate("MainWindow", "SEARCH"))

    '''
    Method to create information object for summoner 1 and handles the updating of GUI objects.
    '''
    def updateOne(self):
        # Check if the player 1 input box is NULL and
        # check that it isn't trying to search the player it just searched. 
        if self.summoner1Input.text() and self.summoner1Input.text() != self.playerOneN:
            self.playerOneN = self.summoner1Input.text()

            # Create the object to store data for the searched player.
            playerOne = PlayerInfo(self.summoner1Input.text(), 'na1')

            # If there isn't an error with the base API call then proceed with updating GUI objects with
            # player object information
            if not playerOne.error == "init":
                # Allows tab to be clicked now
                self.inputsCanvas.setTabEnabled(0, True)

                # Sets tab title as the inputted searched player name
                self.inputsCanvas.setTabText(self.inputsCanvas.indexOf(
                    self.tab), self._translate("MainWindow", playerOne.name))

                # Setting text for rank
                self.rankLabel.setStyleSheet(
                    "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                self.rankLabel.setText("Rank: "+ playerOne.rank)

                # Setting text for wins
                self.rankWinLabel.setStyleSheet(
                    "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                self.rankWinLabel.setText(
                    "Ranked Season Wins: "+str(playerOne.rankedWins))

                # Setting text for losses
                self.rankLossLabel.setStyleSheet(
                    "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                self.rankLossLabel.setText(
                    "Ranked Season Losses: "+str(playerOne.rankedLosses))

                # If there was no error with retrieving data on the previous 7 days then continue.
                if not playerOne.error == "none":
                    # Set text for the win/loss rate in the past 7 days
                    self.ovrWinLossLabel.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                    overall = "Overall Win/Loss (%): "+str(playerOne.wins)+"/"+str(playerOne.losses) +" ("
                    if playerOne.wins == 0:
                        overall += "0%)"
                    elif playerOne.losses == 0:
                        overall += "100%)"
                    else:
                        overall += str(round((playerOne.wins/(playerOne.wins+playerOne.losses))*100)) + "%)"
                    self.ovrWinLossLabel.setText(overall)

                    # Setting text for last week most played champion and image from championID.json
                    self.mostPlayedLabel.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                    # Iterate through championID.json until correct champion is found
                    # retrieve champion name and champion icon from champion ID
                    for champion in championsInfo:
                        if int(champion['key']) == playerOne.res:
                            # Set text of most played champion
                            self.mostPlayedLabel.setText("Most Played Champion: " + champion['name'].capitalize())
                            # Create sclaed image and update image with icon image URL
                            data = urllib.request.urlopen(champion['icon']).read()
                            image = QtGui.QImage()
                            image.loadFromData(data)
                            self.champIcon.setPixmap(QtGui.QPixmap(image).scaled(64, 64, QtCore.Qt.KeepAspectRatio))
                            break

                    # Setting Top Win/Loss (%)
                    self.topWLLabel.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                    topText = "Top Win/Loss (%): "+str(playerOne.laneWins[0]) + "/" + str(playerOne.laneLoss[0])+ " (" 
                    if playerOne.laneWins[0] == 0:
                        topText += "0%)"
                    elif playerOne.laneLoss[0] == 0:
                        topText += "100%)"
                    else:
                        topText += str(round((playerOne.laneWins[0]/(playerOne.laneWins[0]+playerOne.laneLoss[0]))*100)) + "%)"
                    self.topWLLabel.setText(topText) 

                    # Setting Jungle Win/Loss(%)    
                    self.jungWLLabel.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                    jungText = "Jungle Win/Loss (%): "+str(playerOne.laneWins[1]) + "/" + str(playerOne.laneLoss[1])+ " (" 
                    if playerOne.laneWins[1] == 0:
                        jungText += "0%)"
                    elif playerOne.laneLoss[1] == 0:
                        jungText += "100%)"
                    else:
                        jungText += str(round((playerOne.laneWins[1]/(playerOne.laneWins[1]+playerOne.laneLoss[1]))*100)) + "%)"
                    self.jungWLLabel.setText(jungText) 

                    # Setting Mid Win/Loss (%)
                    self.midWLLabel.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                    midText = "Mid Win/Loss (%): "+str(playerOne.laneWins[2]) + "/" + str(playerOne.laneLoss[2])+ " (" 
                    if playerOne.laneWins[2] == 0:
                        midText += "0%)"
                    elif playerOne.laneLoss[2] == 0:
                        midText += "100%)"
                    else:
                        midText += str(round((playerOne.laneWins[2]/(playerOne.laneWins[2]+playerOne.laneLoss[2]))*100)) + "%)"
                    self.midWLLabel.setText(midText) 

                    # Setting ADC Win/Loss (%)
                    self.adcWLLabel.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                    adcText = "ADC Win/Loss (%): "+str(playerOne.laneWins[3]) + "/" + str(playerOne.laneLoss[3])+ " (" 
                    if playerOne.laneWins[3] == 0:
                        adcText += "0%)"
                    elif playerOne.laneLoss[3] == 0:
                        adcText += "100%)"
                    else:
                        adcText += str(round((playerOne.laneWins[3]/(playerOne.laneWins[3]+playerOne.laneLoss[3]))*100)) + "%)"
                    self.adcWLLabel.setText(adcText) 

                    # Setting Support Win/Loss (%)
                    self.suppWLLabel.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                    suppText = "Support Win/Loss (%): "+str(playerOne.laneWins[4]) + "/" + str(playerOne.laneLoss[4])+ " (" 
                    if playerOne.laneWins[4] == 0:
                        suppText += "0%)"
                    elif playerOne.laneLoss[4] == 0:
                        suppText += "100%)"
                    else:
                        suppText += str(round((playerOne.laneWins[4]/(playerOne.laneWins[4]+playerOne.laneLoss[4]))*100)) + "%)"
                    self.suppWLLabel.setText(suppText)

                    # Sets the static variable again in case it was changed to "no games in last week"
                    # during a previous search using this window
                    self.staticLabel.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#FF0000; font-weight:600;")
                    self.staticLabel.setText(
                        "~~ Last Week Stats (Max 100 Games) ~~")
                # If there was an error retrieving JSON from the past 7 days API request
                # then clear all 7 day required GUI objects and set staticLabel to display error.
                else:
                    self.staticLabel.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#FF0000; font-weight:600;")
                    self.staticLabel.setText(
                        "~~ This player has no games in the last week ~~")

                    self.ovrWinLossLabel.clear()
                    self.mostPlayedLabel.clear()
                    self.topWLLabel.clear()
                    self.jungWLLabel.clear()
                    self.midWLLabel.clear()
                    self.adcWLLabel.clear()
                    self.suppWLLabel.clear()
                    self.champIcon.clear()
            # If there was an error in retrieving JSON from the player lookup by name API request
            # then clear all GUI objects except the first to and display error message
            # -- Either the API is down or the searched player doesn't exist.
            else:
                self.rankLabel.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#FF0000; font-weight:600;")
                self.rankLabel.setText(
                        "The given player username doesn't exist")
                self.rankWinLabel.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#FF0000; font-weight:600;")
                self.rankWinLabel.setText("OR the Riot Games API is experiencing errors.")
                self.rankLossLabel.clear()
                self.staticLabel.clear()
                self.ovrWinLossLabel.clear()
                self.mostPlayedLabel.clear()
                self.topWLLabel.clear()
                self.jungWLLabel.clear()
                self.midWLLabel.clear()
                self.adcWLLabel.clear()
                self.suppWLLabel.clear()
                self.champIcon.clear()
                self.inputsCanvas.setTabText(0, playerOne.name)
                self.inputsCanvas.setTabEnabled(0, True)
        # If the respective searchbox is empty then deactivate tab and rename the tab title.
        elif not self.summoner1Input.text():
            self.inputsCanvas.setTabText(0, "-")
            self.inputsCanvas.setTabEnabled(0, False)

    '''
    Method to create information object for summoner 2 and handles the updating of GUI objects.
    '''
    def updateTwo(self):
        # If the user isn't trying to search the same player and the input isn't empty
        if self.summoner2Input.text() and self.summoner2Input.text() != self.playerTwoN:
            self.playerTwoN = self.summoner2Input.text()

            playerTwo = PlayerInfo(self.summoner2Input.text(), 'na1')
            # If there was information found on the player
            if not playerTwo.error == 'init':
                self.inputsCanvas.setTabText(self.inputsCanvas.indexOf(
                    self.tab_2), self._translate("MainWindow", playerTwo.name))

                # Setting text for rank
                self.rankLabel_2.setStyleSheet(
                    "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                self.rankLabel_2.setText("Rank: "+ playerTwo.rank)
                # Setting text for wins
                self.rankWinLabel_2.setStyleSheet(
                    "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                self.rankWinLabel_2.setText(
                    "Ranked Season Wins: "+str(playerTwo.rankedWins))
                # Setting text for losses
                self.rankLossLabel_2.setStyleSheet(
                    "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                self.rankLossLabel_2.setText(
                    "Ranked Season Losses: "+str(playerTwo.rankedLosses))
                if not playerTwo.error == "none":
                    # Setting text for last week win rate
                    self.ovrWinLossLabel_2.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                    overall = "Overall Win/Loss (%): "+str(playerTwo.wins)+"/"+str(playerTwo.losses) +" ("
                    if playerTwo.wins == 0:
                        overall += "0%)"
                    elif playerTwo.losses == 0:
                        overall += "100%)"
                    else:
                        overall += str(round((playerTwo.wins/(playerTwo.wins+playerTwo.losses))*100)) + "%)"
                    self.ovrWinLossLabel_2.setText(overall)
                    # Setting text for last week most played champion and image
                    self.mostPlayedLabel_2.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                    for champion in championsInfo:
                        if int(champion['key']) == playerTwo.res:
                            self.mostPlayedLabel_2.setText("Most Played Champion: " + champion['name'].capitalize())
                            data = urllib.request.urlopen(champion['icon']).read()
                            image = QtGui.QImage()
                            image.loadFromData(data)
                            self.champIcon_2.setPixmap(QtGui.QPixmap(image).scaled(64, 64, QtCore.Qt.KeepAspectRatio))
                            break

                    # Setting Top Win/Loss (%)
                    self.topWLLabel_2.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                    topText = "Top Win/Loss (%): "+str(playerTwo.laneWins[0]) + "/" + str(playerTwo.laneLoss[0])+ " (" 
                    if playerTwo.laneWins[0] == 0:
                        topText += "0%)"
                    elif playerTwo.laneLoss[0] == 0:
                        topText += "100%)"
                    else:
                        topText += str(round((playerTwo.laneWins[0]/(playerTwo.laneWins[0]+playerTwo.laneLoss[0]))*100)) + "%)"
                    self.topWLLabel_2.setText(topText) 

                    # Setting Jungle Win/Loss(%)    
                    self.jungWLLabel_2.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                    jungText = "Jungle Win/Loss (%): "+str(playerTwo.laneWins[1]) + "/" + str(playerTwo.laneLoss[1])+ " (" 
                    if playerTwo.laneWins[1] == 0:
                        jungText += "0%)"
                    elif playerTwo.laneLoss[1] == 0:
                        jungText += "100%)"
                    else:
                        jungText += str(round((playerTwo.laneWins[1]/(playerTwo.laneWins[1]+playerTwo.laneLoss[1]))*100)) + "%)"
                    self.jungWLLabel_2.setText(jungText) 

                    # Setting Mid Win/Loss (%)
                    self.midWLLabel_2.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                    midText = "Mid Win/Loss (%): "+str(playerTwo.laneWins[2]) + "/" + str(playerTwo.laneLoss[2])+ " (" 
                    if playerTwo.laneWins[2] == 0:
                        midText += "0%)"
                    elif playerTwo.laneLoss[2] == 0:
                        midText += "100%)"
                    else:
                        midText += str(round((playerTwo.laneWins[2]/(playerTwo.laneWins[2]+playerTwo.laneLoss[2]))*100)) + "%)"
                    self.midWLLabel_2.setText(midText) 

                    # Setting ADC Win/Loss (%)
                    self.adcWLLabel_2.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                    adcText = "ADC Win/Loss (%): "+str(playerTwo.laneWins[3]) + "/" + str(playerTwo.laneLoss[3])+ " (" 
                    if playerTwo.laneWins[3] == 0:
                        adcText += "0%)"
                    elif playerTwo.laneLoss[3] == 0:
                        adcText += "100%)"
                    else:
                        adcText += str(round((playerTwo.laneWins[3]/(playerTwo.laneWins[3]+playerTwo.laneLoss[3]))*100)) + "%)"
                    self.adcWLLabel_2.setText(adcText) 

                    # Setting Support Win/Loss (%)
                    self.suppWLLabel_2.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                    suppText = "Support Win/Loss (%): "+str(playerTwo.laneWins[4]) + "/" + str(playerTwo.laneLoss[4])+ " (" 
                    if playerTwo.laneWins[4] == 0:
                        suppText += "0%)"
                    elif playerTwo.laneLoss[4] == 0:
                        suppText += "100%)"
                    else:
                        suppText += str(round((playerTwo.laneWins[4]/(playerTwo.laneWins[4]+playerTwo.laneLoss[4]))*100)) + "%)"
                    self.suppWLLabel_2.setText(suppText) 

                    self.staticLabel_2.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#FF0000; font-weight:600;")
                    self.staticLabel_2.setText(
                        "~~ Last Week Stats (Max 100 Games) ~~")
                    self.inputsCanvas.setTabEnabled(1, True)
                # If the player returned no information in last week
                else:
                    self.staticLabel_2.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#FF0000; font-weight:600;")
                    self.staticLabel_2.setText(
                        "~~ This player has no games in the last week ~~")

                    self.ovrWinLossLabel_2.clear()
                    self.mostPlayedLabel_2.clear()
                    self.topWLLabel_2.clear()
                    self.jungWLLabel_2.clear()
                    self.midWLLabel_2.clear()
                    self.adcWLLabel_2.clear()
                    self.suppWLLabel_2.clear()
                    self.champIcon_2.clear()
                    self.inputsCanvas.setTabText(1, playerTwo.name)
                    self.inputsCanvas.setTabEnabled(1, True)
            # If the player returned no information
            else:
                self.rankLabel_2.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#FF0000; font-weight:600;")
                self.rankLabel_2.setText(
                        "The given player username doesn't exist")
                self.rankWinLabel_2.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#FF0000; font-weight:600;")
                self.rankWinLabel_2.setText("OR the Riot Games API is experiencing errors.")
                self.rankLossLabel_2.clear()
                self.staticLabel_2.clear()
                self.ovrWinLossLabel_2.clear()
                self.mostPlayedLabel_2.clear()
                self.topWLLabel_2.clear()
                self.jungWLLabel_2.clear()
                self.midWLLabel_2.clear()
                self.adcWLLabel_2.clear()
                self.suppWLLabel_2.clear()
                self.champIcon_2.clear()
                self.inputsCanvas.setTabText(1, playerTwo.name)
                self.inputsCanvas.setTabEnabled(1, True)
        # If the player input was empty
        elif not self.summoner2Input.text() :
            self.inputsCanvas.setTabText(1, "-")
            self.inputsCanvas.setTabEnabled(1, False)

    '''
    Method to create information object for summoner 3 and handles the updating of GUI objects.
    '''
    def updateThree(self):
        # If the user isn't trying to search the same player and the input isn't empty
        if self.summoner3Input.text() and self.summoner3Input.text() != self.playerThreeN:
            self.playerThreeN = self.summoner3Input.text()

            playerThree = PlayerInfo(self.summoner3Input.text(), 'na1')
            
            # If there was info found on the player
            if not playerThree.error == 'init':
                    self.inputsCanvas.setTabText(self.inputsCanvas.indexOf(
                        self.tab_3), self._translate("MainWindow", playerThree.name))

                    # Setting text for rank
                    self.rankLabel_3.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                    self.rankLabel_3.setText("Rank: "+ playerThree.rank)
                    # Setting text for wins
                    self.rankWinLabel_3.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                    self.rankWinLabel_3.setText(
                        "Ranked Season Wins: "+str(playerThree.rankedWins))
                    # Setting text for losses
                    self.rankLossLabel_3.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                    self.rankLossLabel_3.setText(
                        "Ranked Season Losses: "+str(playerThree.rankedLosses))
                    if not playerThree.error == 'none':
                        # Setting text for last week win rate
                        self.ovrWinLossLabel_3.setStyleSheet(
                            "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                        overall = "Overall Win/Loss (%): "+str(playerThree.wins)+"/"+str(playerThree.losses) +" ("
                        if playerThree.wins == 0:
                            overall += "0%)"
                        elif playerThree.losses == 0:
                            overall += "100%)"
                        else:
                            overall += str(round((playerThree.wins/(playerThree.wins+playerThree.losses))*100)) + "%)"
                        self.ovrWinLossLabel_3.setText(overall)
                        # Setting text for last week most played champion and image
                        self.mostPlayedLabel_3.setStyleSheet(
                            "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                        for champion in championsInfo:
                            if int(champion['key']) == playerThree.res:
                                # Display champion name
                                self.mostPlayedLabel_3.setText("Most Played Champion: " + champion['name'].capitalize())
                                data = urllib.request.urlopen(champion['icon']).read()
                                image = QtGui.QImage()
                                image.loadFromData(data)
                                # Display champion icon
                                self.champIcon_3.setPixmap(QtGui.QPixmap(image).scaled(64, 64, QtCore.Qt.KeepAspectRatio))
                                break

                        # Setting Top Win/Loss (%)
                        self.topWLLabel_3.setStyleSheet(
                            "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                        topText = "Top Win/Loss (%): "+str(playerThree.laneWins[0]) + "/" + str(playerThree.laneLoss[0])+ " (" 
                        if playerThree.laneWins[0] == 0:
                            topText += "0%)"
                        elif playerThree.laneLoss[0] == 0:
                            topText += "100%)"
                        else:
                            topText += str(round((playerThree.laneWins[0]/(playerThree.laneWins[0]+playerThree.laneLoss[0]))*100)) + "%)"
                        self.topWLLabel_3.setText(topText) 

                        # Setting Jungle Win/Loss(%)    
                        self.jungWLLabel_3.setStyleSheet(
                            "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                        jungText = "Jungle Win/Loss (%): "+str(playerThree.laneWins[1]) + "/" + str(playerThree.laneLoss[1])+ " (" 
                        if playerThree.laneWins[1] == 0:
                            jungText += "0%)"
                        elif playerThree.laneLoss[1] == 0:
                            jungText += "100%)"
                        else:
                            jungText += str(round((playerThree.laneWins[1]/(playerThree.laneWins[1]+playerThree.laneLoss[1]))*100)) + "%)"
                        self.jungWLLabel_3.setText(jungText) 

                        # Setting Mid Win/Loss (%)
                        self.midWLLabel_3.setStyleSheet(
                            "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                        midText = "Mid Win/Loss (%): "+str(playerThree.laneWins[2]) + "/" + str(playerThree.laneLoss[2])+ " (" 
                        if playerThree.laneWins[2] == 0:
                            midText += "0%)"
                        elif playerThree.laneLoss[2] == 0:
                            midText += "100%)"
                        else:
                            midText += str(round((playerThree.laneWins[2]/(playerThree.laneWins[2]+playerThree.laneLoss[2]))*100)) + "%)"
                        self.midWLLabel_3.setText(midText) 

                        # Setting ADC Win/Loss (%)
                        self.adcWLLabel_3.setStyleSheet(
                            "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                        adcText = "ADC Win/Loss (%): "+str(playerThree.laneWins[3]) + "/" + str(playerThree.laneLoss[3])+ " (" 
                        if playerThree.laneWins[3] == 0:
                            adcText += "0%)"
                        elif playerThree.laneLoss[3] == 0:
                            adcText += "100%)"
                        else:
                            adcText += str(round((playerThree.laneWins[3]/(playerThree.laneWins[3]+playerThree.laneLoss[3]))*100)) + "%)"
                        self.adcWLLabel_3.setText(adcText) 

                        # Setting Support Win/Loss (%)
                        self.suppWLLabel_3.setStyleSheet(
                            "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                        suppText = "Support Win/Loss (%): "+str(playerThree.laneWins[4]) + "/" + str(playerThree.laneLoss[4])+ " (" 
                        if playerThree.laneWins[4] == 0:
                            suppText += "0%)"
                        elif playerThree.laneLoss[4] == 0:
                            suppText += "100%)"
                        else:
                            suppText += str(round((playerThree.laneWins[4]/(playerThree.laneWins[4]+playerThree.laneLoss[4]))*100)) + "%)"
                        self.suppWLLabel_3.setText(suppText) 

                        # Reinitialize incase of change previously
                        self.staticLabel_3.setStyleSheet("qproperty-alignment: AlignCenter; color:#FF0000; font-weight:600;")
                        self.staticLabel_3.setText("~~ Last Week Stats (Max 100 Games) ~~")
                        self.inputsCanvas.setTabEnabled(2, True)
                    # If the player exists but no last week stats found
                    else:
                        self.staticLabel_3.setStyleSheet(
                            "qproperty-alignment: AlignCenter; color:#FF0000; font-weight:600;")
                        self.staticLabel_3.setText(
                            "~~ This player has no games in the last week ~~")

                        self.ovrWinLossLabel_3.clear()
                        self.mostPlayedLabel_3.clear()
                        self.topWLLabel_3.clear()
                        self.jungWLLabel_3.clear()
                        self.midWLLabel_3.clear()
                        self.adcWLLabel_3.clear()
                        self.suppWLLabel_3.clear()
                        self.champIcon_3.clear()
                        self.inputsCanvas.setTabText(2, playerThree.name)
                        self.inputsCanvas.setTabEnabled(2, True)
                # If no information on the player was found
            else:
                self.rankLabel_3.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#FF0000; font-weight:600;")
                self.rankLabel_3.setText(
                        "The given player username doesn't exist")
                self.rankWinLabel_3.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#FF0000; font-weight:600;")
                self.rankWinLabel_3.setText("OR the Riot Games API is experiencing errors.")
                self.rankLossLabel_3.clear()
                self.staticLabel_3.clear()
                self.ovrWinLossLabel_3.clear()
                self.mostPlayedLabel_3.clear()
                self.topWLLabel_3.clear()
                self.jungWLLabel_3.clear()
                self.midWLLabel_3.clear()
                self.adcWLLabel_3.clear()
                self.suppWLLabel_3.clear()
                self.champIcon_3.clear()
                self.inputsCanvas.setTabText(2, playerThree.name)
                self.inputsCanvas.setTabEnabled(2, True)
        # If the input is empty
        elif not self.summoner3Input.text() :
            self.inputsCanvas.setTabText(2, "-")
            self.inputsCanvas.setTabEnabled(2, False)

    '''
    Method to create information object for summoner 4 and handles the updating of GUI objects.
    '''
    def updateFour(self):
        # If the user isn't trying to search the same player and the input isn't empty
        if self.summoner4Input.text() and self.summoner4Input.text() != self.playerFourN:
            self.playerFourN = self.summoner4Input.text()

            playerFour = PlayerInfo(self.summoner4Input.text(), 'na1')
            
            if not playerFour.error == 'init':
                    self.inputsCanvas.setTabEnabled(3, True)

                    self.inputsCanvas.setTabText(self.inputsCanvas.indexOf(
                        self.tab_4), self._translate("MainWindow", playerFour.name))

                    # Setting text for rank
                    self.rankLabel_4.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                    self.rankLabel_4.setText("Rank: "+ playerFour.rank)
                    # Setting text for wins
                    self.rankWinLabel_4.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                    self.rankWinLabel_4.setText(
                        "Ranked Season Wins: "+str(playerFour.rankedWins))
                    # Setting text for losses
                    self.rankLossLabel_4.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                    self.rankLossLabel_4.setText(
                        "Ranked Season Losses: "+str(playerFour.rankedLosses))
                    if not playerFour.error == 'none':
                        # Setting text for last week win rate
                        self.ovrWinLossLabel_4.setStyleSheet(
                            "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                        overall = "Overall Win/Loss (%): "+str(playerFour.wins)+"/"+str(playerFour.losses) +" ("
                        if playerFour.wins == 0:
                            overall += "0%)"
                        elif playerFour.losses == 0:
                            overall += "100%)"
                        else:
                            overall += str(round((playerFour.wins/(playerFour.wins+playerFour.losses))*100)) + "%)"
                        self.ovrWinLossLabel_4.setText(overall)
                        # Setting text for last week most played champion and image
                        self.mostPlayedLabel_4.setStyleSheet(
                            "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                        for champion in championsInfo:
                            if int(champion['key']) == playerFour.res:
                                # Display most played champion text
                                self.mostPlayedLabel_4.setText("Most Played Champion: " + champion['name'].capitalize())
                                data = urllib.request.urlopen(champion['icon']).read()
                                image = QtGui.QImage()
                                image.loadFromData(data)
                                # Display champion icon
                                self.champIcon_4.setPixmap(QtGui.QPixmap(image).scaled(64, 64, QtCore.Qt.KeepAspectRatio))
                                break

                        # Setting Top Win/Loss (%)
                        self.topWLLabel_4.setStyleSheet(
                            "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                        topText = "Top Win/Loss (%): "+str(playerFour.laneWins[0]) + "/" + str(playerFour.laneLoss[0])+ " (" 
                        if playerFour.laneWins[0] == 0:
                            topText += "0%)"
                        elif playerFour.laneLoss[0] == 0:
                            topText += "100%)"
                        else:
                            topText += str(round((playerFour.laneWins[0]/(playerFour.laneWins[0]+playerFour.laneLoss[0]))*100)) + "%)"
                        self.topWLLabel_4.setText(topText) 

                        # Setting Jungle Win/Loss(%)    
                        self.jungWLLabel_4.setStyleSheet(
                            "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                        jungText = "Jungle Win/Loss (%): "+str(playerFour.laneWins[1]) + "/" + str(playerFour.laneLoss[1])+ " (" 
                        if playerFour.laneWins[1] == 0:
                            jungText += "0%)"
                        elif playerFour.laneLoss[1] == 0:
                            jungText += "100%)"
                        else:
                            jungText += str(round((playerFour.laneWins[1]/(playerFour.laneWins[1]+playerFour.laneLoss[1]))*100)) + "%)"
                        self.jungWLLabel_4.setText(jungText) 

                        # Setting Mid Win/Loss (%)
                        self.midWLLabel_4.setStyleSheet(
                            "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                        midText = "Mid Win/Loss (%): "+str(playerFour.laneWins[2]) + "/" + str(playerFour.laneLoss[2])+ " (" 
                        if playerFour.laneWins[2] == 0:
                            midText += "0%)"
                        elif playerFour.laneLoss[2] == 0:
                            midText += "100%)"
                        else:
                            midText += str(round((playerFour.laneWins[2]/(playerFour.laneWins[2]+playerFour.laneLoss[2]))*100)) + "%)"
                        self.midWLLabel_4.setText(midText) 

                        # Setting ADC Win/Loss (%)
                        self.adcWLLabel_4.setStyleSheet(
                            "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                        adcText = "ADC Win/Loss (%): "+str(playerFour.laneWins[3]) + "/" + str(playerFour.laneLoss[3])+ " (" 
                        if playerFour.laneWins[3] == 0:
                            adcText += "0%)"
                        elif playerFour.laneLoss[3] == 0:
                            adcText += "100%)"
                        else:
                            adcText += str(round((playerFour.laneWins[3]/(playerFour.laneWins[3]+playerFour.laneLoss[3]))*100)) + "%)"
                        self.adcWLLabel_4.setText(adcText) 

                        # Setting Support Win/Loss (%)
                        self.suppWLLabel_4.setStyleSheet(
                            "qproperty-alignment: AlignCenter; color:#146366; font-weight:600;")
                        suppText = "Support Win/Loss (%): "+str(playerFour.laneWins[4]) + "/" + str(playerFour.laneLoss[4])+ " (" 
                        if playerFour.laneWins[4] == 0:
                            suppText += "0%)"
                        elif playerFour.laneLoss[4] == 0:
                            suppText += "100%)"
                        else:
                            suppText += str(round((playerFour.laneWins[4]/(playerFour.laneWins[4]+playerFour.laneLoss[4]))*100)) + "%)"
                        self.suppWLLabel_4.setText(suppText)
                        # Reinitialize incase it was changed before
                        self.staticLabel_4.setStyleSheet(
                            "qproperty-alignment: AlignCenter; color:#FF0000; font-weight:600;")
                        self.staticLabel_4.setText("~~ Last Week Stats (Max 100 Games) ~~")
                        self.inputsCanvas.setTabText(3, playerFour.name)
                        self.inputsCanvas.setTabEnabled(3, True)
                    # If no info on last 7 days was found
                    else:
                        self.staticLabel_4.setStyleSheet(
                            "qproperty-alignment: AlignCenter; color:#FF0000; font-weight:600;")
                        self.staticLabel_4.setText(
                            "~~ This player has no games in the last week ~~")

                        self.ovrWinLossLabel_4.clear()
                        self.mostPlayedLabel_4.clear()
                        self.topWLLabel_4.clear()
                        self.jungWLLabel_4.clear()
                        self.midWLLabel_4.clear()
                        self.adcWLLabel_4.clear()
                        self.suppWLLabel_4.clear()
                        self.champIcon_4.clear()
                        self.inputsCanvas.setTabEnabled(3, True)
            # If player wasn't found
            else:
                self.rankLabel_4.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#FF0000; font-weight:600;")
                self.rankLabel_4.setText(
                        "The given player username doesn't exist")
                self.rankWinLabel_4.setStyleSheet(
                        "qproperty-alignment: AlignCenter; color:#FF0000; font-weight:600;")
                self.rankWinLabel_4.setText("OR the Riot Games API is experiencing errors.")
                self.rankLossLabel_4.clear()
                self.staticLabel_4.clear()
                self.ovrWinLossLabel_4.clear()
                self.mostPlayedLabel_4.clear()
                self.topWLLabel_4.clear()
                self.jungWLLabel_4.clear()
                self.midWLLabel_4.clear()
                self.adcWLLabel_4.clear()
                self.suppWLLabel_4.clear()
                self.champIcon_4.clear()
                self.inputsCanvas.setTabText(3, playerFour.name)
                self.inputsCanvas.setTabEnabled(3, True)
        # If input is empty
        elif not self.summoner4Input.text() :
            self.inputsCanvas.setTabText(3, "-")
            self.inputsCanvas.setTabEnabled(3, False)

    '''
    Function that runs when the SEARCH button is clicked.

    Calls: updateOne, updateTwo, updateThree, and updateFour
    each function updates their own respective GUI window objects
    '''
    def clicked(self):
        # Run all the window update methods in threads to save time.
        p1 = Thread(target = self.updateOne)
        p2 = Thread(target = self.updateTwo)
        p3 = Thread(target = self.updateThree)
        p4 = Thread(target = self.updateFour)
        # Start all of the created Threads
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        # Join all of the Threads so the code after doesn't run until the threads complete
        p1.join()
        p2.join()
        p3.join()
        p4.join()

        # After the button is a clicked a 45 second cooldown on the search button is initiated
        # to prohibit application input overload and deter user from reaching the API request limit.
        self.searchButton.setEnabled(False)
        QtCore.QTimer.singleShot(45000, lambda: self.searchButton.setDisabled(False))

# GUI initialization in main.
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
