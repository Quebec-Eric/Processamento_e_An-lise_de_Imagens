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
        MainWindow.setStyleSheet(u"background-color: rgb(151, 157, 172);")
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
        self.Salvar.setGeometry(QRect(70, 4, 61, 31))
        self.Salvar.setAutoFillBackground(False)
        icon = QIcon()
        icon.addFile(u"App/Imagens/download.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Salvar.setIcon(icon)
        self.Salvar.setIconSize(QSize(49, 30))
        self.Salvar.setFlat(True)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(110, 480, 121, 51))
        self.pushButton.setStyleSheet(u"color: rgb(0, 0, 0);")
        icon1 = QIcon()
        icon1.addFile(u"App/Imagens/power.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(icon1)
        self.pushButton.setIconSize(QSize(46, 42))
        self.pushButton.setCheckable(False)
        self.pushButton.setAutoRepeat(False)
        self.pushButton.setAutoExclusive(False)
        self.pushButton.setAutoDefault(False)
        self.pushButton.setFlat(True)
        self.toolButton = QToolButton(self.centralwidget)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setGeometry(QRect(9, -2, 51, 41))
        icon2 = QIcon()
        icon2.addFile(u"App/Imagens/Pasta.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton.setIcon(icon2)
        self.toolButton.setIconSize(QSize(100, 100))
        self.toolButton.setAutoRaise(True)
        self.IA = QToolButton(self.centralwidget)
        self.IA.setObjectName(u"IA")
        self.IA.setGeometry(QRect(140, 4, 46, 33))
        icon3 = QIcon()
        icon3.addFile(u"App/Imagens/IAFoto.png", QSize(), QIcon.Normal, QIcon.Off)
        self.IA.setIcon(icon3)
        self.IA.setIconSize(QSize(48, 39))
        self.IA.setCheckable(False)
        self.IA.setAutoRepeat(True)
        self.IA.setAutoExclusive(True)
        self.IA.setAutoRaise(True)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(340, 80, 1011, 531))
        self.tabWidget.setStyleSheet(u"border-color: rgb(0, 0, 0);\n"
"border-style: solid;\n"
"border-width: 2px; \n"
"border-radius: 20px;\n"
"color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);")
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
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
        self.label.setGeometry(QRect(10, 140, 321, 301))
        self.label.setPixmap(QPixmap(u"App/Imagens/medicina-logo-886CC8F59D-seeklogo.com.png"))
        self.label.setScaledContents(True)
        self.Colaboradores = QPushButton(self.centralwidget)
        self.Colaboradores.setObjectName(u"Colaboradores")
        self.Colaboradores.setEnabled(True)
        self.Colaboradores.setGeometry(QRect(1170, -10, 71, 61))
        self.Colaboradores.setAutoFillBackground(False)
        icon4 = QIcon()
        icon4.addFile(u"App/Imagens/Pesssoas.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Colaboradores.setIcon(icon4)
        self.Colaboradores.setIconSize(QSize(50, 50))
        self.Colaboradores.setFlat(True)
        self.Funcionamento = QPushButton(self.centralwidget)
        self.Funcionamento.setObjectName(u"Funcionamento")
        self.Funcionamento.setGeometry(QRect(1250, -10, 51, 61))
        self.Funcionamento.setAutoFillBackground(False)
        icon5 = QIcon()
        icon5.addFile(u"App/Imagens/57108.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Funcionamento.setIcon(icon5)
        self.Funcionamento.setIconSize(QSize(37, 44))
        self.Funcionamento.setFlat(True)
        self.pontos = QPushButton(self.centralwidget)
        self.pontos.setObjectName(u"pontos")
        self.pontos.setGeometry(QRect(1320, 0, 41, 41))
        self.pontos.setAutoFillBackground(False)
        icon6 = QIcon()
        icon6.addFile(u"App/Imagens/3pontos.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pontos.setIcon(icon6)
        self.pontos.setIconSize(QSize(30, 30))
        self.pontos.setFlat(True)
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
        self.pontos.clicked.connect(MainWindow.Pontos)
        self.IA.clicked.connect(MainWindow.IaMostrar)
        self.Salvar.clicked.connect(MainWindow.salvar)

        self.pushButton.setDefault(False)
        self.tabWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.Salvar.setText("")
        self.pushButton.setText("")
        self.toolButton.setText(QCoreApplication.translate("MainWindow", u"File", None))
        self.IA.setText(QCoreApplication.translate("MainWindow", u"IA", None))
#if QT_CONFIG(accessibility)
        self.Imagem.setAccessibleName("")
#endif // QT_CONFIG(accessibility)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Imagem), QCoreApplication.translate("MainWindow", u"IMG", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"FILTROS", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"RESPOSTA", None))
        self.label.setText("")
        self.Colaboradores.setText("")
        self.Funcionamento.setText("")
        self.pontos.setText("")
    # retranslateUi

