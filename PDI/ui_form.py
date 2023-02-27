# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QTabWidget, QToolButton, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1444, 739)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(-10, 40, 1431, 16))
        self.line.setStyleSheet(u"\n"
"border-color: rgb(255,255,255);\n"
"border-style: solid;\n"
"border-width: 2px; \n"
"border-radius: 10px;")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.IconFile = QPushButton(self.centralwidget)
        self.IconFile.setObjectName(u"IconFile")
        self.IconFile.setGeometry(QRect(120, 0, 51, 31))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(90, 630, 87, 26))
        self.imageLabel = QLabel(self.centralwidget)
        self.imageLabel.setObjectName(u"imageLabel")
        self.imageLabel.setGeometry(QRect(0, 80, 304, 551))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageLabel.sizePolicy().hasHeightForWidth())
        self.imageLabel.setSizePolicy(sizePolicy)
        self.imageLabel.setMinimumSize(QSize(0, 0))
        self.imageLabel.setAutoFillBackground(False)
        self.imageLabel.setStyleSheet(u"\n"
"border-color: rgb(255,255,255);\n"
"border-style: solid;\n"
"border-width: 2px; \n"
"border-radius: 20px;")
        self.imageLabel.setFrameShape(QFrame.Box)
        self.imageLabel.setLineWidth(0)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.toolButton = QToolButton(self.centralwidget)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setGeometry(QRect(0, 2, 51, 25))
        self.toolButton_2 = QToolButton(self.centralwidget)
        self.toolButton_2.setObjectName(u"toolButton_2")
        self.toolButton_2.setGeometry(QRect(70, 2, 26, 25))
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(330, 80, 1021, 551))
        self.tabWidget.setStyleSheet(u"border-color: rgb(255,255,255);\n"
"border-style: solid;\n"
"border-width: 2px; \n"
"border-radius: 20px;")
        self.Imagem = QWidget()
        self.Imagem.setObjectName(u"Imagem")
        self.tabWidget.addTab(self.Imagem, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1444, 23))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.IconFile.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.imageLabel.setText(QCoreApplication.translate("MainWindow", u"Colocar uma Imagem", None))
        self.toolButton.setText(QCoreApplication.translate("MainWindow", u"File", None))
        self.toolButton_2.setText(QCoreApplication.translate("MainWindow", u"IA", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Imagem), QCoreApplication.translate("MainWindow", u"IMG", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Matriz", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"RESPOSTA", None))
    # retranslateUi

