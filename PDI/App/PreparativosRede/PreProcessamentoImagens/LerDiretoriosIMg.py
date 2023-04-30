import sys
sys.path.append('App/Imports')

from Imports import *
import os
import re

class LeituraDiretorio:
    def __init__(self, path):
        self.train = []
        self.test = []
        self.loadImg(path)
        


    def loadImg(self, path):
        class_map = {0: 'I', 1: 'II', 2: 'III', 3: 'IV'}
        for subdir in os.listdir(path):
            subdir_path = os.path.join(path, subdir)
            if not os.path.isdir(subdir_path):
                continue
            for file in os.listdir(subdir_path):
                match = re.search(r'(\w+)_(\w+)\s*\((\d+)\)\.png', file)
                if match:
                    breast = match.group(1)
                    view = match.group(2)
                    class_num = int(match.group(3)) % 4
                    class_letter = class_map.get(class_num)

                    if class_letter:
                        filename = f"{breast}_{view} ({class_num}).png"
                        if class_num == 0:
                            self.test.append(os.path.join(subdir, filename))
                        else:
                            self.train.append(os.path.join(subdir, filename))

        
        print(len(self.train))
        print(len(self.test)) 
        return 