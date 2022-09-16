from genericpath import isfile
from glob import glob
import re
import cv2
import os

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def is_frame_to_use(bf, detector, img_path, pre_img_path, pre_des):
    img = cv2.imread(img_path)
    if type(pre_des) is str :
        pre_img = cv2.imread(pre_img_path)
    
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    detector = cv2.AKAZE_create()
    kp, des = detector.detectAndCompute(img, None)
    if type(pre_des) is str :
        pre_kp, pre_des = detector.detectAndCompute(pre_img, None)

    try:
        matches = bf.match(des, pre_des)
        dist = [m.distance for m in matches]
        score_match = sum(dist) / len(dist)
    except cv2.error:
        score_match = 100000
    
    EXT = ".png"
    img_base_path, img_num = img_path.replace(EXT, "").split("_")
    img_num = int(img_num)
    return img_num, score_match, des

def pre_process(img_directory_path):
    search_path = img_directory_path + "/*.png"
    img_path_li = sorted(glob(search_path), key=natural_keys)
    EXT = ".png"
    li = []
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    detector = cv2.AKAZE_create()
    des = "none"
    for img_path in img_path_li :
        img_base_path, img_num = img_path.replace(EXT, "").split("_")
        digit = len(img_num)
        img_num = int(img_num)
        if img_num == 0 : continue
        pre_img_path = img_base_path + "_" + str(img_num-1).zfill(digit) + EXT
        img_path = img_base_path + "_" + str(img_num).zfill(digit) + EXT
        img_num, score_match, des = is_frame_to_use(bf, detector, img_path, pre_img_path, des)
        li.append([img_num, score_match])
    
    is_up_li = []
    for i, score in li :
        if i == 1 :
            pre_score = score
            continue
        is_up = (score-pre_score) > 0
        is_up_li.append(is_up)
        pre_score = score
    # for i in range(len(li)-1) :
    #     print(li[i])
    #     print(is_up_li[i])
        
    for i in range(len(li)-2) :
        is_up = is_up_li[i]
        is_up_post = is_up_li[i+1]
        if not (not is_up and is_up_post) :
            img_num, score = li[i]
            file_path = img_base_path + "_" + str(img_num).zfill(digit) + EXT
            os.remove(file_path)
        
def clear_files(directory_path, video_name):
    search_path = directory_path + video_name + "/**"
    remove_path_li = glob(search_path, recursive=True)
    print(remove_path_li)
    for remove_path in remove_path_li:
        if os.path.isfile(remove_path) :
            os.remove(remove_path)
    search_path = directory_path + video_name + ".*"
    remove_path_li = glob(search_path)
    for remove_path in remove_path_li:
        if os.path.isfile(remove_path) :
            os.remove(remove_path)
