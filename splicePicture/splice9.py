import os
import numpy as np
from PIL import Image


def func(file_path):
    image = Image.open(file_path).convert("RGBA")
    np_image = np.array(image, dtype=np.uint8)
    height, width, _ = np_image.shape
    side_length = max(height, width)
    unit = int(side_length / 3)
    '''New pictures will be stored in this dir_path.'''
    dir_path = './999'
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    '''We should expand the shape to a square, and fill the blank area with WHITE.'''
    new_np_image = np.ones((side_length, side_length, 4), dtype=np.uint8) * 255
    '''Put the picture in the middle.'''
    if height < side_length:
        s = int(side_length / 2) - int(height / 2)
        new_np_image[s: s + height, :, :] = np_image
    else:
        t = int(side_length / 2) - int(width / 2)
        new_np_image[:, t: t + width, :] = np_image
    '''Splice.'''
    for i in range(3):
        for j in range(3):
            n = new_np_image[i * unit: (i + 1) * unit, j * unit: (j + 1) * unit, :]
            img = Image.fromarray(n.astype('uint8')).convert('RGB')
            img.save(os.path.join(dir_path, str(3 * i + j + 1) + ".png"))
    print("done.")


if __name__ == "__main__":
    func("./jj.jpg")
