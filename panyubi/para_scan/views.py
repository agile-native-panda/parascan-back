import requests
from rest_framework.views import APIView
from rest_framework.response import Response


class GetOcr(APIView):
    def get(self, request):
        zipcode = request.GET.get(key="zipcode", default="1000011")
        resp = requests.get(
            'http://zipcloud.ibsnet.co.jp/api/search?zipcode=' +
            str(zipcode) +
            '&limit=1')
        print(resp)
        return Response(resp.json(), status=resp.status_code)
