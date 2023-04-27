import sys
sys.path.append('App/Imports')

from Imports import *


img=None

class SubWindow(QMainWindow):
    def __init__(self, parent=None,img2=None):
        super().__init__(parent)
        global img 
        img= img2
        self.setWindowTitle('Sub Window')
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setRenderHint(QPainter.SmoothPixmapTransform)
        self.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.zoom_in_button = QtWidgets.QPushButton("")
        icon = QtGui.QIcon("App/Imagens/zoom.png")
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
        iconO = QtGui.QIcon("App/Imagens/zoomout.png")
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
        iconR = QtGui.QIcon("App/Imagens/rodar.png")
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



    def adjust_contrast(self):
        global img
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
        max_val = bins[np.searchsorted(
            cdf, self.max_slider.value(), side='right') - 1]

        # Normalizar a matriz de imagem para que os valores estejam dentro da faixa definida pelo usuário
        img_array_norm = (img_array - min_val) / (max_val - min_val) * 255
        img_array_norm = np.clip(img_array_norm, 0, 255).astype(np.uint8)

        # Converter a matriz de imagem normalizada em uma imagem PIL
        img_contrast = Image.fromarray(img_array_norm)

        # Salvar a imagem em um arquivo temporário no formato PNG
        temp_path = "App/Imagens/temp.png"
        img_contrast.save(temp_path)

        # Exibir a imagem ajustada na interface gráfica do usuário
        self.show_image(temp_path)

    


