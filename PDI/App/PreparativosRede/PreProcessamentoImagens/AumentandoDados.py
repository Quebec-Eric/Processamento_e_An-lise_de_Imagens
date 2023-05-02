
import sys
sys.path.append('App/Imports')

from Imports import *
import cv2
import os
import numpy as np
from PIL import Image

class AumentarDados:
    def __init__(self, imagens):
        self.train_aumentada = []
        self.augmentData(imagens)

    def augmentData(self, imagens):
        for i, imagem in enumerate(imagens):

            # Abre a imagem como um array numpy
            img = np.array(Image.open("App/Raio-X/mamografias/"+imagem))

            # Espelha a imagem horizontalmente
            img_h = np.fliplr(img)

            # Equaliza o histograma da imagem original
            img_eq = self.equalizeHist(img)

            # Equaliza o histograma da imagem espelhada
            img_h_eq = self.equalizeHist(img_h)

            # Adiciona as imagens ao conjunto de treino aumentado
            self.train_aumentada.extend([img, img_h, img_eq, img_h_eq])
            
            # Salva as imagens em um arquivo de teste
            cv2.imwrite("AkiTeste/original" + str(i) + ".png", img)
            cv2.imwrite("AkiTeste/histrograma" + str(i) + ".png", img_h)
            cv2.imwrite("AkiTeste/equalizar" + str(i) + ".png", img_eq)
            cv2.imwrite("AkiTeste/espelhada" + str(i) + ".png", img_h_eq)



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