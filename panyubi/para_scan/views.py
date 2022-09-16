from logging import raiseExceptions
from urllib import response
import asyncio
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

def file_return(file_path, video_name):
    print(file_path)
    result_file = open(file_path, "rb")
    # print("result_file:", result_file.read())
    result_file.seek(0)
    tmp_file = tempfile.TemporaryFile()
    tmp_file.write(result_file.read())
    tmp_file.seek(0)
    # print("tmp_file", tmp_file.read())
    result_file.close()
    path_to_video = "./media/video/"
    clear_files(path_to_video, video_name)
    tmp_file.seek(0)
    video_name.capitalize()
    return FileResponse(tmp_file, as_attachment=True, filename="result.txt")

def init_path(image):
    print(image)
    dir = "./media/video/"
    image_dir = image.split("_")[0]
    image_name =  "".join(image.split(".")[:-1])
    json_path = dir + image_dir + "/" + image_name + ".json"
    image_path = dir + image_dir + "/" + image
    return [image_path, json_path]

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
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            async def run(loop):
                sem = asyncio.Semaphore(10)
                async with sem:
                    
                    async def run_req(image_path, json_path):
                        return await loop.run_in_executor(None, ocr_api, image_path, json_path)
                
                tasks = [run_req(image_path, json_path) for image_path, json_path in map(init_path, [image for image in sorted(os.listdir(dir), key=natural_keys) if "result" not in image])]
                return await asyncio.gather(*tasks)
                
            loop.run_until_complete(run(loop))
            join_text(dir+"/result")
        except:
            raiseExceptions("ocr process error")
        file_path = dir + "/result/" + "result.txt"
        return file_return(file_path, video_name)
