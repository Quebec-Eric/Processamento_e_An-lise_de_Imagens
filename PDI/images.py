import imageio.v3 as iio
import re
import os 
from pathlib import Path

class images():
    def __init__(self, fileFolder):
        #Criar dois arranjos, um para treino e outro para teste
        trainList = list()
        testList = list()
    
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
                    print(file.name) 
                    trainList.append(iio.imread(file))
                else:
                    testList.append(iio.imread(file))