from decode_to_video import decode_to_video
from brake_video import brake_video
from ocr_api import ocr_api
from pre_process import is_frame_to_use

def test_decode(video_name):
    encoded_str = ""
    
    with open("ENCODED_MP4.txt", "r") as f :
        encoded_str = f.readline()
            
    decode_to_video(encoded_str, video_name)
    
def test_brake_to_frame(video_name):
    brake_video(video_name)
    
def test_ocr_api():
    img_path = "./tmp/1_0722.png"
    output_json_file = "./tmp/result3.json"
    ocr_api(img_path, output_json_file)
    
def test_is_frame_to_use():
    img_path = "./panyubi/media/video/1_0117.png"
    print(is_frame_to_use(img_path))

if __name__ == "__main__" :
    video_name = "2.mp4"
    
    # test_decode(video_name=video_name)
    # test_brake_to_frame(video_name)
    # test_ocr_api()
    test_is_frame_to_use()
    