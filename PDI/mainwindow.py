#Pontifícia Universidade Católica de Minas Gerais (Campus Coração Eucarístico)
#Ciência da Computação
#Bryan Jonathan Melo De Oliveira - 708688
#Eric Azevedo de Oliveira - 1269480
#João Gabriel Sena Fernandes - 1209882

import sys

sys.path.append('App/Imports')

from Imports import *
from PIL import Image
import random
import os
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from tensorflow.keras.applications.resnet_v2 import preprocess_input
import tensorflow as tf
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
from App.Curso.Logo import Logo
from App.Colaboradores.JanelaColaboradores import Janela
from App.JanelaCinza.JanelaSeg import SubWindow
from App.PreparativosRede.PreProcessamentoImagens.LerDiretoriosIMg import LeituraDiretorio
from App.PreparativosRede.PreProcessamentoImagens.AumentandoDados import AumentarDados
from App.Mascaras.Binarização.binaria import binaria
from App.Mascaras.Fourier.fourier import fourier
from App.Mascaras.Fourier.passaBaixa import passaBaixa
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Image, SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from App.Mascaras.Bordas.sobel import sobel
from App.Mascaras.RemoverTexto.removerTexto import removerTexto
import cv2
from App.IA.MostrarTxt import MostrarTxt
import numpy as np
import os
from tensorflow.keras.models import load_model
import shutil
from tensorflow.keras.models import load_model
import numpy as np
import tensorflow as tf
from PIL import Image
import os
from tensorflow.keras.applications.resnet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image

#variaveis globais que serao utiizadas em todo codigo
img = None
intQual=0
train = []
porcentagemE=[]
classeEscolhida=0
l1=None
l2=None
test = []
fezerSobel=0
fezerBinarizacao=0
fazerForiier=0
fazerpassaBaixa=0
intQualPredicao=0
#janela Principal do programa onde sera realizado todo o programa em si
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_components()

    #funccao para quando aertar f11 deixar a interface em toda tela
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()

    #funcao para iniciar os componentes do trabalho completo
    def init_components(self):
        self.setWindowTitle('PDI')
        self.showMaximized()
        self.ui.tabWidget.currentChanged.connect(self.tab_changed)  
        
    # funcao para ao ir para a tab Img , ee mostrar a imagem que sofreu o janelamento que escolhemos e a limializacao automatiica  deixando so o contorno da mama    
    def mudarAbaImagem(self):
        self.automatica()
        # Encontra ou cria o widget de imagem
        for i in range(self.ui.tabWidget.count()):
            # se ja exister uma tabeWidget criada , colocar os botoes verificar a hist
            if self.ui.tabWidget.tabText(i) == "IMG":
                tab_imagem = self.ui.tabWidget.widget(i)
                layout = tab_imagem.layout()
                if layout is not None:
                    label1 = layout.itemAt(0).widget()
                    label2 = QLabel() 
                    button_verificar = layout.itemAt(1).widget()
                    button_hist = layout.itemAt(2).widget()
                else:
                    label1 = QLabel()
                    label2 = QLabel() 
                    button_verificar = QPushButton("Verificar")
                    button_hist = QPushButton("Hist")
                    layout = QHBoxLayout(tab_imagem) 
                    layout.addWidget(label1)
                    layout.addWidget(label2) 
                    layout.addWidget(button_verificar)
                    layout.addWidget(button_hist)
                    layout.setAlignment(Qt.AlignLeft)
                break
        else:
            # se nao exister criar a widget e colocar os mesmo botoes
            tab_imagem = QWidget()
            layout = QHBoxLayout(tab_imagem) 
            label1 = QLabel()
            label2 = QLabel() 
            button_verificar = QPushButton("Verificar")
            button_hist = QPushButton("Hist")
            layout.addWidget(label1)
            layout.addWidget(label2) 
            layout.addWidget(button_verificar)
            layout.addWidget(button_hist)
            layout.setAlignment(Qt.AlignLeft)

            self.ui.tabWidget.addTab(tab_imagem, "IMG")

        try:
            # Carrega a imagem , na qual sofreu o janelamento dos tons de cinza que escolhemos o max e min
            pixmap1 = QPixmap('App/Imagens/temp.png')
            pixmap1 = pixmap1.scaled(self.ui.tabWidget.width() // 3, self.ui.tabWidget.height() // 1)
            label1.setMaximumWidth(self.ui.tabWidget.width() // 3)
            label1.setMaximumHeight(self.ui.tabWidget.height() // 1)
            label1.setPixmap(pixmap1)
            label1.setStyleSheet("border: none;")
            button_verificar.setMaximumWidth(label1.maximumWidth())
            button_hist.setMaximumWidth(label1.maximumWidth())
            
            # Carrega a imagem que sofreu a segmenta;ao de forma automaica
            pixmap2 = QPixmap('App/Imagens/automatica.png')
            pixmap2 = pixmap2.scaled(self.ui.tabWidget.width() // 3, self.ui.tabWidget.height() // 1)
            label2.setMaximumWidth(self.ui.tabWidget.width() // 3)
            label2.setMaximumHeight(self.ui.tabWidget.height() // 1)
            label2.setPixmap(pixmap2)
            label2.setStyleSheet("border: none;")
            
        except:
            label1.setText("Imagem não encontrada.")

        button_verificar.clicked.connect(self.on_botao_clicado)
        button_hist.clicked.connect(self.on_botao_hist_clicado)


        #no proximo aba chamada filtro  mostrar os filtros que utilizamos para aumentar a imagem e outros para verificar 
    def adicionarWidgetsNaAbaFiltros(self):
        # Encontra a aba "Filtros"
        for i in range(self.ui.tabWidget.count()):
            if self.ui.tabWidget.tabText(i) == "FILTROS":
                tab_imagem = self.ui.tabWidget.widget(i)
                layout = QHBoxLayout(tab_imagem)

                # criar o QComboBox para as escolhas
                comboBox = QComboBox()
                comboBox.setStyleSheet("background-color: rgb(151, 157, 172); color: black;")  # Texto preto


                comboBox.addItem("Esolha")
                comboBox.addItem("Binnarização")
                comboBox.addItem("Sobel")
                comboBox.addItem("Fourier")
                comboBox.addItem("Passa Baixa")
                comboBox.addItem("Remover Texto")
                layout.addWidget(comboBox)

                # criar os QLabels para as imagens 
                layout1 = QVBoxLayout()
                label1 = QLabel("")
                button_verificar1 = QPushButton("Verificar")
                button_verificar1.clicked.connect(lambda: self.mostrar_imagens(comboBox, label1))
                button_verificar1.hide()  
                button_hist1 = QPushButton("Hist")
                button_hist1.hide()  
                layout1.addWidget(label1)
                layout1.addWidget(button_verificar1)
                layout1.addWidget(button_hist1)

                layout2 = QVBoxLayout()
                label2 = QLabel("")
                button_verificar2 = QPushButton("Verificar")
                button_verificar2.clicked.connect(lambda: self.mostrar_imagens(comboBox, label2))
                button_verificar2.hide()  
                button_hist2 = QPushButton("Hist")
                button_hist2.hide()  
                layout2.addWidget(label2)
                layout2.addWidget(button_verificar2)
                layout2.addWidget(button_hist2)

                layout.addLayout(layout1)
                layout.addLayout(layout2)

                
                comboBox.currentIndexChanged.connect(lambda: self.mostrar_botoes(comboBox, label1, label2, button_verificar1, button_hist1, button_verificar2, button_hist2))

                tab_imagem.setLayout(layout)

    #funcao para ao ser clicado binarizar ele fazer a binarizacao da imagem
    def binarizaar(self):
        global img
        global l1, l2
        global intQual
        intQual = 1
        self.textbox = QLineEdit(self)
        self.enviar_button = QPushButton('Enviar', self)
        self.enviar_button.move(320, 20) 
        self.enviar_button.resize(80, 40)
        self.enviar_button.clicked.connect(self.on_enviar_clicked)
        l1 = label1
        l2 = label2
        self.textbox.move(20, 20)
        self.textbox.resize(280, 40)
        self.textbox.show()
        self.enviar_button.show()  # Mostrar o botão de envio
        self.textbox.setPlaceholderText("Digite o valor aqui")
        return

    def fazerSobel(self):
        global img
        ob = sobel(img)
        rr = ob.sobel_edge_detection
        return
    
    def fazerPassaBaixa(self):
        global img
        objeto_fourier = passaBaixa(img,20)
        resultado = objeto_fourier.low_pass_filter
        return

    def fazerEqualizacao(self, img):
        img = cv2.imread(img, 0)
        equalized_img = cv2.equalizeHist(img)
        cv2.imwrite('App/Raio-X/Equalizada.png', equalized_img)
        return       

    def fazerEspelho(self, img):
        img = cv2.imread(img)
        rotated_img =np.rot90(img, 2)
        cv2.imwrite('App/Raio-X/Espelho.png', rotated_img)
        return

    


    def mostrar_botoes(self, comboBox, label1, label2, button_verificar1, button_hist1, button_verificar2, button_hist2):
        
        global img
        global l1, l2
        global intQual
        global fezerSobel
        global fezerBinarizacao
        global fazerForiier
        global fazerpassaBaixa

        if comboBox.currentText() == "Binnarização":
            intQual = 1
            fezerBinarizacao =1
            self.textbox = QLineEdit(self)
            self.enviar_button = QPushButton('Enviar', self)
            self.enviar_button.move(320, 20) 
            self.enviar_button.resize(80, 40)
            self.enviar_button.clicked.connect(self.on_enviar_clicked)
            l1 = label1
            l2 = label2
            self.textbox.move(20, 20)
            self.textbox.resize(280, 40)
            self.textbox.show()
            self.enviar_button.show() 

        elif comboBox.currentText() == "Sobel":
            fezerSobel=1
            ob = sobel(img)
            rr = ob.sobel_edge_detection
            self.mostrar_imagens("App/Raio-X/Sobel.png", img, label1, label2)
            button_verificar1.hide()
            button_hist1.hide()
            button_verificar2.hide()
            button_hist2.hide()

        elif comboBox.currentText() == "Fourier":
                fazerForiier =1
                objeto_fourier = fourier(img)
                resultado = objeto_fourier.fazerfori
                self.mostrar_imagens("App/Raio-X/EspectroFourier.png", "App/Raio-X/ImgFourier.png", label1, label2)
                button_verificar1.hide()
                button_hist1.hide()
                button_verificar2.hide()
                button_hist2.hide()

        elif comboBox.currentText() == "Remover Texto":
                
                removTexto= removerTexto(img)
                resultado=removTexto.fazerRemoção
                self.mostrar_imagens("App/Raio-X/SemTexto.png", img, label1, label2)
                button_verificar1.hide()
                button_hist1.hide()
                button_verificar2.hide()
                button_hist2.hide()


        elif comboBox.currentText() == "Passa Baixa":
                intQual = 2
                fazerpassaBaixa =1
                self.textbox = QLineEdit(self)
                self.enviar_button = QPushButton('Enviar', self)
                self.enviar_button.move(320, 20)  
                self.enviar_button.resize(80, 40)
                self.enviar_button.clicked.connect(self.on_enviar_clicked)
                l1 = label1
                l2 = label2
                self.textbox.move(20, 20)
                self.textbox.resize(280, 40)
                self.textbox.show()
                self.enviar_button.show()  
                self.textbox.setPlaceholderText("Digite o valor aqui")

        else:
           
            if hasattr(self, 'textbox'):
                self.textbox.hide()
                self.textbox.deleteLater()
                del self.textbox
            if hasattr(self, 'enviar_button'):
                self.enviar_button.hide()
                self.enviar_button.deleteLater()
                del self.enviar_button




    # Funcao para chamada quando o botão de envio for clicado
    def on_enviar_clicked(self):
        global l1, l2, intQual, img
        print(intQual)
        if intQual==1:
            valor = int(self.textbox.text())
            binarizador = binaria(img, valor) 
            self.mostrar_imagens("App/Raio-X/binary_image.png","App/Raio-X/R.png", l1, l2)
        else:
            valor = int(self.textbox.text())
            objeto_fourier = passaBaixa(img,valor)
            resultado = objeto_fourier.low_pass_filter
            self.mostrar_imagens("App/Raio-X/PassaBaixa.png","App/Raio-X/R.png", l1, l2)
        #button_verificar1.show()
        #button_hist1.show()
        #button_verificar2.show()
        #button_hist2.show()

    #Funcao para redimensionar a imagem com base no label
    def mostrar_imagens(self, imagem1, imagem2, label1, label2):
       
        pixmap1 = QPixmap(imagem1)
        pixmap2 = QPixmap(imagem2)
        pixmap1 = pixmap1.scaled(self.ui.tabWidget.width() // 3, self.ui.tabWidget.height() // 1)
        pixmap2 = pixmap2.scaled(self.ui.tabWidget.width() // 3, self.ui.tabWidget.height() // 1)
        label1.setMaximumWidth(self.ui.tabWidget.width() // 3)
        label1.setMaximumHeight(self.ui.tabWidget.height() // 1)
        label1.setPixmap(pixmap1)
        label1.setStyleSheet("border: none;")
        label2.setMaximumWidth(self.ui.tabWidget.width() // 3)
        label2.setMaximumHeight(self.ui.tabWidget.height() // 1)
        label2.setPixmap(pixmap2)
        label2.setStyleSheet("border: none;")

        # 
        #button_verificar.setMaximumWidth(label1.maximumWidth())
        #button_hist.setMaximumWidth(label1.maximumWidth())


        #fncao para mostrar o histograma
    def on_botao_hist_clicado(self):
        img = cv2.imread('App/Imagens/temp.png', cv2.IMREAD_GRAYSCALE)
        #hist = cv2.calcHist([img], [0], None, [256], [0, 256])
        plt.hist(img.ravel(),256,[0,256])
        plt.show()

        #funcao para mostrar a imagem antes e depois
    def on_botao_clicado(self):
        global img
        msg_box = QMessageBox()
        msg_box.setText("Selecione o modo de exibição:")
        msg_box.addButton("Automático", QMessageBox.YesRole)
        msg_box.addButton("Não Automático", QMessageBox.NoRole)
        msg_box.exec_()
        resposta = msg_box.clickedButton().text()
        if resposta == "Automático":
            # Exibe a imagem automaticamente
            img1 = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
            scale_percent = 10 
            width = int(img1.shape[1] * scale_percent / 100)
            height = int(img1.shape[0] * scale_percent / 100)
            dim = (width, height)
            img1 = cv2.resize(img1, dim, interpolation=cv2.INTER_AREA)
            img2 = cv2.imread('App/Imagens/automatica.png', cv2.IMREAD_GRAYSCALE)
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
        elif resposta == "Não Automático":
            
            img1 = cv2.imread('App/Raio-X/R.png', cv2.IMREAD_GRAYSCALE)
            scale_percent = 10 
            width = int(img1.shape[1] * scale_percent / 100)
            height = int(img1.shape[0] * scale_percent / 100)
            dim = (width, height)
            img1 = cv2.resize(img1, dim, interpolation=cv2.INTER_AREA)
            img2 = cv2.imread('App/Imagens/temp.png', cv2.IMREAD_GRAYSCALE)
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
    
    
    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0).widget()
            if child is not None:
                child.deleteLater()

    def button1_clicked(self):
        global img
        global intQualPredicao
        intQualPredicao =4
        self.clearLayout(self.tab2Layout)

        hbox_main_layout = QHBoxLayout()
        removTexto= removerTexto(img)
        resultado=removTexto.fazerRemoção

        # Adiciona a QLabel com a imagem R.png à esquerda
        label = QLabel(self)
        pixmap = QPixmap("App/Raio-X/SemTexto.png")
        pixmap = pixmap.scaled(pixmap.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(pixmap)
        label.setScaledContents(True) # Esta linha garante que a imagem se ajuste ao tamanho do QLabel
        # Adiciona a QLabel ao layout principal
        hbox_main_layout.addWidget(label, 1)

        # Cria um layout vertical para os botões de filtro e outras opções
        vbox_layout = QVBoxLayout()

        self.filters = []
        filter_checkbox = QCheckBox("Sobel")
        filter_checkbox.setStyleSheet("QCheckBox { color: black; } QCheckBox::indicator:checked { color: black; }")
        filter_checkbox1 = QCheckBox("Passa Baixa")
        filter_checkbox1.setStyleSheet("QCheckBox { color: black; } QCheckBox::indicator:checked { color: black; }")
        filter_checkbox2 = QCheckBox("Equalizacao")
        filter_checkbox2.setStyleSheet("QCheckBox { color: black; } QCheckBox::indicator:checked { color: black; }")
        filter_checkbox3 = QCheckBox("Espelho")
        filter_checkbox3.setStyleSheet("QCheckBox { color: black; } QCheckBox::indicator:checked { color: black; }")
        vbox_layout.addWidget(filter_checkbox)
        vbox_layout.addWidget(filter_checkbox1)
        vbox_layout.addWidget(filter_checkbox2)
        vbox_layout.addWidget(filter_checkbox3)
        self.filters.append(filter_checkbox)
        self.filters.append(filter_checkbox1)
        self.filters.append(filter_checkbox2)
        self.filters.append(filter_checkbox3)

        # Adiciona a seleção de opções
        self.option1 = QRadioButton("Sem Texto")
        self.option1.setStyleSheet("QRadioButton { color: black; } QRadioButton::indicator:checked { color: black; }")
        self.option2 = QRadioButton("Com Texto")
        self.option2.setStyleSheet("QRadioButton { color: black; } QRadioButton::indicator:checked { color: black; }")
        vbox_layout.addWidget(self.option1)
        vbox_layout.addWidget(self.option2)

        # Adiciona o botão para enviar as seleções
        send_button = QPushButton("Predicao")
        send_button.setStyleSheet("QPushButton { color: black; }")
        send_button.setFixedSize(100, 30)
        send_button.clicked.connect(self.send_selections)
        vbox_layout.addWidget(send_button, alignment=Qt.AlignBottom)

        # Adiciona as barras de progresso
        self.progress_bars = []
        roman_numerals = ["I", "II", "III", "IV"] # Números romanos
        for i in range(4):
            roman_label = QLabel(roman_numerals[i]) # QLabel para o número romano
            vbox_layout.addWidget(roman_label, alignment=Qt.AlignLeft) # Adiciona o QLabel ao layout vertical
            progress_bar = QProgressBar(self)
            progress_bar.setFixedSize(500, 40)
            vbox_layout.addWidget(progress_bar) # Adiciona a barra de progresso ao layout vertical
            self.progress_bars.append(progress_bar)

        # Adiciona o layout vertical ao layout horizontal principal
        hbox_main_layout.addLayout(vbox_layout, 1)

        # Adiciona o layout horizontal ao layout principal da terceira aba
        self.tab2Layout.addLayout(hbox_main_layout)







        

    def button2_clicked(self):
        global img
        global intQualPredicao
        intQualPredicao =2
        self.clearLayout(self.tab2Layout)

        # Cria um layout horizontal para a estrutura principal
        hbox_main_layout = QHBoxLayout()
        removTexto= removerTexto(img)
        resultado=removTexto.fazerRemoção

        # Adiciona a QLabel com a imagem R.png à esquerda
        label = QLabel(self)
        pixmap = QPixmap("App/Raio-X/SemTexto.png")
        # ajuste o tamanho do pixmap para corresponder à altura da janela
        pixmap = pixmap.scaled(pixmap.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(pixmap)
        label.setScaledContents(True) # Esta linha garante que a imagem se ajuste ao tamanho do QLabel
        # Adiciona a QLabel ao layout principal
        hbox_main_layout.addWidget(label, 1)

        # Cria um layout vertical para os botões de filtro e outras opções
        vbox_layout = QVBoxLayout()

        self.filters = []
        filter_checkbox = QCheckBox("Sobel")
        filter_checkbox.setStyleSheet("QCheckBox { color: black; } QCheckBox::indicator:checked { color: black; }")
        filter_checkbox1 = QCheckBox("Passa Baixa")
        filter_checkbox1.setStyleSheet("QCheckBox { color: black; } QCheckBox::indicator:checked { color: black; }")
        filter_checkbox2 = QCheckBox("Equalizacao")
        filter_checkbox2.setStyleSheet("QCheckBox { color: black; } QCheckBox::indicator:checked { color: black; }")
        filter_checkbox3 = QCheckBox("Espelho")
        filter_checkbox3.setStyleSheet("QCheckBox { color: black; } QCheckBox::indicator:checked { color: black; }")
        vbox_layout.addWidget(filter_checkbox)
        vbox_layout.addWidget(filter_checkbox1)
        vbox_layout.addWidget(filter_checkbox2)
        vbox_layout.addWidget(filter_checkbox3)
        self.filters.append(filter_checkbox)
        self.filters.append(filter_checkbox1)
        self.filters.append(filter_checkbox2)
        self.filters.append(filter_checkbox3)

        # Adiciona a seleção de opções
        self.option1 = QRadioButton("Sem Texto")
        self.option1.setStyleSheet("QRadioButton { color: black; } QRadioButton::indicator:checked { color: black; }")
        self.option2 = QRadioButton("Com Texto")
        self.option2.setStyleSheet("QRadioButton { color: black; } QRadioButton::indicator:checked { color: black; }")
        vbox_layout.addWidget(self.option1)
        vbox_layout.addWidget(self.option2)

        # Adiciona o botão para enviar as seleções
        send_button = QPushButton("Predicao")
        send_button.setStyleSheet("QPushButton { color: black; }")
        send_button.setFixedSize(100, 30)
        send_button.clicked.connect(self.send_selections)
        vbox_layout.addWidget(send_button, alignment=Qt.AlignBottom)

        # Adiciona as barras de progresso
        self.progress_bars = []
        roman_numerals = ["  I + II", "III + IV"] # Números romanos
        for i in range(2):
            font = QFont()
            font.setPointSize(15)  
            roman_label = QLabel(roman_numerals[i]) # QLabel para o número romano
            roman_label.setFont(font)
            roman_label.setFixedSize(70, 50) 
            vbox_layout.addWidget(roman_label, alignment=Qt.AlignLeft) # Adiciona o QLabel ao layout vertical
            progress_bar = QProgressBar(self)
            progress_bar.setFixedSize(500, 40)
            vbox_layout.addWidget(progress_bar) # Adiciona a barra de progresso ao layout vertical
            self.progress_bars.append(progress_bar)

        # Adiciona o layout vertical ao layout horizontal principal
        hbox_main_layout.addLayout(vbox_layout, 1)

        # Adiciona o layout horizontal ao layout principal da terceira aba
        self.tab2Layout.addLayout(hbox_main_layout)

    


    def fazer4classes(self, filtros, texto):
        # Cria o dicionário de operações
        global img
        operations = {
            "Sobel": [self.fazerSobel(), "App/Raio-X/Sobel.png"],
            "Passa Baixa": [self.fazerPassaBaixa(), "App/Raio-X/PassaBaixa.png"],
            "Equalizacao": [self.fazerEqualizacao(img), "App/Raio-X/Equalizada.png"],
            "Espelho": [self.fazerEspelho(img), "App/Raio-X/Espelho.png"],
        }



        if texto == "Sem Texto":
            print("ak")
            model = tf.keras.models.load_model('App/IA/my_model_4SemTexto.h5')

            # Carregar e pré-processar a imagem de entrada
            img_path = img
            img = image.load_img(img_path, target_size=(224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)

            # Fazer a classificação da imagem
            predictions = model.predict(x)

            # Definir a ordem das classes
            classes = ["d", "e", "f", "g"]

            # Obter a classe prevista
            indice_previsto = np.argmax(predictions)
            classe_prevista = classes[indice_previsto]
            print('Classe prevista:', classe_prevista)

            # Printar as probabilidades de cada classe
            print("Probabilidades:")
            for i, classe in enumerate(classes):
                print(f"{classe}: {predictions[0][i]*100:.2f}%")

            # Retornar a classe prevista e as probabilidades
            return classe_prevista, {classe: predictions[0][i]*100 for i, classe in enumerate(classes)}
        elif texto =="Com Texto":
            model = tf.keras.models.load_model('App/IA/my_model_4.h5')

            # Carregar e pré-processar a imagem de entrada
            img_path = img
            img = image.load_img(img_path, target_size=(224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)

            # Fazer a classificação da imagem
            predictions = model.predict(x)

            # Definir a ordem das classes
            classes = ["d", "e", "f", "g"]

            # Obter a classe prevista
            indice_previsto = np.argmax(predictions)
            classe_prevista = classes[indice_previsto]
            print('Classe prevista:', classe_prevista)

            # Printar as probabilidades de cada classe
            print("Probabilidades:")
            for i, classe in enumerate(classes):
                print(f"{classe}: {predictions[0][i]*100:.2f}%")

            # Retornar a classe prevista e as probabilidades
            return classe_prevista, {classe: predictions[0][i]*100 for i, classe in enumerate(classes)}

        else:
            return None, {}

    def fazer2classes(self, filtros, texto):
        # Cria o dicionário de operações
        global img
        operations = {
            "Sobel": [self.fazerSobel(), "App/Raio-X/Sobel.png"],
            "Passa Baixa": [self.fazerPassaBaixa(), "App/Raio-X/PassaBaixa.png"],
            "Equalizacao": [self.fazerEqualizacao(img), "App/Raio-X/Equalizada.png"],
            "Espelho": [self.fazerEspelho(img), "App/Raio-X/Espelho.png"],
        }



        if texto == "Sem Texto":
            print("ak")
            model = tf.keras.models.load_model('App/IA/my_model_binarySemTexto.h5')

            # Carregar e pré-processar a imagem de entrada
            img_path = img
            img = image.load_img(img_path, target_size=(224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)

            predictions = model.predict(x)
            print("Previsões:", predictions)
            
            # Definir a ordem das classes
            classes = ["d e", "f g"]
            
            # Obter a probabilidade da classe 1
            prob_classe1 = predictions[0][0]

            # Probabilidade da classe 0
            prob_classe0 = 1 - prob_classe1

            # Obter a classe prevista
            classe_prevista = classes[0] if prob_classe0 > prob_classe1 else classes[1]

            print('Classe prevista:', classe_prevista)
            print("Probabilidades:")
            print(f"d e: {prob_classe0*100:.2f}%")
            print(f"f g: {prob_classe1*100:.2f}%")

        # Retornar a classe prevista e as probabilidades
            return classe_prevista, {classes[0]: prob_classe0*100, classes[1]: prob_classe1*100}
        elif texto =="Com Texto":
            model = tf.keras.models.load_model('App/IA/my_model_binary.h5')

            # Carregar e pré-processar a imagem de entrada
            img_path = img
            img = image.load_img(img_path, target_size=(224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)

            predictions = model.predict(x)
            print("Previsões:", predictions)
            
            # Definir a ordem das classes
            classes = ["d e", "f g"]
            
            # Obter a probabilidade da classe 1
            prob_classe1 = predictions[0][0]

            # Probabilidade da classe 0
            prob_classe0 = 1 - prob_classe1

            # Obter a classe prevista
            classe_prevista = classes[0] if prob_classe0 > prob_classe1 else classes[1]

            print('Classe prevista:', classe_prevista)
            print("Probabilidades:")
            print(f"d e: {prob_classe0*100:.2f}%")
            print(f"f g: {prob_classe1*100:.2f}%")

        # Retornar a classe prevista e as probabilidades
            return classe_prevista, {classes[0]: prob_classe0*100, classes[1]: prob_classe1*100}

        else:
            return None, {}


    def prepare_image_for_model(self,image, target_size=(224, 224)):
        # Redimensiona a imagem para o tamanho-alvo
        image = cv2.resize(image, target_size)
        
        # Normaliza os pixels para o intervalo [0, 1]
        image = image.astype('float32') / 255.0
        
        # Adiciona uma dimensão de lote
        image = np.expand_dims(image, axis=0)
        
        return image

    def send_selections(self):
        global intQualPredicao
        global porcentagemE
        global classeEscolhida
        selected_filters = [filter.text() for filter in self.filters if filter.isChecked()]
        selected_option = self.option1.text() if self.option1.isChecked() else self.option2.text() if self.option2.isChecked() else None
        if intQualPredicao == 4:
            classePrevista, probabilidade = self.fazer4classes(selected_filters,selected_option)
            print(classePrevista)
            print(probabilidade)

            # Obter as porcentagens das probabilidades
            percentages = list(probabilidade.values())
            porcentagemE =percentages 
            classeEscolhida=classePrevista
            self.update_progress_bars(percentages)
            return
        if intQualPredicao==2:
            classePrevista, probabilidade = self.fazer2classes(selected_filters,selected_option)
            print(classePrevista)
            print(probabilidade)
            print("aki")
            percentages = list(probabilidade.values())
            print(percentages)
            self.update_progress_bars(percentages)
            return
        else:
            percentages = [random.randint(0, 100) for _ in self.progress_bars]
            self.update_progress_bars(percentages)



    def update_progress_bars(self, percentages):
        for i, percentage in enumerate(percentages):
            self.progress_bars[i].setValue(percentage)
            self.progress_bars[i].setStyleSheet("""
            QProgressBar{
                border: 2px solid black;  /* Contorno preto */
                border-radius: 15px;
                background-color: #FFFFFF;
                padding: 1px;  /* Adiciona espaço ao redor da barra de progresso */
                text-align: center;
                color:black;
            }
            QProgressBar::chunk{
                border-radius: 15px;
                background-color: #0466C8;  /* Cor da barra de progresso */
                margin: 1px;  /* Adiciona espaço ao redor das "fatias" */
            }
            """)



    def setup_custom_tab(self):
        self.tab2Layout = QVBoxLayout()
        self.ui.tabWidget.widget(2).setLayout(self.tab2Layout)
        self.pushButton1 = QPushButton("4 classes")
        self.pushButton2 = QPushButton("Binaria")
        self.tab2Layout.addWidget(self.pushButton1)
        self.tab2Layout.addWidget(self.pushButton2)
        self.pushButton1.clicked.connect(self.button1_clicked)
        self.pushButton2.clicked.connect(self.button2_clicked)
        # Agora adicione seus widgets ao self.tab2Layout

   


    # funcao para verificar qual aba estamos e mandar a resposta para a funcao de cada aba
    def tab_changed(self):
        if(self.ui.tabWidget.currentIndex()==0):
            self.mudarAbaImagem()
        elif(self.ui.tabWidget.currentIndex()==1):
            self.adicionarWidgetsNaAbaFiltros()
        else:
            #print("Resultado")
            self.setup_custom_tab() 

    def teste(self):
        subwindow = SubWindow(self, img2=img)
        subwindow.show()

    def Mudar(self):
        print("")

    def Funcionamento(self):
        return


    def salvar(self):
        print("aki")
        global porcentagemE
        global classeEscolhida
        global img
        global fezerSobel
        global fezerBinarizacao
        global fazerForiier
        global fazerpassaBaixa

        print(img)
        print(classeEscolhida)
        print(porcentagemE)
        c = canvas.Canvas('meu_arquivo.pdf', pagesize=letter)
        width, height = letter

        # Título
        c.setFont("Helvetica", 20)
        title = "Trabalho final de PDI"
        title_width = c.stringWidth(title, "Helvetica", 20)
        c.drawString((width - title_width) / 2, height - 50, title)

        # Abrindo a imagem e adicionando-a ao PDF
        #img = Image.open(img)
        img.save('img.bmp')
        c.drawImage('img.bmp', 50, height - 350, width=400, height=300)
        c.setFont("Helvetica", 14)
        c.drawString(50, height - 360, "Imagem antes da segmentação")

        # Abrindo a segunda imagem e adicionando-a ao PDF
        img2 = Image.open('App/Raio-X/SemTexto.png')
        img2.save('App/Raio-X/SemTexto.bmp')
        c.drawImage('App/Raio-X/SemTexto.bmp', 50, height - 650, width=400, height=300)
        c.drawString(50, height - 660, "Imagem depois da segmentação")

        c.showPage()  # Cria uma nova página

        # Adicionando a classificação do grupo
        classeEscolhida = classeEscolhida
        c.setFont("Helvetica", 16)
        c.drawString(50, height - 50, "Classificação do Grupo")
        c.setFont("Helvetica", 14)
        c.drawString(50, height - 70, str(classeEscolhida))

        # Adicionando a sequência de números romanos
        porcentagemE = [porcentagemE[0], porcentagemE[1], porcentagemE[2], porcentagemE[3]]  # Substitua pelos valores reais
        numeros_romanos = ['I', 'II', 'III', 'IV']
        for i in range(4):
            c.drawString(50, height - 100 - i*20, f"{numeros_romanos[i]}: {porcentagemE[i]}%")

        if fazerForiier ==1: 
            c.showPage()
            img2 = Image.open('App/Raio-X/EspectroFourier.png')
            img2.save('App/Raio-X/EspectroFourier.bmp')
            c.drawImage('App/Raio-X/EspectroFourier.bmp', 50, height - 650, width=400, height=300)
            c.drawString(50, height - 660, "Espectro de Fourier")

        if fazerpassaBaixa ==1:
            c.showPage()
            img2 = Image.open('App/Raio-X/PassaBaixa.png')
            img2.save('App/Raio-X/PassaBaixa.bmp')
            c.drawImage('App/Raio-X/PassaBaixa.bmp', 50, height - 650, width=400, height=300)
            c.drawString(50, height - 660, "Passa Baixa")

        if fezerBinarizacao ==1:
            c.showPage()
            img2 = Image.open('App/Raio-X/binary_image.png')
            img2.save('App/Raio-X/binary_image.bmp')
            c.drawImage('App/Raio-X/binary_image.bmp', 50, height - 650, width=400, height=300)
            c.drawString(50, height - 660, "Binarização")

        if fezerSobel==1:
            c.showPage()
            img2 = Image.open('App/Raio-X/Sobel.png')
            img2.save('App/Raio-X/Sobel.bmp')
            c.drawImage('App/Raio-X/Sobel.bmp', 50, height - 650, width=400, height=300)
            c.drawString(50, height - 660, "Soble")



        # Adicionando os nomes
        c.setFont("Helvetica", 14)
        c.drawString(50, height - 200, "Eric Azevedo")
        c.drawString(50, height - 220, "Bran")
        c.drawString(50, height - 240, "Alexeis")
        print(3)

       

        
        # Salvando o PDF
        c.save()





    def Pontos(self):    
        logo = Logo(self)
        logo.show()

    def escreverArquivo(self,train):
        with open("nomeTest1.txt", 'w') as arquivo:
            for item in train:
                arquivo.write(str(item) + '\n')

    def Colaboradores(self):
        global train , test
        #self.janela = Janela(self)
        #self.janela.show()
        ld=LeituraDiretorio(QFileDialog.getExistingDirectory(self, "Selecione o diretório"))
        train=ld.train
        test=ld.test
        print("1-------")
        self.escreverArquivo(test) 
        #AumentarDados(train)
        #print(test[1])
        print("fim")


    

    def File(self):
        global img
        fileName, _ = QFileDialog.getOpenFileName(self, "")
        if fileName:
           img = fileName

    #funcao para fazer a lmizlizacao automatica
    def automatica(self):
        global img
        img1 = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
        img1 = cv2.resize(img1, (800, 800))
        for i in range(4):
            img1 = cv2.rotate(img1, cv2.ROTATE_90_COUNTERCLOCKWISE)

        #pegar o histograma entre 0 e 256
        hist, bins = np.histogram(img1.ravel(), 256, [0, 256])

        #verificar a quantidade de pixel
        total_pixels = img1.shape[0] * img1.shape[1]
   
        w0 = 0
        sum0 = 0
        mean0 = 0
        max_var = 0
        threshold = 0

        # testar os valores
        for t in range(256):
            w1 = total_pixels - w0
            if w1 == 0:
                break
            sum1 = sum(hist[t+1:] * np.arange(t+1, 256))
            mean1 = sum1 / w1
            if w0 == 0:
                mean0 = 0 
            else:
                mean0 = sum0 / w0
            var_between = w0 * w1 * (mean0 - mean1) ** 2
            if var_between > max_var:
                max_var = var_between
                threshold = t
            w0 += hist[t]
            sum0 += t * hist[t]

        # fazer a automatica
        img_threshold = np.zeros_like(img1)
        img_threshold[img1 > threshold] = 255

        contours, _ = cv2.findContours(img_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour = max(contours, key=cv2.contourArea)

        # fazer uma mascara com base na resultate da automatica
        mask = np.zeros_like(img_threshold)

        # desenhar o contorno para colocar a imagem que esta dentro em branco
        cv2.drawContours(mask, [contour], 0, 255, -1)

        # colocar branco dentro da imagem com base no desenho do contorno 
        mask[mask == 255] = 1
        result = img1 * mask
        result[result > 0] = 255
        cv2.imwrite('App/Imagens/automatica.png', result)

     # mostrar innformacaos do modeo   
    def mostrarSumario(self):
        msg_box = QMessageBox()
        msg_box.setText("Qual sumario de modelo quer ver ")
        msg_box.addButton("Sumario classificação binaria", QMessageBox.YesRole)
        msg_box.addButton("Sumario classificação entre 4", QMessageBox.NoRole)
        msg_box.exec_()

        resposta = msg_box.clickedButton().text()
        if resposta=="Sumario classificação binaria":
            print("binaria")
            caminho_arquivo = "App/IA/model_Binaria.txt"
            dialogo = MostrarTxt(caminho_arquivo)
            dialogo.exec()
        elif resposta =="Sumario classificação entre 4":
            print("4 classes")
            caminho_arquivo = "App/IA/model_4classes.txt"
            dialogo = MostrarTxt(caminho_arquivo)
            dialogo.exec()
               
        return
    

    def comAnotacoes(self, horas, minutos, acuracia, precisao, recall, f1_score, sensibilidade, especificidade):
        dialog = QDialog()
        dialog.setWindowTitle("Métricas")
        layout = QVBoxLayout(dialog)
        
        label_tempo_aprendizado = QLabel(f'Tempo de Aprendizado: {horas:02d} horas e {minutos:02d} minutos')
        layout.addWidget(label_tempo_aprendizado)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)
        
        label_acuracia = QLabel(f"Acurácia: {acuracia}")
        layout.addWidget(label_acuracia)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)
        
        label_precisao = QLabel(f"Precisão: {precisao}")
        layout.addWidget(label_precisao)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)
        
        label_recall = QLabel(f"Recall: {recall}")
        layout.addWidget(label_recall)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)
        
        label_f1_score = QLabel(f"F1 Score: {f1_score}")
        layout.addWidget(label_f1_score)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)
        
        label_sensibilidade = QLabel(f"Sensibilidade: {sensibilidade}")
        layout.addWidget(label_sensibilidade)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)
        
        label_especificidade = QLabel(f"Especificidade: {especificidade}")
        layout.addWidget(label_especificidade)
        
        dialog.setLayout(layout)
        dialog.exec()
       

    def qualMetricasBina(self):
        msg_box = QMessageBox()
        msg_box.setText("Qual Metrica do das magens voce quer ")
        msg_box.addButton("Metricas Sem as Anotacoes", QMessageBox.YesRole)
        msg_box.addButton("Metricas Com as Anotacoes", QMessageBox.NoRole)
        msg_box.exec_()
        resposta = msg_box.clickedButton().text()
        if resposta=="Metricas Sem as Anotacoes":
            self.comAnotacoes(9,3,0.600160256410264, 0.5874125874125874, 0.6730769230769231, 0.6273338312173264, 0.6730769230769231, 0.5272435897435898)
            
        elif resposta =="Metricas Com as Anotacoes":
           self.comAnotacoes(12,17,0.5095338983050848, 0.5050840276797063, 0.947166313559322, 0.6588376162844247, 0.947166313559322, 0.07190148305084745)

        return
    
    # mostrar innformacaos do modeo 
    def mostrarMetricas(self):
        msg_box = QMessageBox()
        msg_box.setText("Qual Metrica de Modelo voce quer ")
        msg_box.addButton("Metricas da classificação binaria", QMessageBox.YesRole)
        msg_box.addButton("Metricas da classificação entre 4", QMessageBox.NoRole)
        msg_box.exec_()

        resposta = msg_box.clickedButton().text()
        if resposta=="Metricas da classificação binaria":
            self.qualMetricasBina()
        elif resposta =="Metriicas da classificação entre 4":
            print("4 classes")
                   
        return
    #quando apertar no botao ele vira para essa funcao
    def IaMostrar(self):
        msg_box = QMessageBox()
        msg_box.setText("Selecione o que quer ver")
        msg_box.addButton("Sumario da IA", QMessageBox.YesRole)
        msg_box.addButton("Matricas", QMessageBox.NoRole)
        msg_box.exec_()

        resposta = msg_box.clickedButton().text()
        if resposta == "Sumario da IA":
            self.mostrarSumario()

        elif resposta == "Matricas":
            self.mostrarMetricas()
            if __name__ == "__main__":
                app = QApplication(sys.argv)
                widget = MainWindow()

                widget.show()
                sys.exit(app.exec())










