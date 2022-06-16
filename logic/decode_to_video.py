import base64

def decode_to_video(encoded_str=""):
    '''
    parameters
    ----------
    encoded_str : str
        動画をエンコードした文字列
    
    returns
    ------
    decoded : bytes
        文字列をデコードした動画
    '''
    decoded = base64.b64decode(encoded_str)
    return decoded