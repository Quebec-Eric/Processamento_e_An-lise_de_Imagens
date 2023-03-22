import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6 import QtWidgets, QtGui

from ui_form import Ui_MainWindow
import cv2
import numpy as np

from ui_form import Ui_MainWindow

img = "R.png"


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
        self.zoom_in_button = QtWidgets.QPushButton("Zoom In")
        self.zoom_in_button.clicked.connect(self.zoom_in)

        self.zoom_out_button = QtWidgets.QPushButton("Zoom Out")
        self.zoom_out_button.clicked.connect(self.zoom_out)

        self.rotate_button = QtWidgets.QPushButton("Rotate")
        self.rotate_button.clicked.connect(self.rotate)

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
        min_val = self.min_slider.value()
        max_val = self.max_slider.value()

        if min_val >= max_val:
            return

        img = cv2.imread("R.png", cv2.IMREAD_GRAYSCALE)
        np_img = np.array(img, dtype=np.float32)

    # Normalizando a imagem para o intervalo [0, 1]
        np_img /= 255.0

    # Aplicando o ajuste de contraste
        np_img = (np_img - min_val/255.0) * (255.0/(max_val - min_val))
        np_img = np.clip(np_img, 0, 1)

    # Convertendo a imagem de volta para o formato uint8
        np_img = (np_img * 255.0).astype(np.uint8)

    # Atualizando a imagem exibida na sub janela
        self.show_image(cv2.cvtColor(np_img, cv2.COLOR_BGR2GRAY))
        


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

    def File(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Selecionar arquivo', '', 'Arquivos de Imagem (*.png *.jpg *.jpeg *.bmp *.gif)')
        self.subwindow.show_image(file_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
