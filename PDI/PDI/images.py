import imageio.v3 as iio
import re
import os 
from pathlib import Path
from operator import length_hint 
from PIL import Image
import numpy as np

class images():
    def __init__(self, fileFolder):
        #Criar arranjos;
        #NMNE = Nao Espelhada (Not mirrored) x nao equalizada, NME = Nao espelhada x equalizada
        #MNE = Espelhada x nao equalizada, ME = Espelhada x equalizada
        self.trainListNMNE = list()
        self.trainListNME = list()
        self.trainListMNE = list()
        self.trainListME = list()
        self.testList = list()
    
        #Para os arquivos dentro do path
        y = os.path.join('Images', fileFolder)
        for file in Path(y).iterdir():
            if not file.is_file():
                continue
            #Se o nome possuir formato tiff ou png
            if file.name.endswith('.tiff') or file.name.endswith('.png'):
                #Verificar se nome possui multiplo de 4, e mandar para lista de treino, 
                #caso contrario, para lista de teste
                x = re.findall('[0-9]+', file.name)
                if (int(x[0]) % 4 == 0):
                    #print(file.name) 
                    self.trainListNMNE.append(iio.imread(file))
                else:
                    self.testList.append(iio.imread(file))
        #Espelhar
        for i in self.trainListNMNE:
            self.trainListMNE.append(np.fliplr(i))
