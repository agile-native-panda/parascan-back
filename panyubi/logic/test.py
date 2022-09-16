import cv2
import numpy as np
from math import sqrt
from decode_to_video import decode_to_video
from brake_video import brake_video
from ocr_api import ocr_api, format_data, join_text
from process import is_frame_to_use, pre_process
import json
def test_decode(video_name):
    encoded_str = ""
    
    with open("ENCODED_MP4.txt", "r") as f :
        encoded_str = f.readline()
            
    decode_to_video(encoded_str, video_name)
    
def test_brake_to_frame(video_name):
    brake_video(video_name)
    
def test_ocr_api():
    img_path = "./panyubi/media/video/parapara/parapara_055.png"
    output_json_file = "./panyubi/media/video/parapara/json/test.json"

    ocr_api(img_path, output_json_file)
    with open(output_json_file, "r") as f :
        output_json = json.load(f)
    format_data(output_json)
    
def test_format_data():
    output_json_file = "./panyubi/media/video/3/3_000.json"
    print(format_data(output_json_file))

def test_is_frame_to_use():
    img_path = "./panyubi/media/video/parapara/parapara_055.png"
    print(is_frame_to_use(img_path))
    
def test_pre_process():
    img_directory_path = "./panyubi/media/video/4"
    pre_process(img_directory_path)

def test_join_text():
    path = "./panyubi/media/video/3/result"
    join_text(path)

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
    
def test_hough_transform(img_path):
    img = cv2.imread(img_path)
    img_preprocessed  = cv2.cvtColor(cv2.GaussianBlur(img, (15,15), 0), cv2.COLOR_BGR2GRAY)
    threshold = luminance_threshold(img_preprocessed)
    img_edges = cv2.Canny(img_preprocessed, threshold1=threshold/2-80, threshold2=threshold/2-70)
    cv2.imwrite("/Users/tatsu/Documents/215ぱんアジャ/02parascan/tests/8/8_0114_edges.png", img_edges)
    
    # copy of image to draw lines    
    img_lines = np.copy(img)

    # find hough lines
    num_pix_threshold = 110 # minimum number of pixels that must be on a line
    lines = cv2.HoughLines(img_edges, 1, np.pi/180, num_pix_threshold)

    for line in lines :
        for rho, theta in line:
            # convert line equation into start and end points of line
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho

            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))

            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))

            cv2.line(img_lines, (x1,y1), (x2,y2), (0,0,255), 1)
    
    cv2.imwrite("/Users/tatsu/Documents/215ぱんアジャ/02parascan/tests/8/8_0114_lines.png", img_lines)
    
def test_harris_corner(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(cv2.GaussianBlur(img, (11,11), 0), cv2.COLOR_BGR2GRAY)

    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.04)

    #result is dilated for marking the corners, not important
    dst = cv2.dilate(dst,None)

    # Threshold for an optimal value, it may vary depending on the image.
    img[dst>0.01*dst.max()]=[0,0,255]
    
    cv2.imwrite("/Users/tatsu/Documents/215ぱんアジャ/02parascan/tests/8/8_0114_harris.png", img)

def test_marge_harris_and_hough():
    line_img = cv2.imread("/Users/tatsu/Documents/215ぱんアジャ/02parascan/tests/8/8_0114_lines.png")
    corner_img = cv2.imread("/Users/tatsu/Documents/215ぱんアジャ/02parascan/tests/8/8_0114_harris.png")
    red = np.array([0, 0, 255])
    line_img = cv2.inRange(line_img, red, red)
    corner_img = cv2.inRange(corner_img, red, red)
    size = min(len(line_img), len(line_img[0]))
    kernel_large = np.ones((size//50,size//50))
    line_img = cv2.dilate(line_img, kernel_large)
    kernel_small = np.ones((size//500,size//500))
    corner_img = cv2.dilate(corner_img, kernel_small)
    marge_img = cv2.bitwise_and(line_img, corner_img)
    kernel_medium = np.ones((size//100,size//100))
    # marge_img = cv2.morphologyEx(marge_img, cv2.MORPH_OPEN, kernel_medium)
    cv2.imwrite("/Users/tatsu/Documents/215ぱんアジャ/02parascan/tests/8/8_0114_marge.png", marge_img)

def calc_cross(v1, v2, v3, v4):
    # 成分に分ける
    x1, y1 = v1
    x2, y2 = v2
    x3, y3 = v3
    x4, y4 = v4

    # 分子、分母の値
    denominator = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    nua = (x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)
    # nub = (x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)

    # ua, ubを求める
    ua = nua / denominator
    # ub = nub / denominator

    # 交点ベクトルのx, y
    x = x1 + ua * (x2 - x1)
    y = y1 + ua * (y2 - y1)
    
    return int(x), int(y)

def test_contours(img_path):
    img = cv2.imread(img_path)
    img_def = np.copy(img)
    img_height = len(img)
    img_width = len(img[0])
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    threshold = luminance_threshold(img_gray)
    ret, img_gray = cv2.threshold(img_gray, threshold*0.775, 255, 0)
    cv2.imwrite("/Users/tatsu/Documents/215ぱんアジャ/02parascan/tests/8/8_0149_binary.png", img_gray)
    red = np.array([0, 0, 255])
    contours, hierarchy = cv2.findContours(img_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    max_cnt = max(contours, key=lambda x: cv2.contourArea(x))
    img = cv2.drawContours(img, max_cnt, -1, (0, 0, 255), 1)
    img_edges = cv2.inRange(img, red, red)
    cv2.imwrite("/Users/tatsu/Documents/215ぱんアジャ/02parascan/tests/8/8_0149_contour.png", img)
    
    # copy of image to draw lines    
    img_lines = img_def + 255 - img_def
    white_img_def = np.copy(img_lines)
    img_lines = cv2.cvtColor(img_lines, cv2.COLOR_BGR2GRAY)
    white_img_def = cv2.cvtColor(white_img_def, cv2.COLOR_BGR2GRAY)
    white_img = np.copy(white_img_def)

    # find hough lines
    num_pix_threshold = 110 # minimum number of pixels that must be on a line
    lines = cv2.HoughLines(img_edges, 1, np.pi/180, num_pix_threshold)

    vectors = []
    for line in lines :
        for rho, theta in line :
            # convert line equation into start and end points of line
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho

            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))

            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))

            vectors.append([[x1, y1], [x2, y2]])
            cv2.line(img_lines, (x1,y1), (x2,y2), 0, 1)
            
    cv2.imwrite("/Users/tatsu/Documents/215ぱんアジャ/02parascan/tests/8/8_0149_lines.png", img_lines)
            
    points = []
    for i in range(len(vectors) - 1) :
        for j in range(i+1, len(vectors)) :
            v1, v2 = vectors[i]
            v3, v4 = vectors[j]
            x, y = calc_cross(v1, v2, v3, v4)
            cv2.circle(img_lines, (x, y), 4, (0), -1)
            if 0 < x and x < img_width and 0 < y and y < img_height :
                points.append([x, y])
    cv2.imwrite("/Users/tatsu/Documents/215ぱんアジャ/02parascan/tests/8/8_0149_circle.png", img_lines)
            
    points.sort(key=lambda x : x[0] + x[1])
    print(points)
            
    distances = []
    for i in range(len(points) - 1) :
        for j in range(i+1, len(points)) :
            if i == j : continue
            x1, y1 = points[i]
            x2, y2 = points[j]
            distances.append(int(sqrt((x1-x2)**2 + (y1-y2)**2)))
            
    distances.sort()
    width = distances[0]
    height = distances[2]
    
    print(width, height)
    
    pts1 = np.float32([points[0], points[1], points[2], points[3]])
    pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
    
    M = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(img_def,M,(width,height))

    cv2.imwrite("/Users/tatsu/Documents/215ぱんアジャ/02parascan/tests/8/8_0149_out.png", dst)
    

if __name__ == "__main__" :
    video_name = "3.mp4"
    
    img_path = "/Users/tatsu/Documents/215ぱんアジャ/02parascan/tests/8/8_0149.png"
    # test_hough_transform(img_path)
    # test_harris_corner(img_path)
    # test_marge_harris_and_hough()
    test_contours(img_path)
    
    # test_decode(video_name=video_name)
    # test_brake_to_frame(video_name)
    # test_ocr_api()
    # test_is_frame_to_use()
    # test_format_data()
    # test_pre_process()
    # test_join_text()