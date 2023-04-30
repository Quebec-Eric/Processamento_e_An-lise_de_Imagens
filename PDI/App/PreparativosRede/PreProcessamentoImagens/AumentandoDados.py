
import sys
sys.path.append('App/Imports')

from Imports import *

import os
import numpy as np
from PIL import Image

class AumentarDados:
    def __init__(self, imagens):
        self.train_aumentada = []
        self.augmentData(imagens)

    def augmentData(self, imagens):
        for imagem in imagens:
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

    def equalizeHist(self, img):
        # Calcula o histograma da imagem
        hist, bins = np.histogram(img.flatten(), 256, [0, 256])

        # Calcula a função de distribuição acumulada do histograma
        cdf = hist.cumsum()

        # Normaliza a função de distribuição acumulada
        cdf_norm = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())
        cdf_norm = cdf_norm.astype(np.uint8)

        # Equaliza o histograma da imagem
        img_eq = np.interp(img.flatten(), bins[:-1], cdf_norm)
        img_eq = np.reshape(img_eq, img.shape)

        return img_eq