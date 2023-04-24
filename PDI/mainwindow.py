import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import QTabWidget
from PySide6.QtWidgets import *
from matplotlib.figure import Figure
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6 import QtWidgets, QtGui
from PIL import Image,ImageOps
from ui_form import Ui_MainWindow
import cv2
from matplotlib.backends.backend_qt5agg import FigureCanvas
import matplotlib.pyplot as plt

import numpy as np

from ui_form import Ui_MainWindow

img = None

#janela para mostrar tonalizacoes de cinza
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
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.zoom_in_button)
        button_layout.addWidget(self.zoom_out_button)
        button_layout.addWidget(self.rotate_button)
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(button_layout)
        self.setCentralWidget(central_widget)
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
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.zoom_in_button)
        button_layout.addWidget(self.zoom_out_button)
        button_layout.addWidget(self.rotate_button)
        slider_layout = QtWidgets.QHBoxLayout()
        slider_layout.addWidget(QLabel("Min"))
        slider_layout.addWidget(self.min_slider)
        slider_layout.addWidget(QLabel("Max"))
        slider_layout.addWidget(self.max_slider)
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.view)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(slider_layout)
        widget = QtWidgets.QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        self.pixmap = QPixmap(img)
        self.scene.addPixmap(self.pixmap)

    #mostrar a imagem na jannela
    def show_image(self, img):
        self.scene.clear()
        pixmap = QPixmap(img)
        self.scene.addPixmap(pixmap)
        self.pixmap = pixmap

    #dar o zomm
    def zoom_in(self):
        self.view.scale(1.2, 1.2)

    #tirar o zoo
    def zoom_out(self):
        self.view.scale(1 / 1.2, 1 / 1.2)

    #girar a imagem 
    def rotate(self):
        transform = QTransform()
        transform.rotate(90)
        rotated_pixmap = self.pixmap.transformed(
            transform, Qt.SmoothTransformation)
        self.scene.clear()
        self.scene.addPixmap(rotated_pixmap)
        self.pixmap = rotated_pixmap

    #ajustar o contrast com base nos botoes de conntrast e com isso ajustar
    def adjust_contrast(self):
    # Abrir a imagem e convertê-la para escala de cinza
        img_gray = Image.open(img).convert('L')
        
        # Equalizar o histograma da imagem
        img_eq = ImageOps.equalize(img_gray)
        
        # Converter a imagem equalizada em uma matriz NumPy
        img_array = np.array(img_eq)
        
        # Definir os valores mínimos e máximos com base no histograma equalizado
        hist, bins = np.histogram(img_array, bins=256, range=(0, 255))
        cdf = hist.cumsum()
        cdf = (cdf - cdf[0]) * 255 / (cdf[-1] - cdf[0])
        min_val = bins[np.searchsorted(cdf, self.min_slider.value(), side='left')]
        max_val = bins[np.searchsorted(cdf, self.max_slider.value(), side='right') - 1]
        
        # Normalizar a matriz de imagem para que os valores estejam dentro da faixa definida pelo usuário
        img_array_norm = (img_array - min_val) / (max_val - min_val) * 255
        img_array_norm = np.clip(img_array_norm, 0, 255).astype(np.uint8)
        
        # Converter a matriz de imagem normalizada em uma imagem PIL
        img_contrast = Image.fromarray(img_array_norm)
        
        # Salvar a imagem em um arquivo temporário no formato PNG
        temp_path = "temp.png"
        img_contrast.save(temp_path)
        
        # Exibir a imagem ajustada na interface gráfica do usuário
        self.show_image(temp_path)


class Logo(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle('Projeto')
        self.setGeometry(100, 100, 400, 200)
        pixmap = QPixmap('puc_minas.png').scaled(200, 200)  
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





#Janela para mostrar os calaboradores do projeto
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

       

#janela Principal do programa onde sera realizado todo o programa em si
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_components()



    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()

    def init_components(self):
        self.setWindowTitle('PDI')
        self.showMaximized()
        self.ui.tabWidget.currentChanged.connect(self.tab_changed)  
    

    def mudarAbaImagem(self):
        
        for i in range(self.ui.tabWidget.count()):
            if self.ui.tabWidget.tabText(i) == "IMG":
                tab_imagem = self.ui.tabWidget.widget(i)
                layout = tab_imagem.layout()
                if layout is not None:
                    label = layout.itemAt(0).widget()
                    button_verificar = layout.itemAt(1).widget()
                    button_hist = layout.itemAt(2).widget()
                    spacer = layout.itemAt(3)
                else:
                    label = QLabel()
                    button_verificar = QPushButton("Verificar")
                    button_hist = QPushButton("Hist")
                    spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
                    layout = QVBoxLayout(tab_imagem)
                    layout.addWidget(label)
                    layout.addWidget(button_verificar)
                    layout.addWidget(button_hist)
                    layout.addItem(spacer)
                    layout.setAlignment(Qt.AlignLeft)
                break
        else:
            tab_imagem = QWidget()
            layout = QVBoxLayout(tab_imagem)
            label = QLabel()
            button_verificar = QPushButton("Verificar")
            button_hist = QPushButton("Hist")
            spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            layout.addWidget(label)
            layout.addWidget(button_verificar)
            layout.addWidget(button_hist)
            layout.addItem(spacer)
            layout.setAlignment(Qt.AlignLeft)

            self.ui.tabWidget.addTab(tab_imagem, "IMG")

        try:

            pixmap = QPixmap('temp.png')
            pixmap = pixmap.scaled(self.ui.tabWidget.width() // 3, self.ui.tabWidget.height() // 1)
            label.setMaximumWidth(self.ui.tabWidget.width() // 3)
            label.setMaximumHeight(self.ui.tabWidget.height() // 1)
            label.setPixmap(pixmap)
            label.setStyleSheet("border: none;")
            button_verificar.setMaximumWidth(label.maximumWidth())
            button_hist.setMaximumWidth(label.maximumWidth())
        
        except:
            label.setText("Imagem não encontrada.")

        button_verificar.clicked.connect(self.on_botao_clicado)
        button_hist.clicked.connect(self.on_botao_hist_clicado)

        
    def on_botao_hist_clicado(self):
        img = cv2.imread('temp.png', cv2.IMREAD_GRAYSCALE)
        hist = cv2.calcHist([img], [0], None, [256], [0, 256])
        
        mean_val = int(cv2.mean(img)[0])
        min_val, max_val, _, _ = cv2.minMaxLoc(img)
        
        plt.figure()
        plt.title('Histograma de Tonalidades de Cinza')
        plt.xlabel('Intensidade de Cinza')
        plt.ylabel('Frequência')
        plt.plot(hist, color='gray')
        plt.axvline(x=mean_val, color='red', label=f'Média: {mean_val}')
        plt.text(0.05, 0.95, f'Máximo: {max_val:.0f}\nMínimo: {min_val:.0f}', transform=plt.gca().transAxes, va='top', ha='left')
        plt.legend(loc='upper right')
        plt.xlim([0, 256])
        plt.ylim([0, max(hist)+1000])
        plt.bar(range(256), hist.flatten(), width=1, color='gray')
        plt.show()


    def on_botao_clicado(self):
            img1 = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
            scale_percent = 10 
            width = int(img1.shape[1] * scale_percent / 100)
            height = int(img1.shape[0] * scale_percent / 100)
            dim = (width, height)
            img1 = cv2.resize(img1, dim, interpolation=cv2.INTER_AREA)

            img2 = cv2.imread('temp.png', cv2.IMREAD_GRAYSCALE)
            scale_percent = 10  
            width = int(img2.shape[1] * scale_percent / 100)
            height = int(img2.shape[0] * scale_percent / 100)
            dim = (width, height)
            img2 = cv2.resize(img2, dim, interpolation=cv2.INTER_AREA)
            cv2.namedWindow('Original', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('Original', img1)
            cv2.namedWindow('Segmentada', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('Segmentada', img2)
            cv2.resizeWindow('Original', width, height)
            cv2.moveWindow('Original', 0, 0)              
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
