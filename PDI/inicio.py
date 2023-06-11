#Pontifícia Universidade Católica de Minas Gerais (Campus Coração Eucarístico)
#Ciência da Computação
#Bryan Jonathan Melo De Oliveira - 708688
#Eric Azevedo de Oliveira - 1269480
#João Gabriel Sena Fernandes - 1209882

#Dependencias
import sys
sys.path.append('App/Imports')
import os

# Redireciona a saída de erro para /dev/null no Linux/macOS ou para nul no Windows
if os.name == 'posix':  # Linux ou macOS
    devnull = open('/dev/null', 'w')

os.dup2(devnull.fileno(), 2)
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from Imports import *
from mainwindow import MainWindow
from Imports import *
from App.Curso.Logo import Logo
from App.JanelaCinza.JanelaSeg import SubWindow
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()

    widget.show()
    sys.exit(app.exec())



