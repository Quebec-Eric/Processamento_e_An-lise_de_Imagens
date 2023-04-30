#Janela para mostrar os calaboradores do projeto
import sys
sys.path.append('App/Imports')

from Imports import *

class Janela(QDialog):
    def  __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Colaboradores")
        self.resize(270, 110)
        layout = QVBoxLayout()
        layout.addWidget(QPushButton("Eric Azevedo de Oliveira"))
        layout.addWidget(QPushButton("--------------"))
        layout.addWidget(QPushButton("-------------"))
        layout.addStretch()
        self.setLayout(layout)