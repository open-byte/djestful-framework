from django.http import HttpResponse, JsonResponse
from djestful.views import APIView
from djestful.decorators import action
from django.http import HttpRequest
from asgiref.sync import sync_to_async
class TestView(APIView):

    @action.post('/test/test', summary='This is a test post endpoint')
    async def testendpoint(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        response = await self.test(request, *args, **kwargs)
        return response
    

    @action.post('/test/test', summary='This is a test post endpoint')
    async def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
      
        return JsonResponse({'message': 'Hello, World! (POST)'})

    async def test(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return JsonResponse({'message': 'Hello, World! (GET)'})

# @action.post('/test/')
# def  test_view(request):
#     return JsonResponse({'message': 'Function Hello, World! (POST)'})