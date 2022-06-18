from glob import glob
import cv2

def is_frame_to_use(img_path):
    img = cv2.imread(img_path)
    
    detector = cv2.AKAZE_create()

    keypoints = detector.detect(img)
    
    print(img_path, len(keypoints))


def pre_process(img_directory_path):
    search_path = img_directory_path + "/*.png"
    img_name_li = glob(search_path)
    for img_name in img_name_li :
        img_path = img_directory_path + "/" + img_name
        if is_frame_to_use(img_path) :
            break