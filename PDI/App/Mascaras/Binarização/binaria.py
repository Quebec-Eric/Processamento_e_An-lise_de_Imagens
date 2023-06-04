
import cv2

class binaria:
    def __init__(self, img_path, valor):
        img = cv2.imread(img_path, 0)  # Carrega a imagem como uma matriz NumPy em escala de cinza
        if img is None:
            print(f"Erro ao carregar imagem: {img_path}")
        else:
            self.imagem_binarizada = self.fazer_binarizacao(img, valor)

    def fazer_binarizacao(self, img, valor):
        _, binary_image = cv2.threshold(img, valor, 255, cv2.THRESH_BINARY)
        cv2.imwrite('App/Raio-X/binary_image.png', binary_image)
        