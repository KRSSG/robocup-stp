# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1126, 688)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 600, 400))
        self.graphicsView.setStyleSheet(_fromUtf8("background-color: rgb(85, 170, 0);\n"
"background-color: rgb(0, 85, 0);"))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.GoToBall = QtGui.QPushButton(self.centralwidget)
        self.GoToBall.setGeometry(QtCore.QRect(920, 80, 99, 27))
        self.GoToBall.setObjectName(_fromUtf8("GoToBall"))
        self.textBotId = QtGui.QLineEdit(self.centralwidget)
        self.textBotId.setGeometry(QtCore.QRect(790, 80, 113, 27))
        self.textBotId.setObjectName(_fromUtf8("textBotId"))
        self.bot_id = QtGui.QLabel(self.centralwidget)
        self.bot_id.setGeometry(QtCore.QRect(740, 90, 41, 17))
        self.bot_id.setObjectName(_fromUtf8("bot_id"))
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(740, 30, 161, 27))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.GoToBallFsm = QtGui.QPushButton(self.centralwidget)
        self.GoToBallFsm.setGeometry(QtCore.QRect(920, 110, 121, 27))
        self.GoToBallFsm.setObjectName(_fromUtf8("GoToBallFsm"))
        self.GoInTriangle = QtGui.QPushButton(self.centralwidget)
        self.GoInTriangle.setGeometry(QtCore.QRect(790, 160, 99, 27))
        self.GoInTriangle.setObjectName(_fromUtf8("GoInTriangle"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(270, 460, 81, 201))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.bot0 = QtGui.QCheckBox(self.groupBox)
        self.bot0.setGeometry(QtCore.QRect(10, 20, 51, 22))
        self.bot0.setObjectName(_fromUtf8("bot0"))
        self.bot1 = QtGui.QCheckBox(self.groupBox)
        self.bot1.setGeometry(QtCore.QRect(10, 40, 51, 22))
        self.bot1.setObjectName(_fromUtf8("bot1"))
        self.bot2 = QtGui.QCheckBox(self.groupBox)
        self.bot2.setGeometry(QtCore.QRect(10, 60, 61, 22))
        self.bot2.setObjectName(_fromUtf8("bot2"))
        self.bot3 = QtGui.QCheckBox(self.groupBox)
        self.bot3.setGeometry(QtCore.QRect(10, 80, 61, 22))
        self.bot3.setObjectName(_fromUtf8("bot3"))
        self.bot4 = QtGui.QCheckBox(self.groupBox)
        self.bot4.setGeometry(QtCore.QRect(10, 100, 61, 22))
        self.bot4.setObjectName(_fromUtf8("bot4"))
        self.bot5 = QtGui.QCheckBox(self.groupBox)
        self.bot5.setGeometry(QtCore.QRect(10, 120, 41, 22))
        self.bot5.setObjectName(_fromUtf8("bot5"))
        self.sendBotId = QtGui.QPushButton(self.groupBox)
        self.sendBotId.setGeometry(QtCore.QRect(-10, 150, 99, 27))
        self.sendBotId.setObjectName(_fromUtf8("sendBotId"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1126, 25))
        self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuDIFFERENT_RRT = QtGui.QMenu(self.menubar)
        self.menuDIFFERENT_RRT.setObjectName(_fromUtf8("menuDIFFERENT_RRT"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionRRT_CONNECT = QtGui.QAction(MainWindow)
        self.actionRRT_CONNECT.setObjectName(_fromUtf8("actionRRT_CONNECT"))
        self.actionRRTStar = QtGui.QAction(MainWindow)
        self.actionRRTStar.setObjectName(_fromUtf8("actionRRTStar"))
        self.actionRRT = QtGui.QAction(MainWindow)
        self.actionRRT.setObjectName(_fromUtf8("actionRRT"))
        self.menubar.addAction(self.menuDIFFERENT_RRT.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.GoToBall.setText(_translate("MainWindow", "GoToBall", None))
        self.bot_id.setText(_translate("MainWindow", "BotId", None))
        self.comboBox.setItemText(0, _translate("MainWindow", "PRM", None))
        self.comboBox.setItemText(1, _translate("MainWindow", "RRT", None))
        self.comboBox.setItemText(2, _translate("MainWindow", "RRTConnect", None))
        self.comboBox.setItemText(3, _translate("MainWindow", "RRTStar", None))
        self.comboBox.setItemText(4, _translate("MainWindow", "LBTRRT", None))
        self.comboBox.setItemText(5, _translate("MainWindow", "LazyRRT", None))
        self.comboBox.setItemText(6, _translate("MainWindow", "TRRT", None))
        self.comboBox.setItemText(7, _translate("MainWindow", "pRRT", None))
        self.comboBox.setItemText(8, _translate("MainWindow", "EST", None))
        self.GoToBallFsm.setText(_translate("MainWindow", "GoToBall(FSM)", None))
        self.GoInTriangle.setText(_translate("MainWindow", "GoInTriangle", None))
        self.groupBox.setTitle(_translate("MainWindow", "BotIds", None))
        self.bot0.setText(_translate("MainWindow", "0", None))
        self.bot1.setText(_translate("MainWindow", "1", None))
        self.bot2.setText(_translate("MainWindow", "2", None))
        self.bot3.setText(_translate("MainWindow", "3", None))
        self.bot4.setText(_translate("MainWindow", "4", None))
        self.bot5.setText(_translate("MainWindow", "5", None))
        self.sendBotId.setText(_translate("MainWindow", "sendBotIds", None))
        self.menuDIFFERENT_RRT.setTitle(_translate("MainWindow", "DIFFERENT_RRT", None))
        self.actionRRT_CONNECT.setText(_translate("MainWindow", "RRT_CONNECT", None))
        self.actionRRTStar.setText(_translate("MainWindow", "RRT_STAR", None))
        self.actionRRT.setText(_translate("MainWindow", "RRT", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

