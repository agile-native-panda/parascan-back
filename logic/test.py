from decode_to_video import decode_to_video

def test():
    encoded_str = ""
    
    with open("./logic/ENCODED_MP4.txt", "r") as f :
        encoded_str = f.readline()
            
    video_binary = decode_to_video(encoded_str)    

if __name__ == "__main__" :
    test()