import argparse
import cv2
import subprocess
import numpy as np
import time
import matplotlib.pyplot as plt

"""
demo
"""
pixels = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:oa+>!:+. ")

if __name__ == "__main__":
    file_path = 'D:\work\BadApple.mp4'
    vc = cv2.VideoCapture(file_path)
    if vc.isOpened():
        ret, frame = vc.read()
    else:
        ret = False
    i = 0
    size = (64, 48)
    while ret and i < 500:
        # plt.imshow(frame)
        # plt.show()
        ret, frame = vc.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(gray, size, interpolation=cv2.INTER_AREA)
        i += 1

        percents = img / 255
        indexes = (percents * (len(pixels) - 1)).astype(np.int)

        res = []
        height, width = img.shape
        for row in range(height):
            line = ""
            for col in range(width):
                index = indexes[row][col]
                line += pixels[index] + " "
            res.append(line)
            print(line)
        time.sleep(1/15)
        subprocess.call("cls", shell=True)
