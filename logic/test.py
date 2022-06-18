from decode_to_video import decode_to_video
from brake_video import brake_video

def test_decode(video_name):
    encoded_str = ""
    
    with open("ENCODED_MP4.txt", "r") as f :
        encoded_str = f.readline()
            
    decode_to_video(encoded_str, video_name)
    
def test_brake_to_frame(video_name):
    brake_video(video_name)

if __name__ == "__main__" :
    video_name = "2.mp4"
    
    test_decode(video_name=video_name)
    #test_brake_to_frame(video_name)