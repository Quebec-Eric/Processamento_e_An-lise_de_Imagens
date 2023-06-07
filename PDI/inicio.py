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



