from django.http import HttpResponse, JsonResponse
from djestful.views import APIView
from django.http import HttpRequest
class TestView(APIView):

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        from djestful.urls import get_urls

        print(get_urls())
        return JsonResponse({'message': 'Hello, World! (GET)'})

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
      
        return JsonResponse({'message': 'Hello, World! (POST)'})