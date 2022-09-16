import cv2
import numpy as np
import re
from glob import glob

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def luminance_threshold(gray_img):
    """
    グレースケールでの値(輝度と呼ぶ)が `x` 以上のポイントの数が20%を超えるような最大のxを計算する
    ただし、 `100 <= x <= 200` とする
    """
    card_luminance_percentage = 0.2
    number_threshold = gray_img.size * card_luminance_percentage
    flat = gray_img.flatten()
    # 200 -> 100 
    for diff_luminance in range(100):
        if np.count_nonzero(flat > 200 - diff_luminance) >= number_threshold:
            return 200 - diff_luminance
    return 100

def binarize(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def transform(img_directory_path):
    search_path = img_directory_path + "/*.png"
    img_path_li = sorted(glob(search_path), key=natural_keys)
    for img_path in img_path_li :
        img = cv2.imread(img_path)
        img = binarize(img)