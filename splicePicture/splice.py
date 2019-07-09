import os
import logging
import numpy as np
from PIL import Image
from argparse import ArgumentParser


def load(pic_path):
    file_name_list = os.listdir(pic_path)
    height, width = 32, 32
    for idx, file_name in enumerate(file_name_list, 1):
        if file_name.endswith("png"):
            avg_rgb = []
            image = Image.open(os.path.join(pic_path, file_name)).convert("RGBA")
            '''resize'''
            image = image.resize((width, height), Image.ANTIALIAS)
            np_image = np.array(image, dtype=np.uint8)
            # height, width, _ = np_image.shape
            '''record the average value of RGB in the center area'''
            center_h_start, center_h_end = int(height / 8),  int(7 * height / 8)
            center_w_start, center_w_end = int(width / 8),  int(7 * width / 8)
            avg_rgb.append(np.mean(np_image[center_h_start: center_h_end, center_w_start: center_w_end, 0]))
            avg_rgb.append(np.mean(np_image[center_h_start: center_h_end, center_w_start: center_w_end, 1]))
            avg_rgb.append(np.mean(np_image[center_h_start: center_h_end, center_w_start: center_w_end, 2]))

            pic_list.append(np_image)
            avg_rgb_list.append(avg_rgb)
    logging.info("pic_list0 {} \t load done.".format(pic_list[0].shape))


def splice(target_pic_path, new_pic_path):
    image = Image.open(target_pic_path).convert("RGBA")
    np_image = np.array(image)
    logging.info("{} 's shape = {}".format(target_pic_path, np_image.shape))
    height, width, _ = np_image.shape
    '''Block size.'''
    block_size = int(width / 128 + 1)
    '''Splice original pic into the h_num * w_num blocks'''
    block_h_num = int(height / block_size)
    block_w_num = int(width / block_size)
    logging.info("block_size = {}, block_h_num = {}, block_w_num = {}".format(block_size, block_h_num, block_w_num))
    # new_image = Image.new("RGBA", new_width * unit, new_height * unit)
    '''Compare a block to thumbnail according to average value of RGB. 
        And choose the most similar thumbnail to replace this block.
        So the new pic's size will be as follows.'''
    new_np_image = np.zeros((block_h_num * 32, block_w_num * 32, 4), dtype=np.uint8)
    for i in range(block_h_num):
        for j in range(block_w_num):
            block = np_image[i * block_size: (i + 1) * block_size, j * block_size: (j + 1) * block_size, :]
            # print(i * unit, (i + 1) * unit, j * unit,  (j + 1) * unit)
            pic = find_replace_pic(block)
            # new_image.paste()
            new_np_image[i * 32: (i + 1) * 32, j * 32: (j + 1) * 32, :] = pic
    logging.info("new image's shape = {}".format(new_np_image.shape))
    img = Image.fromarray(new_np_image.astype('uint8')).convert('RGB')
    img.save(new_pic_path)
    logging.info("splice done.")


def find_replace_pic(block):
    _r = np.mean(block[:, :, 0])
    _g = np.mean(block[:, :, 1])
    _b = np.mean(block[:, :, 2])
    min_distance = float("inf")
    index = -1
    for idx, avg_rgb in enumerate(avg_rgb_list):
        distance = get_distance((_r, _g, _b), avg_rgb)
        if distance < min_distance:
            min_distance = distance
            index = idx
    # np_image
    return pic_list[index]


def get_distance(pic1, pic2, mode=1):
    if mode == 1:
        return (pic1[0] - pic2[0]) ** 2 + (pic1[1] - pic2[1]) ** 2 + (pic1[2] - pic2[2]) ** 2
    return 3 * (pic1[0] - pic2[0]) ** 2 + 4 * (pic1[1] - pic2[1]) ** 2 + 2 * (pic1[2] - pic2[2]) ** 2


def test():
    img = Image.open("./picture/ee_1.png").convert("RGBA")
    print(img.size)
    new_img = img.resize((32, 32), Image.ANTIALIAS)
    new_img.save("new.png")


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                        datefmt="%d-%M-%Y %H:%M:%S", level=logging.INFO)
    parser = ArgumentParser()
    parser.add_argument("-d", "--dir", default="./picture", help="thumbnails dir", type=str)
    parser.add_argument("-f", "--file", default="./jj.jpg", help="the path of target picture", type=str)
    parser.add_argument("-n", "--new", default="new.png", help="the path of new picture", type=str)
    args = parser.parse_args()
    if os.path.exists(args.dir) and os.path.exists(args.file):
        pic_list = []
        avg_rgb_list = []
        # load("./picture")
        load(args.dir)
        # splice("./jj.jpg", "new.png")
        splice(args.file, args.new)
    else:
        if not os.path.exists(args.dir):
            error = args.dir
        else:
            error = args.file
        logging.error("{} is not exist.".format(error))
    # test()
