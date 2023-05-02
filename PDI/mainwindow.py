import sys

sys.path.append('App/Imports')

from Imports import *
from App.Curso.Logo import Logo
from App.Colaboradores.JanelaColaboradores import Janela
from App.JanelaCinza.JanelaSeg import SubWindow
from App.PreparativosRede.PreProcessamentoImagens.LerDiretoriosIMg import LeituraDiretorio
from App.PreparativosRede.PreProcessamentoImagens.AumentandoDados import AumentarDados
import cv2
import numpy as np
img = None
train = []
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
            img1 = cv2.imread('App/Raio-X/R.png', cv2.IMREAD_GRAYSCALE)
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
            print("Matrix")
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


    def Colaboradores(self):
        global train , test
        #self.janela = Janela(self)
        #self.janela.show()
        ld=LeituraDiretorio(QFileDialog.getExistingDirectory(self, "Selecione o diretório"))
        train=ld.train
        test=ld.test
        print("1-------")
        #print(train[1])
        AumentarDados(train)
        

    def File(self):
        global img
        fileName, _ = QFileDialog.getOpenFileName(self, "")
        if fileName:
           img = fileName

    def automatica(self):
        img = cv2.imread('App/Raio-X/R.png', cv2.IMREAD_GRAYSCALE)

        # Redimensionar a imagem para 800x800 pixels
        img = cv2.resize(img, (800, 800))

        # Rotacionar a imagem 90 graus no sentido horário

        for i in range(4):
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # Histograma da imagem
        hist, bins = np.histogram(img.ravel(), 256, [0, 256])

        # Total de pixels na imagem
        total_pixels = img.shape[0] * img.shape[1]

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
        img_threshold = np.zeros_like(img)
        img_threshold[img > threshold] = 255

        contours, _ = cv2.findContours(img_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour = max(contours, key=cv2.contourArea)

        # Cria uma máscara que cobre toda a imagem
        mask = np.zeros_like(img_threshold)

        # Desenha o contorno da mama na máscara
        cv2.drawContours(mask, [contour], 0, 255, -1)

        # Preenche a região interna da mama com branco
        mask[mask == 255] = 1
        result = img * mask
        result[result > 0] = 255
        cv2.imwrite('App/Imagens/automatica.png', result)




