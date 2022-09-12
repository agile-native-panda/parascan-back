from logging import raiseExceptions
from urllib import response
import requests
from rest_framework.views import APIView
import os
import re
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from django.http import JsonResponse, FileResponse
from rest_framework import status, viewsets
from .serializers import MediaSerializer
from .models import Media
import sys
sys.path.append("../")
from logic.brake_video import brake_video
from logic.ocr_api import join_text, ocr_api, format_data
from logic.process import pre_process, post_process
import concurrent.futures
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
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        try:
            file = str(request.data["video"])
            print(file)
            brake_video(file)
            dir = "../panyubi/media/video/"
            video_name = "".join(file.split(".")[:-1])
            dir += video_name
            
            pre_process(dir)
            
            for image in sorted(os.listdir(dir), key=natural_keys):
                image_name =  "".join(image.split(".")[:-1])
                json_path = dir+"/"+image_name+".json"
                image_path = dir+"/"+image

                ocr_api(image_path, json_path)
                print("-----------")
                print(json_path)
                format_data(json_path)
            join_text(dir+"/result")
            post_process(dir)
        except:
            raiseExceptions("ocr process error")
        file_path = dir + "/result/" + "result.txt"
        print(file_path)
        return FileResponse(open(file_path, "rb"), as_attachment=True, filename="result.txt")
