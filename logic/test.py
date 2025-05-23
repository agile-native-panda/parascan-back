from decode_to_video import decode_to_video
from brake_video import brake_video
<<<<<<< HEAD
from ocr_api import ocr_api, format_data
from pre_process import is_frame_to_use, pre_process
=======
from ocr_api import ocr_api, format_data, join_text
from pre_process import is_frame_to_use
>>>>>>> b823ef2c7476fb8957f1b20cb3f2891a537059ae
import json
def test_decode(video_name):
    encoded_str = ""
    
    with open("ENCODED_MP4.txt", "r") as f :
        encoded_str = f.readline()
            
    decode_to_video(encoded_str, video_name)
    
def test_brake_to_frame(video_name):
    brake_video(video_name)
    
def test_ocr_api():
    img_path = "../panyubi/media/video/parapara/parapara_055.png"
    output_json_file = "../panyubi/media/video/parapara/json/test.json"

    ocr_api(img_path, output_json_file)
    with open(output_json_file, "r") as f :
        output_json = json.load(f)
    format_data(output_json)
    
def test_format_data():
    output_json_file = "../panyubi/media/video/3/3_000.json"
    print(format_data(output_json_file))

def test_is_frame_to_use():
    img_path = "./panyubi/media/video/parapara/parapara_055.png"
    print(is_frame_to_use(img_path))
    
def test_pre_process():
    img_directory_path = "./panyubi/media/video/4"
    pre_process(img_directory_path)

def test_join_text():
    path = "../panyubi/media/video/3/result"
    join_text(path)
if __name__ == "__main__" :
    video_name = "3.mp4"
    
    # test_decode(video_name=video_name)
    # test_brake_to_frame(video_name)
    # test_ocr_api()
    # test_is_frame_to_use()
    # test_format_data()
    # test_pre_process()
    # test_join_text()