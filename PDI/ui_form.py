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
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(u"background-color: rgb(72, 117, 162);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(-10, 40, 1431, 16))
        self.line.setStyleSheet(u"border-style: solid;\n"
"border-width: 3px; \n"
"border-radius: 10px;")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.Salvar = QPushButton(self.centralwidget)
        self.Salvar.setObjectName(u"Salvar")
        self.Salvar.setGeometry(QRect(60, 2, 61, 31))
        self.Salvar.setAutoFillBackground(False)
        icon = QIcon()
        icon.addFile(u"download.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Salvar.setIcon(icon)
        self.Salvar.setIconSize(QSize(49, 30))
        self.Salvar.setFlat(True)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(110, 480, 121, 51))
        self.toolButton = QToolButton(self.centralwidget)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setGeometry(QRect(-10, 2, 61, 31))
        icon1 = QIcon()
        icon1.addFile(u"Pasta.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton.setIcon(icon1)
        self.toolButton.setIconSize(QSize(100, 100))
        self.toolButton.setAutoRaise(True)
        self.toolButton_2 = QToolButton(self.centralwidget)
        self.toolButton_2.setObjectName(u"toolButton_2")
        self.toolButton_2.setGeometry(QRect(210, 10, 26, 25))
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(340, 80, 1011, 531))
        self.tabWidget.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
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
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 140, 321, 231))
        self.label.setPixmap(QPixmap(u"medicina-logo-886CC8F59D-seeklogo.com.png"))
        self.label.setScaledContents(True)
        self.Colaboradores = QPushButton(self.centralwidget)
        self.Colaboradores.setObjectName(u"Colaboradores")
        self.Colaboradores.setEnabled(True)
        self.Colaboradores.setGeometry(QRect(1200, -10, 71, 61))
        self.Colaboradores.setAutoFillBackground(False)
        icon2 = QIcon()
        icon2.addFile(u"Pesssoas.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Colaboradores.setIcon(icon2)
        self.Colaboradores.setIconSize(QSize(50, 50))
        self.Colaboradores.setFlat(True)
        self.Funcionamento = QPushButton(self.centralwidget)
        self.Funcionamento.setObjectName(u"Funcionamento")
        self.Funcionamento.setGeometry(QRect(1290, -10, 51, 61))
        self.Funcionamento.setAutoFillBackground(False)
        icon3 = QIcon()
        icon3.addFile(u"57108.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Funcionamento.setIcon(icon3)
        self.Funcionamento.setIconSize(QSize(37, 44))
        self.Funcionamento.setFlat(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1444, 23))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(MainWindow.teste)
        self.tabWidget.currentChanged.connect(MainWindow.Mudar)
        self.toolButton.clicked.connect(MainWindow.File)
        self.Funcionamento.clicked.connect(MainWindow.Funcionamento)
        self.Colaboradores.clicked.connect(MainWindow.Colaboradores)

        self.tabWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.Salvar.setText("")
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Imagem", None))
        self.toolButton.setText(QCoreApplication.translate("MainWindow", u"File", None))
        self.toolButton_2.setText(QCoreApplication.translate("MainWindow", u"IA", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Imagem), QCoreApplication.translate("MainWindow", u"IMG", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Matriz", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"RESPOSTA", None))
        self.label.setText("")
        self.Colaboradores.setText("")
        self.Funcionamento.setText("")
    # retranslateUi

