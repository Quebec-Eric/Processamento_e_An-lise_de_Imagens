#Pontifícia Universidade Católica de Minas Gerais (Campus Coração Eucarístico)
#Ciência da Computação
#Bryan Jonathan Melo De Oliveira - 708688
#Eric Azevedo de Oliveira - 1269480
#João Gabriel Sena Fernandes - 1209882

import sys

sys.path.append('App/Imports')

from Imports import *
import cv2
import os
import re
import numpy as np
from PIL import Image

class AumentarDados:
    def __init__(self, imagens):
        self.train_aumentada = []
        self.augmentData(imagens)

    def augmentData(self, imagens):
        for i, imagem in enumerate(imagens):
            # Abre a imagem como um array numpy
            if i >0:
                img = np.array(Image.open("App/Raio-X/mamografias/"+imagem))
                
                # Aplica a expressão regular à variável 'imagem', não à lista 'imagens'
                match = re.search(r'\((\d+)\)', imagem)
                if match:
                    # O método group(1) retorna o primeiro grupo de captura, que é o número entre parênteses
                    number = int(match.group(1))
                    new_filename = "AkiTeste/" + str(number) + "_Normal_.png"
                    new_filename2 = "AkiTeste/" + str(number) + "_Espelhada_.png"
                    #new_filename3 = "AkiTeste/" + str(number) + "_EspelhadaEQ_.png"
                    #new_filename4 = "AkiTeste/" + str(number) + "_Histo_.png"
                    espelho = np.rot90(img, 2)
                    #img_eq = self.equalizeHist(espelho)
                    #img_eq2 = self.equalizeHist(img)
                    cv2.imwrite(new_filename2, espelho)
                    cv2.imwrite(new_filename, img)
                    #cv2.imwrite(new_filename3, img_eq)
                    #cv2.imwrite(new_filename4, img_eq2)

                    #cv2.imwrite("teste/Teste" + str(i) + ".png", img)
                    # Espelha a imagem horizontalmente
                    #img_h = np.fliplr(img)
                    # = img.rotate(180)
                    #espelho = np.fliplr(img)
                    #espelho = np.rot90(img, 2)

                    # Equaliza o histograma da imagem original
                    #img_eq = self.equalizeHist(img_h)

                    # Equaliza o histograma da imagem espelhada
                    #img_h_eq = self.equalizeHist(img)

                    # Adiciona as imagens ao conjunto de treino aumentado
                    #self.train_aumentada.extend([img, img_h, img_eq, img_h_eq])
                    
                    # Salva as imagens em um arquivo de teste
                    #nome_arquivo = os.path.splitext(imagem)[0] 
                    #cv2.imwrite("AkiTeste/" +nome_arquivo+"_NN_.png", img)
                    #cv2.imwrite("AkiTeste/histrograma" + str(i) + ".png", img)
                    #cv2.imwrite("AkiTeste/equalizar" + str(i) + ".png", img_h_eq )
                    #cv2.imwrite("AkiTeste/espelhada" + str(i) + ".png", espelho)
                    print(i)



    def equalizeHist(self, img):
        # Normaliza os valores de pixel da imagem para o intervalo de [0, 255]
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)

        # Calcula o histograma da imagem
        hist, bins = np.histogram(img.flatten(), 256, [0, 256])

        # Calcula a função de distribuição acumulada do histograma
        cdf = hist.cumsum()

        # Normaliza a função de distribuição acumulada
        cdf_normalized = cdf * float(hist.max()) / cdf.max()

        # Calcula os novos valores de pixel usando a função de distribuição acumulada normalizada
        img_eq = np.interp(img.flatten(), bins[:-1], cdf_normalized).reshape(img.shape)

        return img_eq.astype('uint8')