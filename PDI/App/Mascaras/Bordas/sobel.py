import cv2
from matplotlib import pyplot as plt


class sobel:
    def __init__(self, imagens):
        img = cv2.imread(imagens, 0)
        self.sob=self.sobel_edge_detection(img)

    def sobel_edge_detection(self,image):
        sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
        gradient_magnitude = cv2.magnitude(sobelx, sobely)
        gradient_magnitude = cv2.convertScaleAbs(gradient_magnitude)
        cv2.imwrite('App/Raio-X/Sobel.png', gradient_magnitude)