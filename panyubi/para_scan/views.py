from logging import raiseExceptions
from urllib import response
import requests
from rest_framework.views import APIView
import os
import re
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from django.http import JsonResponse, FileResponse, HttpResponse
from rest_framework import status, viewsets
from .serializers import MediaSerializer
from .models import Media
import sys
sys.path.append("../")
from logic.brake_video import brake_video
from logic.ocr_api import join_text, ocr_api, format_data
from logic.process import pre_process, clear_files
import concurrent.futures
import tempfile
"""
class OcrRequest(APIView):
    def get(self, request):
        zipcode = request.GET.get(key="zipcode", default="1000011")
        resp = requests.get(
            'http://zipcloud.ibsnet.co.jp/api/search?zipcode=' +
            str(zipcode) +
            '&limit=1')
        print(resp)
        return Response(resp.json(), status=resp.status_code)

    def post(self, request):
        try:
            file = request.data['file']
            print(file)
        except KeyError:
            raise ParseError('Request has no resource file attached')
        return JsonResponse({}, status=status.HTTP_201_CREATED)
"""

def index(request):
    return HttpResponse('nothing here.')

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def file_return(file_path):
    print(file_path)
    result_file = open(file_path, "rb")
    # print("result_file:", result_file.read())
    result_file.seek(0)
    tmp_file = tempfile.TemporaryFile()
    tmp_file.write(result_file.read())
    tmp_file.seek(0)
    # print("tmp_file", tmp_file.read())
    result_file.close()
    path_to_video = "./media/video"
    clear_files(path_to_video)
    tmp_file.seek(0)
    return FileResponse(tmp_file, as_attachment=True, filename="result.txt")

class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        try:
            dir = "./media/video/"
            file = str(request.data["video"])
            brake_video(file)
            video_name = "".join(file.split(".")[:-1])
            
            dir += video_name
            
            pre_process(dir)
            
            for image in sorted(os.listdir(dir), key=natural_keys):
                if "result" in image : continue
                image_name =  "".join(image.split(".")[:-1])
                json_path = dir+"/"+image_name+".json"
                image_path = dir+"/"+image

                ocr_api(image_path, json_path)
                print("-----------")
                print(json_path)
                format_data(json_path)
            join_text(dir+"/result")
        except:
            raiseExceptions("ocr process error")
        file_path = dir + "/result/" + "result.txt"
        return file_return(file_path)
