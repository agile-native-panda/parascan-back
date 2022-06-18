import base64

def decode_to_video(encoded_str="", video_name=""):
    '''
    parameters
    ----------
    encoded_str : str
        動画をエンコードした文字列
    video_name : デコード先のビデオの名前
    
    returns
    -------
    なし
    '''
    
    path = "./tmp/" + video_name
    
    with open(path, "wb") as f :
        f.write(base64.b64decode(encoded_str))