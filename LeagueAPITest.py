import json
import requests
import RequestMatchlist.requestMatchlists as RequestMatchlists
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os

# Library for ease of Riot Game API use.
# https://riot-watcher.readthedocs.io/en/latest/
from riotwatcher import RiotWatcher, ApiError
print(json.load(open("keys.json", encoding="UTF-8"))['apiKey'])
api = RiotWatcher(
    json.load(open("keys.json", encoding="UTF-8"))['apiKey'])


class Ui_MainWindow(object):
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
        self.lolImage.setStyleSheet("image: url(:/lol-icon/lol-logo.png);")
        self.lolImage.setText("")
        self.lolImage.setPixmap(QtGui.QPixmap(
            "../../Users/Sean Blevins/.designer/backup/Images/lol-logo.png"))
        self.lolImage.setScaledContents(True)
        self.lolImage.setObjectName("lolImage")
        self.inputsCanvas = QtWidgets.QTabWidget(self.centralwidget)
        self.inputsCanvas.setGeometry(QtCore.QRect(20, 220, 631, 341))
        self.inputsCanvas.setObjectName("inputsCanvas")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.summ1Data = QtWidgets.QTextBrowser(self.tab)
        self.summ1Data.setGeometry(QtCore.QRect(55, 20, 511, 271))
        self.summ1Data.setObjectName("summ1Data")
        self.inputsCanvas.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.inputsCanvas.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.inputsCanvas.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.inputsCanvas.addTab(self.tab_4, "")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(130, 100, 241, 121))
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
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.summoner1Input = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.summoner1Input.setObjectName("summoner1Input")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.summoner1Input)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(
            3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(
            4, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.summoner2Input = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.summoner2Input.setObjectName("summoner2Input")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.FieldRole, self.summoner2Input)
        self.summoner3Input = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.summoner3Input.setObjectName("summoner3Input")
        self.formLayout.setWidget(
            3, QtWidgets.QFormLayout.FieldRole, self.summoner3Input)
        self.summoner4Input = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.summoner4Input.setObjectName("summoner4Input")
        self.formLayout.setWidget(
            4, QtWidgets.QFormLayout.FieldRole, self.summoner4Input)
        self.searchButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchButton.setGeometry(QtCore.QRect(400, 140, 91, 31))
        self.searchButton.setStyleSheet("")
        self.searchButton.setObjectName("searchButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 668, 21))
        self.menubar.setObjectName("menubar")
        self.menuPre_game_Search = QtWidgets.QMenu(self.menubar)
        self.menuPre_game_Search.setObjectName("menuPre_game_Search")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuPre_game_Search.menuAction())

        self.retranslateUi(MainWindow)
        self.inputsCanvas.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.lolImage.setPixmap(QtGui.QPixmap(
            "./Images/lol-logo.png"))
        # Summoner search button click method call
        self.searchButton.clicked.connect(self.clicked)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(
            "MainWindow", "Sean\'s League Program"))
        self.inputsCanvas.setTabText(self.inputsCanvas.indexOf(
            self.tab), _translate("MainWindow", "Summoner 1"))
        self.inputsCanvas.setTabText(self.inputsCanvas.indexOf(
            self.tab_2), _translate("MainWindow", "Summoner 2"))
        self.inputsCanvas.setTabText(self.inputsCanvas.indexOf(
            self.tab_3), _translate("MainWindow", "Summoner 3"))
        self.inputsCanvas.setTabText(self.inputsCanvas.indexOf(
            self.tab_4), _translate("MainWindow", "Summoner 4"))
        self.label.setText(_translate(
            "MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Summoner #1:</span></p></body></html>"))
        self.label_2.setText(_translate(
            "MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Summoner #2:</span></p></body></html>"))
        self.label_3.setText(_translate(
            "MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Summoner #3:</span></p></body></html>"))
        self.label_4.setText(_translate(
            "MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Summoner #4:</span></p></body></html>"))
        self.searchButton.setText(_translate("MainWindow", "SEARCH"))
        self.menuPre_game_Search.setTitle(
            _translate("MainWindow", "Pre-game Search"))

    def clicked(self):
        print(self.summoner1Input.text())
        stats = summonerSearch(self, 'na1', self.summoner1Input.text())
        self.summ1Data.setText(str(stats))


def summonerSearch(self, region, name):
    summoner = api.summoner.by_name(region, name)
    print(summoner)
    stats = api.league.by_summoner(region, summoner['id'])
    return stats
    # Except e


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

# Importing functions to allow for use - ex. RequestMatchlists.requestLastDay()

#apiKey = json.load(open("keys.json", encoding="UTF-8"))['apiKey']

# Creates a JSON object with all champion names and other information given in championID.json
# Credit of json file to https://github.com/ngryman/lol-champions/blob/master/champions.json - By ngryman
with open("./Information/championID.json", encoding="UTF-8") as f:
    championsInfo = json.load(f)

# for champ in championsInfo:
#    print(champ['name'])

# API key from developer.riotgames.com


def requestSummonerData(apiKey, region, summonerName):
    response = requests.get(
        "https://"+region+".api.riotgames.com/lol/summoner/v4/summoners/by-name/"+summonerName+"?api_key="+apiKey)
    # print(response.json())
    return response


#summoner = requestSummonerData(apiKey, "na1", "SeanTehScrub")
#requestGames(apiKey, "na1", summoner.json()['accountId'])
# root.mainloop()  # Runs
