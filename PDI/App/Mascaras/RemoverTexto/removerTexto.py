import cv2

class removerTexto:
    def __init__(self, img):
        img = cv2.imread(img, cv2.COLOR_BGR2GRAY)
        self.semTexto= self.fazerRemoção(img)
        return

    def fazerRemoção(self,imagem):
        #segmetar a imagem
        _, thresholded = cv2.threshold(imagem, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        opened = cv2.morphologyEx(thresholded, cv2.MORPH_OPEN, kernel, iterations=1)
        contours, _ = cv2.findContours(opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        result = imagem.copy()
        cv2.drawContours(result, contours, -1, (255, 255, 255), thickness=cv2.FILLED)
        cv2.imwrite('App/Raio-X/SemTexto.png', result)
        return