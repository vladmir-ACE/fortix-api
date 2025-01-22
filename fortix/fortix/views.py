
from rest_framework.views import APIView
from django.http import JsonResponse

from .settings import GLOBAL_APP_VERSION

class AppVersion(APIView):
    def get(self, request):
        return JsonResponse({'version': GLOBAL_APP_VERSION})
    