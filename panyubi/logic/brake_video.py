import cv2
import os

def brake_video(video_name=""):
    '''
    parameters
    ----------
    video_name : str
        動画のファイル名
    returns
    -------
    None
    '''
    
    PATH_TO_TMP = "./media/video/"
    
    filepath = PATH_TO_TMP + video_name
    print(filepath)
    capture = cv2.VideoCapture(filepath)
    if not capture.isOpened():
        print("capture Error")
        return
    
    base_name = "".join(video_name.split(".")[:-1])
    dir_path = PATH_TO_TMP + base_name
    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, base_name)
    
    digit = len(str(int(capture.get(cv2.CAP_PROP_FRAME_COUNT))))
    
    n = 0
    m = 0
    EXT = "png"
    while True:
        ret, frame = capture.read()
        if n%3 != 0 :
            n += 1
            continue
        if ret:
            cv2.imwrite('{}_{}.{}'.format(base_path, str(m).zfill(digit), EXT), frame)
            n += 1
            m += 1
        else:
            return