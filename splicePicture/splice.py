import os
import numpy as np
from PIL import Image


def load(pic_path):
    file_name_list = os.listdir(pic_path)
    for idx, file_name in enumerate(file_name_list, 1):
        if file_name.endswith("png"):
            avg_rgb = []
            image = Image.open(os.path.join(pic_path, file_name)).convert("RGBA")
            np_image = np.array(image, dtype=np.uint8)
            height, width, _ = np_image.shape
            center_h_start, center_h_end = int(height / 8),  int(7 * height / 8)
            center_w_start, center_w_end = int(width / 8),  int(7 * width / 8)
            if idx == 1:
                print(center_h_start, center_h_end, center_w_start, center_w_end)
            # print(file_name, np_image.shape)
            avg_rgb.append(np.mean(np_image[center_h_start: center_h_end, center_w_start: center_w_end, 0]))
            avg_rgb.append(np.mean(np_image[center_h_start: center_h_end, center_w_start: center_w_end, 1]))
            avg_rgb.append(np.mean(np_image[center_h_start: center_h_end, center_w_start: center_w_end, 2]))
            # print(idx, avg_rgb)
            pic_list.append(np_image)
            avg_rgb_list.append(avg_rgb)
    print("pic_list0", pic_list[0].shape)


def c(target_pic_path):
    image = Image.open(target_pic_path).convert("RGBA")
    np_image = np.array(image)
    print(np_image.shape)
    height, width = np_image.shape[0], np_image.shape[1]
    unit = int(width / 128 + 1)
    new_height = int(height / unit)
    new_width = int(width / unit)
    print(type(height), unit, new_height, new_width)
    # new_image = Image.new("RGBA", new_width * unit, new_height * unit)
    new_np_image = np.zeros((new_height * 32, new_width * 32, 4), dtype=np.uint8)
    for i in range(new_height):
        for j in range(new_width):
            block = np_image[i * unit: (i + 1) * unit, j * unit: (j + 1) * unit, :]
            # print(i * unit, (i + 1) * unit, j * unit,  (j + 1) * unit)
            pic = find_replace_pic(block)
            # new_image.paste()
            new_np_image[i * 32: (i + 1) * 32, j * 32: (j + 1) * 32, :] = pic
    print(new_np_image.shape)
    img = Image.fromarray(new_np_image.astype('uint8')).convert('RGB')
    # img.show()
    img.save("test.jpg")
    # img.show()


def find_replace_pic(block):
    _r = np.mean(block[:, :, 0])
    _g = np.mean(block[:, :, 1])
    _b = np.mean(block[:, :, 2])
    min_distance = 999999999
    index = -1
    for idx, avg_rgb in enumerate(avg_rgb_list):
        distance = get_distance((_r, _g, _b), avg_rgb)
        if distance < min_distance:
            min_distance = distance
            index = idx
    # np_image
    return pic_list[index]


def get_distance(pic1, pic2):
    # return (pic1[0] - pic2[0]) ** 2 + (pic1[1] - pic2[1]) ** 2 + (pic1[2] - pic2[2]) ** 2
    return 3 * (pic1[0] - pic2[0]) ** 2 + 4 * (pic1[1] - pic2[1]) ** 2 + 2 * (pic1[2] - pic2[2]) ** 2


if __name__ == "__main__":
    pic_list = []
    avg_rgb_list = []
    load("./picture")
    c("C:\\Users\\yan\\Desktop\\jj.jpg")
