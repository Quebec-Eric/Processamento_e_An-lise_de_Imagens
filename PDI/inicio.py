import sys
sys.path.append('App/Imports')




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



