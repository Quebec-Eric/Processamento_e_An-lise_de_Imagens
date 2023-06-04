import numpy as np
import cv2

class passaBaixa:
    def __init__(self, imagens,valor):
        img = cv2.imread(imagens, 0)
        self.passa=self.low_pass_filter(img,valor)
        

    def low_pass_filter(self,image, cutoff_freq):
        f = np.fft.fft2(image)
        fshift = np.fft.fftshift(f)

        rows, cols = image.shape
        crow, ccol = rows // 2, cols // 2
        mask = np.zeros((rows, cols), np.uint8)
        mask[crow-cutoff_freq:crow+cutoff_freq, ccol-cutoff_freq:ccol+cutoff_freq] = 1

        fshift_filtered = fshift * mask
        f_ishift = np.fft.ifftshift(fshift_filtered)
        img_back = np.fft.ifft2(f_ishift)
        img_back = np.abs(img_back)
        passaBx=img_back.astype(np.uint8)
        cv2.imwrite('App/Raio-X/PassaBaixa.png',passaBx)