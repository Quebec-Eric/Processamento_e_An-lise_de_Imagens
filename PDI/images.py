import imageio.v3 as iio
from pathlib import Path

class images(folder):

    imageList = list()
    for file in Path("Images/{folder}").iterdir():
        if not file.is_file():
            continue
        if file.name.endswith('.tiff') or file.name.endswith('.png'):
            imageList.append(iio.imread(file))

    print(imageList)