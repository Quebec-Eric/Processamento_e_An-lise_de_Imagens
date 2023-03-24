import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6 import QtWidgets, QtGui
from PIL import Image
from ui_form import Ui_MainWindow
import cv2
import numpy as np

from ui_form import Ui_MainWindow

img = None


class SubWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Sub Window')

        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setRenderHint(QPainter.SmoothPixmapTransform)
        self.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        # Adicionando botões
        self.zoom_in_button = QtWidgets.QPushButton("")
        icon = QtGui.QIcon("zoom.png")
        icon_size = QtCore.QSize(40, 40)
        self.zoom_in_button.setIconSize(icon_size)
        self.zoom_in_button.setIcon(icon)
        self.zoom_in_button.setFixedSize(icon_size + QtCore.QSize(6,6))
        self.zoom_in_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: none;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_in_button.setAutoFillBackground(True)

        self.zoom_out_button = QtWidgets.QPushButton("")
        iconO = QtGui.QIcon("zoomout.png")
        self.zoom_out_button.setIcon(iconO)
        self.zoom_out_button.setIconSize(icon_size)
        self.zoom_out_button.setFixedSize(icon_size + QtCore.QSize(6, 6))
        self.zoom_out_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: none;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.zoom_out_button.setAutoFillBackground(True)

        self.rotate_button = QtWidgets.QPushButton("")
        iconR = QtGui.QIcon("rodar.png")
        self.rotate_button.setIcon(iconR)
        self.rotate_button.setIconSize(icon_size)
        self.rotate_button.setFixedSize(icon_size + QtCore.QSize(6, 6))
        self.rotate_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: none;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        self.rotate_button.clicked.connect(self.rotate)
        self.rotate_button.setAutoFillBackground(True)

        # Adicionando os botões no layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.zoom_in_button)
        button_layout.addWidget(self.zoom_out_button)
        button_layout.addWidget(self.rotate_button)

        # Adicionando o layout na janela principal
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(button_layout)
        self.setCentralWidget(central_widget)



        # Adicionando barras de deslizamento
        self.min_slider = QSlider(Qt.Horizontal)
        self.min_slider.setMinimum(0)
        self.min_slider.setMaximum(255)
        self.min_slider.setValue(0)
        self.min_slider.setTickPosition(QSlider.TicksBelow)
        self.min_slider.setTickInterval(1)
        self.min_slider.valueChanged.connect(self.adjust_contrast)

        self.max_slider = QSlider(Qt.Horizontal)
        self.max_slider.setMinimum(0)
        self.max_slider.setMaximum(255)
        self.max_slider.setValue(255)
        self.max_slider.setTickPosition(QSlider.TicksBelow)
        self.max_slider.setTickInterval(1)
        self.max_slider.valueChanged.connect(self.adjust_contrast)

        # Adicionando layout para botões e barras de deslizamento
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.zoom_in_button)
        button_layout.addWidget(self.zoom_out_button)
        button_layout.addWidget(self.rotate_button)

        slider_layout = QtWidgets.QHBoxLayout()
        slider_layout.addWidget(QLabel("Min"))
        slider_layout.addWidget(self.min_slider)
        slider_layout.addWidget(QLabel("Max"))
        slider_layout.addWidget(self.max_slider)

        # Adicionando layout principal para janela
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.view)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(slider_layout)

        widget = QtWidgets.QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        # Carregando imagem
        self.pixmap = QPixmap(img)
        self.scene.addPixmap(self.pixmap)

    def show_image(self, img):
        self.scene.clear()
        pixmap = QPixmap(img)
        self.scene.addPixmap(pixmap)
        self.pixmap = pixmap

    def zoom_in(self):
        self.view.scale(1.2, 1.2)

    def zoom_out(self):
        self.view.scale(1 / 1.2, 1 / 1.2)

    def rotate(self):
        transform = QTransform()
        transform.rotate(90)
        rotated_pixmap = self.pixmap.transformed(
            transform, Qt.SmoothTransformation)
        self.scene.clear()
        self.scene.addPixmap(rotated_pixmap)
        self.pixmap = rotated_pixmap

    def adjust_contrast(self):
    # Carregar a imagem em tons de cinza
        img_gray = Image.open(img).convert('L')
        img_array = np.array(img_gray)

    # Definir os valores mínimo e máximo de intensidade da imagem com base nos valores dos sliders
        min_val = self.min_slider.value()
        max_val = self.max_slider.value()

    # Normalizar os valores dos pixels para o intervalo [0, 255]
        img_array_norm = (img_array - min_val) / (max_val - min_val) * 255
        img_array_norm = np.clip(img_array_norm, 0, 255).astype(np.uint8)

    # Converter a imagem numpy de volta para PIL
        img_contrast = Image.fromarray(img_array_norm)

    # Salvar a imagem resultante temporariamente em um arquivo
        temp_path = "temp.png"
        img_contrast.save(temp_path)

    # Exibir a imagem resultante na sub-janela
        self.show_image(temp_path)


class Janela(QDialog):
    def  __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Colaboradores")
        # Define as propriedades da janela
        self.resize(270, 110)
        # Create a QVBoxLayout instance
        layout = QVBoxLayout()
        # Add widgets to the layout
        layout.addWidget(QPushButton("Eric Azevedo de Oliveira"))
        layout.addWidget(QPushButton("--------------"))
        layout.addWidget(QPushButton("-------------"))
        layout.addStretch()
        # Set the layout on the application's window
        self.setLayout(layout)

       


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_components()

    def init_components(self):
        self.setWindowTitle('PDI')
        self.showMaximized()

    def teste(self):
        self.subwindow = SubWindow(self)
        self.subwindow.show()

    def Mudar(self):
        print("oi")

    def Funcionamento(self):

         print("oi")

    def Colaboradores(self):
        self.janela = Janela(self)
        self.janela.show()
        
    def File(self):
        global img
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", "Image Files (*.png *.jpg *.bmp *.tiff)")
        if fileName:
           img = fileName


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
