from django.http import HttpResponse, JsonResponse
from djestful.views import APIView
from djestful.decorators import action
from django.http import HttpRequest
class TestView(APIView):

    @action.generic('/test/test', methods=['get'])
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:

        return JsonResponse({'message': 'Hello, World! (GET)'})
    

    @action.post('/test/test', summary='This is a test post endpoint')
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
      
        return JsonResponse({'message': 'Hello, World! (POST)'})



@action.post('/test/')
def  test_view(request):
    return JsonResponse({'message': 'Function Hello, World! (POST)'})