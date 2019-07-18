import numpy as np
from PIL import Image


def func(file_path, mode="cut"):
    """
    This is to make the image into a square. And mode is cut or fill.
    """
    image = Image.open(file_path).convert("RGBA")
    np_image = np.array(image, dtype=np.uint8)
    height, width, _ = np_image.shape
    if mode == "fill":
        side_length = max(height, width)
    else:
        side_length = min(height, width)
    '''We should expand or reduce the shape to a square, and fill the blank area with WHITE.'''
    new_np_image = np.ones((side_length, side_length, 4), dtype=np.uint8) * 255
    '''Put the picture in the middle.'''
    if mode == "fill":
        if height < side_length:
            s = int(side_length / 2) - int(height / 2)
            new_np_image[s: s + height, :, :] = np_image
        else:
            t = int(side_length / 2) - int(width / 2)
            new_np_image[:, t: t + width, :] = np_image
    else:
        if height > side_length:
            s = int(height / 2) - int(side_length / 2)
            new_np_image = np_image[s: s + side_length, :, :]
        else:
            t = int(width / 2) - int(side_length / 2)
            new_np_image = np_image[:, t: t + side_length, :]
    img = Image.fromarray(new_np_image.astype('uint8')).convert('RGB')
    img.save("square.png")
    print("done.")


if __name__ == "__main__":
    func("./k_new.png")
