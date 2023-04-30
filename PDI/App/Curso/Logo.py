import sys
sys.path.append('App/Imports')

from Imports import *

class Logo(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle('Projeto')
        self.setGeometry(100, 100, 400, 200)
        pixmap = QPixmap('App/Imagens/puc_minas.png').scaled(200, 200)  
        logo_label = QLabel(self)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        names_label = QLabel(self)
        names_label.setText('Professor  Alexei')
        names_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(logo_label)
        layout.addWidget(names_label)
        self.setLayout(layout)

