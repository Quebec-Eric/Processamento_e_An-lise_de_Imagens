#Pontifícia Universidade Católica de Minas Gerais (Campus Coração Eucarístico)
#Ciência da Computação
#Bryan Jonathan Melo De Oliveira - 708688
#Eric Azevedo de Oliveira - 1269480
#João Gabriel Sena Fernandes - 1209882

from PyQt6.QtWidgets import QDialog, QTextEdit, QVBoxLayout

class MostrarTxt(QDialog):
    def __init__(self, caminho_arquivo):
        super().__init__()

        self.setWindowTitle("Conteúdo do Arquivo")

        # Criar o widget QTextEdit para exibir o texto do arquivo
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        # Ler o conteúdo do arquivo
        with open(caminho_arquivo, 'r') as file:
            conteudo = file.read()

        # Exibir o conteúdo no QTextEdit
        self.text_edit.setPlainText(conteudo)

        # Configurar o layout do diálogo
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        self.setLayout(layout)
