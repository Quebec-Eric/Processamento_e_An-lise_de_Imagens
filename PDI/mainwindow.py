import sys

sys.path.append('App/Imports')

from Imports import *
from App.Curso.Logo import Logo
from App.JanelaCinza.JanelaSeg import SubWindow

img = None
 
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

            pixmap = QPixmap('App/Imagens/temp.png')
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
            img1 = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
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
        self.janela = Janela(self)
        self.janela.show()
        
    def File(self):
        global img
        fileName, _ = QFileDialog.getOpenFileName(self, "")
        if fileName:
           img = fileName



