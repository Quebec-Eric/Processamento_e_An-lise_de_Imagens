import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import QTabWidget
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
        icon = QtGui.QIcon("Images/zoom.png")
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
        iconO = QtGui.QIcon("Images/zoomout.png")
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
        iconR = QtGui.QIcon("Images/rodar.png")
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
        temp_path = "Images/temp.png"
        img_contrast.save(temp_path)

    # Exibir a imagem resultante na sub-janela
        self.show_image(temp_path)


class Logo(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)

        # Configura a janela
        self.setWindowTitle('Projeto')
        self.setGeometry(100, 100, 400, 200)

       # Carrega a imagem e redimensiona para 100x100 pixels
        pixmap = QPixmap('Images/puc_minas.png').scaled(200, 200)

        # Cria o label com a logo do projeto
        logo_label = QLabel(self)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # Cria o label com o nome dos realizadores
        names_label = QLabel(self)
        names_label.setText('Realizadores: Fulano e Ciclano')
        names_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Cria o layout vertical e adiciona os labels
        layout = QVBoxLayout()
        layout.addWidget(logo_label)
        layout.addWidget(names_label)

        # Configura o layout na janela
        self.setLayout(layout)





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
        layout.addWidget(QPushButton("João Gabriel Sena Fernandes"))
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
        self.ui.tabWidget.currentChanged.connect(self.tab_changed)  
    
        
    def mudarAbaImagem(self):
        # Verifica se a aba de imagem já existe
        for i in range(self.ui.tabWidget.count()):
            if self.ui.tabWidget.tabText(i) == "IMG":
                tab_imagem = self.ui.tabWidget.widget(i)
                layout = tab_imagem.layout()
                if layout is not None:
                    label = layout.itemAt(0).widget()
                    button = layout.itemAt(1).widget()
                    spacer = layout.itemAt(2)
                else:
                    label = QLabel()
                    button = QPushButton("Botão")
                    spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
                    layout = QVBoxLayout(tab_imagem)
                    layout.addWidget(label)
                    layout.addWidget(button)
                    layout.addItem(spacer)
                    layout.setAlignment(Qt.AlignLeft)
                break
        else:
            tab_imagem = QWidget()
            layout = QVBoxLayout(tab_imagem)
            label = QLabel()
            button = QPushButton("Botão")
            spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            layout.addWidget(label)
            layout.addWidget(button)
            layout.addItem(spacer)
            layout.setAlignment(Qt.AlignLeft)

            self.ui.tabWidget.addTab(tab_imagem, "IMG")

        try:

            pixmap = QPixmap('Images/temp.png')
            pixmap = pixmap.scaled(self.ui.tabWidget.width() // 3, self.ui.tabWidget.height() // 1)
            label.setMaximumWidth(self.ui.tabWidget.width() // 3)
            label.setMaximumHeight(self.ui.tabWidget.height() // 1)
            label.setPixmap(pixmap)
            #cv2.imshow('Imagem original', pixmap)
            label.setStyleSheet("border: none;")
            button.setMaximumWidth(label.maximumWidth())
        except:
            label.setText("Imagem não encontrada.")

        button.clicked.connect(self.on_botao_clicado)

    def on_botao_clicado(self):
            img1 = cv2.imread('Images/R.png', cv2.IMREAD_GRAYSCALE)
            # Redimensionando a imagem e a janela
            scale_percent = 10  # reduzindo a escala da imagem para 50%
            width = int(img1.shape[1] * scale_percent / 100)
            height = int(img1.shape[0] * scale_percent / 100)
            dim = (width, height)
            img1 = cv2.resize(img1, dim, interpolation=cv2.INTER_AREA)

            img2 = cv2.imread('Images/temp.png', cv2.IMREAD_GRAYSCALE)
            # Redimensionando a imagem e a janela
            scale_percent = 10  # reduzindo a escala da imagem para 50%
            width = int(img2.shape[1] * scale_percent / 100)
            height = int(img2.shape[0] * scale_percent / 100)
            dim = (width, height)
            img2 = cv2.resize(img2, dim, interpolation=cv2.INTER_AREA)


            cv2.namedWindow('Original', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('Original', img1)
            
            cv2.namedWindow('Segmentada', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('Segmentada', img2)
            
            # Redimensionando a janela
            cv2.resizeWindow('Original', width, height)
            cv2.moveWindow('Original', 0, 0)  # mover a janela para (0,0)
            
            cv2.waitKey(0)
            cv2.destroyAllWindows()


        

    def tab_changed(self):
        if(self.ui.tabWidget.currentIndex()==0):
            self.mudarAbaImagem()
        elif(self.ui.tabWidget.currentIndex()==1):
            print("Matrix")
        else:
            print("Resultado") 

    def teste(self):
        self.subwindow = SubWindow(self)
        self.subwindow.show()

    def Mudar(self):
        print("")

    def Funcionamento(self):
        return

    def Pontos(self):    
        self.Logo =  Logo(self)
        self.Logo.show()


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
