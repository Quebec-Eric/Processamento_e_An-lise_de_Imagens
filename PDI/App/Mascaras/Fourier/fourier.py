import cv2
import numpy as np


class fourier:
    def __init__(self, imagens):
        img = cv2.imread(imagens, 0)
        self.fazerfori=self.transformada_fourier(img)
    
    def transformada_fourier(self,imagen):
        f = np.fft.fft2(imagen)
        f_shift = np.fft.fftshift(f)
        espectro = np.log(np.abs(f_shift))
        espectro = (espectro - np.min(espectro)) / (np.max(espectro) - np.min(espectro))
        espectro = (255 * espectro).astype(np.uint8)
        linhas, colunas = imagen.shape
        cw, cc = linhas // 2, colunas // 2

        f_shift[cw - 20: cw + 10, cc - 20: cc + 10] = 0

        ishift = np.fft.ifftshift(f_shift)
        img = np.fft.ifft2(ishift)
        img = np.abs(img)

        cv2.imwrite('App/Raio-X/EspectroFourier.png', espectro)
        cv2.imwrite('App/Raio-X/ImgFourier.png',img)