from logging import raiseExceptions
from urllib import response
import requests
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from django.http import JsonResponse
from rest_framework import status, viewsets
from .serializers import MediaSerializer
from .models import Media
import sys
sys.path.append("../")
from logic.brake_video import brake_video

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
class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        try:
            file = str(request.data["video"])
            brake_video(file)
        except:
            raiseExceptions("brake_vide error")
        return response
