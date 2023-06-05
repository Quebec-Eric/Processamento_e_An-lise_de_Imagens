import sys

sys.path.append('App/Imports')

from Imports import *
from PIL import Image
from App.Curso.Logo import Logo
from App.Colaboradores.JanelaColaboradores import Janela
from App.JanelaCinza.JanelaSeg import SubWindow
from App.PreparativosRede.PreProcessamentoImagens.LerDiretoriosIMg import LeituraDiretorio
from App.PreparativosRede.PreProcessamentoImagens.AumentandoDados import AumentarDados
from App.Mascaras.Binarização.binaria import binaria
from App.Mascaras.Fourier.fourier import fourier
from App.Mascaras.Fourier.passaBaixa import passaBaixa
from App.Mascaras.Bordas.sobel import sobel
from App.Mascaras.RemoverTexto.removerTexto import removerTexto
import cv2
from App.IA.MostrarTxt import MostrarTxt
import numpy as np
import os
import shutil

img = None
intQual=0
train = []
l1=None
l2=None
test = []
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
        self.automatica()
        # Encontra ou cria o widget de imagem
        for i in range(self.ui.tabWidget.count()):
            if self.ui.tabWidget.tabText(i) == "IMG":
                tab_imagem = self.ui.tabWidget.widget(i)
                layout = tab_imagem.layout()
                if layout is not None:
                    label1 = layout.itemAt(0).widget()
                    label2 = QLabel() # Novo QLabel para a segunda imagem
                    button_verificar = layout.itemAt(1).widget()
                    button_hist = layout.itemAt(2).widget()
                else:
                    label1 = QLabel()
                    label2 = QLabel() # Novo QLabel para a segunda imagem
                    button_verificar = QPushButton("Verificar")
                    button_hist = QPushButton("Hist")
                    layout = QHBoxLayout(tab_imagem) # Alteração do QVBoxLayout para QHBoxLayout
                    layout.addWidget(label1)
                    layout.addWidget(label2) # Adiciona o novo QLabel
                    layout.addWidget(button_verificar)
                    layout.addWidget(button_hist)
                    layout.setAlignment(Qt.AlignLeft)
                break
        else:
            tab_imagem = QWidget()
            layout = QHBoxLayout(tab_imagem) # Alteração do QVBoxLayout para QHBoxLayout
            label1 = QLabel()
            label2 = QLabel() # Novo QLabel para a segunda imagem
            button_verificar = QPushButton("Verificar")
            button_hist = QPushButton("Hist")
            layout.addWidget(label1)
            layout.addWidget(label2) # Adiciona o novo QLabel
            layout.addWidget(button_verificar)
            layout.addWidget(button_hist)
            layout.setAlignment(Qt.AlignLeft)

            self.ui.tabWidget.addTab(tab_imagem, "IMG")

        try:
            # Carrega a primeira imagem e configura o primeiro QLabel
            pixmap1 = QPixmap('App/Imagens/temp.png')
            pixmap1 = pixmap1.scaled(self.ui.tabWidget.width() // 3, self.ui.tabWidget.height() // 1)
            label1.setMaximumWidth(self.ui.tabWidget.width() // 3)
            label1.setMaximumHeight(self.ui.tabWidget.height() // 1)
            label1.setPixmap(pixmap1)
            label1.setStyleSheet("border: none;")
            button_verificar.setMaximumWidth(label1.maximumWidth())
            button_hist.setMaximumWidth(label1.maximumWidth())
            
            # Carrega a segunda imagem e configura o segundo QLabel
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


        
    def adicionarWidgetsNaAbaFiltros(self):
        # Encontra a aba "Filtros"
        for i in range(self.ui.tabWidget.count()):
            if self.ui.tabWidget.tabText(i) == "Filtros":
                tab_imagem = self.ui.tabWidget.widget(i)
                layout = QHBoxLayout(tab_imagem)

                # Criação do QComboBox para as escolhas
                comboBox = QComboBox()
                comboBox.addItem("Esolha")
                comboBox.addItem("Binnarização")
                comboBox.addItem("Sobel")
                comboBox.addItem("Fourier")
                comboBox.addItem("Passa Baixa")
                comboBox.addItem("Remover Texto")
                layout.addWidget(comboBox)

                # Criação dos QLabels para as imagens e botões
                layout1 = QVBoxLayout()
                label1 = QLabel("Label 1")
                button_verificar1 = QPushButton("Verificar")
                button_verificar1.clicked.connect(lambda: self.mostrar_imagens(comboBox, label1))
                button_verificar1.hide()  # O botão fica inicialmente oculto
                button_hist1 = QPushButton("Hist")
                button_hist1.hide()  # O botão fica inicialmente oculto
                layout1.addWidget(label1)
                layout1.addWidget(button_verificar1)
                layout1.addWidget(button_hist1)

                layout2 = QVBoxLayout()
                label2 = QLabel("Label 2")
                button_verificar2 = QPushButton("Verificar")
                button_verificar2.clicked.connect(lambda: self.mostrar_imagens(comboBox, label2))
                button_verificar2.hide()  # O botão fica inicialmente oculto
                button_hist2 = QPushButton("Hist")
                button_hist2.hide()  # O botão fica inicialmente oculto
                layout2.addWidget(label2)
                layout2.addWidget(button_verificar2)
                layout2.addWidget(button_hist2)

                layout.addLayout(layout1)
                layout.addLayout(layout2)

                # Conecta o sinal de mudança de index do comboBox ao slot que mostra os botões
                comboBox.currentIndexChanged.connect(lambda: self.mostrar_botoes(comboBox, label1, label2, button_verificar1, button_hist1, button_verificar2, button_hist2))

                tab_imagem.setLayout(layout)


    def binarizaar(self):
        global img
        global l1, l2
        global intQual
        intQual = 1
        # Adicione esta linha para criar um QLineEdit (caixa de texto)
        self.textbox = QLineEdit(self)

            # Adicione esta linha para criar um botão de envio
        self.enviar_button = QPushButton('Enviar', self)
        self.enviar_button.move(320, 20)  # Mova e dimensione o botão conforme necessário
        self.enviar_button.resize(80, 40)

            # Conecte o botão a uma função
        self.enviar_button.clicked.connect(self.on_enviar_clicked)

            # Mostrar o QLineEdit
        l1 = label1
        l2 = label2
        self.textbox.move(20, 20)
        self.textbox.resize(280, 40)
        self.textbox.show()
        self.enviar_button.show()  # Mostrar o botão de envio

            # Defina um texto informativo
        self.textbox.setPlaceholderText("Digite o valor aqui")
    
    def mostrar_botoes(self, comboBox, label1, label2, button_verificar1, button_hist1, button_verificar2, button_hist2):
        # Mostra os botões e as imagens correspondentes dependendo da escolha
        global img
        global l1, l2
        global intQual

        if comboBox.currentText() == "Binnarização":
            intQual = 1
            # Adicione esta linha para criar um QLineEdit (caixa de texto)
            self.textbox = QLineEdit(self)

                # Adicione esta linha para criar um botão de envio
            self.enviar_button = QPushButton('Enviar', self)
            self.enviar_button.move(320, 20)  # Mova e dimensione o botão conforme necessário
            self.enviar_button.resize(80, 40)

                # Conecte o botão a uma função
            self.enviar_button.clicked.connect(self.on_enviar_clicked)

                # Mostrar o QLineEdit
            l1 = label1
            l2 = label2
            self.textbox.move(20, 20)
            self.textbox.resize(280, 40)
            self.textbox.show()
            self.enviar_button.show()  # Mostrar o botão de envio

        elif comboBox.currentText() == "Sobel":
            ob = sobel(img)
            rr = ob.sobel_edge_detection
            self.mostrar_imagens("App/Raio-X/Sobel.png", img, label1, label2)
            button_verificar1.hide()
            button_hist1.hide()
            button_verificar2.hide()
            button_hist2.hide()

        elif comboBox.currentText() == "Fourier":
                objeto_fourier = fourier(img)
                resultado = objeto_fourier.fazerfori
                self.mostrar_imagens("App/Raio-X/EspectroFourier.png", "App/Raio-X/ImgFourier.png", label1, label2)
                button_verificar1.hide()
                button_hist1.hide()
                button_verificar2.hide()
                button_hist2.hide()

        elif comboBox.currentText() == "Remover Texto":
                objeto_fourier = fourier(img)
                resultado = objeto_fourier.fazerfori
                removTexto= removerTexto(img)
                resultado=removTexto.fazerRemoção
                self.mostrar_imagens("App/Raio-X/SemTexto.png", img, label1, label2)
                button_verificar1.hide()
                button_hist1.hide()
                button_verificar2.hide()
                button_hist2.hide()


        elif comboBox.currentText() == "Passa Baixa":
                intQual = 2
                # Adicione esta linha para criar um QLineEdit (caixa de texto)
                self.textbox = QLineEdit(self)

                # Adicione esta linha para criar um botão de envio
                self.enviar_button = QPushButton('Enviar', self)
                self.enviar_button.move(320, 20)  # Mova e dimensione o bot conforme necessário
                self.enviar_button.resize(80, 40)

                # Conecte o botão a uma função
                self.enviar_button.clicked.connect(self.on_enviar_clicked)

                # Mostrar o QLineEdit
                l1 = label1
                l2 = label2
                self.textbox.move(20, 20)
                self.textbox.resize(280, 40)
                self.textbox.show()
                self.enviar_button.show()  # Mostrar o botão de envio

                # Defina um texto informativo
                self.textbox.setPlaceholderText("Digite o valor aqui")

        else:
            # Esconder o QLineEdit e o botão de envio, se estiverem visíveis
            if hasattr(self, 'textbox'):
                self.textbox.hide()
                self.textbox.deleteLater()
                del self.textbox
            if hasattr(self, 'enviar_button'):
                self.enviar_button.hide()
                self.enviar_button.deleteLater()
                del self.enviar_button




    # Função que será chamada quando o botão de envio for clicado
    def on_enviar_clicked(self):
        global l1, l2, intQual, img
        print(intQual)
        # Obtenha o valor do QLineEdit quando o botão é pressionado
        if intQual==1:
            valor = int(self.textbox.text())
            binarizador = binaria(img, valor)  # Usar o valor na função binaria
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


    def mostrar_imagens(self, imagem1, imagem2, label1, label2):
        # Carrega as imagens
        pixmap1 = QPixmap(imagem1)
        pixmap2 = QPixmap(imagem2)

        # Redimensiona os pixmaps para caberem dentro do tamanho do QLabel, mantendo a proporção da imagem.
        pixmap1 = pixmap1.scaled(self.ui.tabWidget.width() // 3, self.ui.tabWidget.height() // 1)
        pixmap2 = pixmap2.scaled(self.ui.tabWidget.width() // 3, self.ui.tabWidget.height() // 1)

        # Define o tamanho máximo para os labels e aplica os pixmaps
        label1.setMaximumWidth(self.ui.tabWidget.width() // 3)
        label1.setMaximumHeight(self.ui.tabWidget.height() // 1)
        label1.setPixmap(pixmap1)
        label1.setStyleSheet("border: none;")

        label2.setMaximumWidth(self.ui.tabWidget.width() // 3)
        label2.setMaximumHeight(self.ui.tabWidget.height() // 1)
        label2.setPixmap(pixmap2)
        label2.setStyleSheet("border: none;")

        # Define o tamanho máximo para os botões
        #button_verificar.setMaximumWidth(label1.maximumWidth())
        #button_hist.setMaximumWidth(label1.maximumWidth())


        
    def on_botao_hist_clicado(self):
        img = cv2.imread('App/Imagens/temp.png', cv2.IMREAD_GRAYSCALE)
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
        global img
        # Cria um diálogo de mensagem com dois botões
        msg_box = QMessageBox()
        msg_box.setText("Selecione o modo de exibição:")
        msg_box.addButton("Automático", QMessageBox.YesRole)
        msg_box.addButton("Não Automático", QMessageBox.NoRole)
        msg_box.exec_()
        
        # Obtém a resposta do usuário
        resposta = msg_box.clickedButton().text()

        # Exibe a imagem de acordo com a resposta do usuário
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
                # Exibe a imagem automaticamente
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
        


        

    def tab_changed(self):
        if(self.ui.tabWidget.currentIndex()==0):
            self.mudarAbaImagem()
        elif(self.ui.tabWidget.currentIndex()==1):
            self.adicionarWidgetsNaAbaFiltros()
        else:
            print("Resultado") 

    def teste(self):
        subwindow = SubWindow(self, img2=img)
        subwindow.show()

    def Mudar(self):
        print("")

    def Funcionamento(self):
        return

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

    def automatica(self):
        global img
        img1 = cv2.imread(img, cv2.IMREAD_GRAYSCALE)

        # Redimensionar a imagem para 800x800 pixels
        img1 = cv2.resize(img1, (800, 800))

        # Rotacionar a imagem 90 graus no sentido horário

        for i in range(4):
            img1 = cv2.rotate(img1, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # Histograma da imagem
        hist, bins = np.histogram(img1.ravel(), 256, [0, 256])

        # Total de pixels na imagem
        total_pixels = img1.shape[0] * img1.shape[1]

        # Inicializar variáveis
        w0 = 0
        sum0 = 0
        mean0 = 0
        max_var = 0
        threshold = 0

        # Iterar sobre os possíveis valores de limiar
        for t in range(256):
            w1 = total_pixels - w0
            if w1 == 0:
                break
            sum1 = sum(hist[t+1:] * np.arange(t+1, 256))
            mean1 = sum1 / w1
            if w0 == 0:
                mean0 = 0 # Ou algum outro valor padrão
            else:
                mean0 = sum0 / w0
            var_between = w0 * w1 * (mean0 - mean1) ** 2
            if var_between > max_var:
                max_var = var_between
                threshold = t
            w0 += hist[t]
            sum0 += t * hist[t]

        # Limiarização da imagem
        img_threshold = np.zeros_like(img1)
        img_threshold[img1 > threshold] = 255

        contours, _ = cv2.findContours(img_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour = max(contours, key=cv2.contourArea)

        # Cria uma máscara que cobre toda a imagem
        mask = np.zeros_like(img_threshold)

        # Desenha o contorno da mama na máscara
        cv2.drawContours(mask, [contour], 0, 255, -1)

        # Preenche a região interna da mama com branco
        mask[mask == 255] = 1
        result = img1 * mask
        result[result > 0] = 255
        cv2.imwrite('App/Imagens/automatica.png', result)

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

    def mostrarMetricas():
        msg_box = QMessageBox()
        msg_box.setText("Qual Metrica de Modelo voce quer ")
        msg_box.addButton("Metricas da classificação binaria", QMessageBox.YesRole)
        msg_box.addButton("Metricas da classificação entre 4", QMessageBox.NoRole)
        msg_box.exec_()

        resposta = msg_box.clickedButton().text()
        if resposta=="Metricas da classificação binaria":
            print("Binaria")
        elif resposta =="Metriicas da classificação entre 4":
            print("4 classes")
                   
        return

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
            matricas_box = QMessageBox()
            matricas_box.setText("Selecione o que quer ver")
            matricas_box.addButton("Classificação binaria", QMessageBox.YesRole)
            matricas_box.addButton("Classificação de 4 classes", QMessageBox.NoRole)
            matricas_box.exec_()
    






