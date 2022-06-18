import json
import time
import datetime
import http.client, urllib.request, urllib.parse
import urllib.error, base64
import ast

def open_json():
    loaded_dict = {}
    path = "./logic/key.json"
    with open(path, "r") as f :
        loaded_dict = json.load(f)
    return loaded_dict

def ocr_api(file_path, output_json_file):
    loaded_dict = open_json()
    end_point = loaded_dict["endpoint"]
    secret_key = loaded_dict["key"]
    host = end_point.split("/")[2]
    ocr_url = end_point + "vision/v3.2/read/analyze"
    read_headers = {
                    "Ocp-Apim-Subscription-Key":secret_key,
                    "Content-Type":"application/octet-stream"
                    }
    result_headers = {
                        "Ocp-Apim-Subscription-Key":secret_key,
                        }
    
    body = ""
    with open(file_path, "rb") as f :
        body = f.read()

    # パラメータの指定
    # 自然な読み取り順序で出力できるオプションを追加
    params = urllib.parse.urlencode({
        # Request parameters
        'readingOrder': 'natural',
    })

    # readAPIを呼んでOperation Location URLを取得
    print(datetime.datetime.now())
    OL_url = call_read_api(host, ocr_url, body, params, read_headers)

    print(OL_url)

    # 処理待ち10秒
    time.sleep(10)

    # Read結果取得
    result_dict = call_get_read_result_api(host, file_path, OL_url, result_headers)
    
    print(result_dict)
    with open(output_json_file, "w") as f :
        json.dump(result_dict, f, ensure_ascii = False)

# Read APIを呼ぶ関数
def call_read_api(host, text_recognition_url, body, params, read_headers):
    # Read APIの呼び出し
    try:
        conn = http.client.HTTPSConnection(host)
        # 読み取りリクエスト
        conn.request(
            method = "POST",
            url = text_recognition_url + "?%s" % params,
            body = body,
            headers = read_headers,
        )

        # 読み取りレスポンス
        read_response = conn.getresponse()
        print(read_response.status)

        # レスポンスの中から読み取りのOperation-Location URLを取得
        OL_url = read_response.headers["Operation-Location"]

        conn.close()
        print("read_request:SUCCESS")

    except Exception as e:
        print("[ErrNo {0}]{1}".format(e.errno,e.strerror))

    return OL_url

# OCR結果を取得する関数
def call_get_read_result_api(host, file_name, OL_url, result_headers):
    result_dict = {}
    # Read結果取得
    try:
        conn = http.client.HTTPSConnection(host)

        # 読み取り完了/失敗時にFalseになるフラグ
        poll = True
        while(poll):
            if (OL_url == None):
                print(file_name + ":None Operation-Location")
                break

            # 読み取り結果取得
            conn.request(
                method = "GET",
                url = OL_url,
                headers = result_headers,
            )
            result_response = conn.getresponse()
            result_str = result_response.read().decode()
            result_dict = ast.literal_eval(result_str)

            if ("analyzeResult" in result_dict):
                poll = False
                print("get_result:SUCCESS")
            elif ("status" in result_dict and 
                  result_dict["status"] == "failed"):
                poll = False
                print("get_result:FAILD")
            else:
                time.sleep(10)
        conn.close()

    except Exception as e:
        print("[ErrNo {0}] {1}".format(e.errno,e.strerror))

    return result_dict