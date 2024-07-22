from django.http import HttpResponse, JsonResponse
from djestful.views import APIView
from djestful.decorators import action
from django.http import HttpRequest
class TestView(APIView):

    @action.post('/users/me', summary='This is a test post endpoint')
    async def post_test_endpoint(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return JsonResponse({'message': 'This is a test POST endpoint', 'function': 'post_test_endpoint',})


    @action.get('/users/me', summary='This is a test get endpoint')
    async def get_test_endpoint(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return JsonResponse({'message': 'This is a test  endpoint', 'function': 'get_test_endpoint',})


    @action.put('/users/me', summary='This is a test put endpoint')
    async def put_test_endpoint(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return JsonResponse({'message': 'This is a test PUT endpoint', 'function': 'put_test_endpoint',})
    
    @action.delete('/users/me', summary='This is a test delete endpoint')
    async def delete_test_endpoint(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return JsonResponse({'message': 'This is a test DELETE endpoint', 'function': 'delete_test_endpoint',})


class TestView2(APIView):

    @action.post('/organization', summary='This is a test post endpoint', url_name='organnization-post')
    async def organization_post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return JsonResponse({'message': 'This is a test POST endpoint', 'function': 'organization_post',})

    @action.get('/organization', summary='This is a test get endpoint', url_name='organnization-get')
    async def organization_get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return JsonResponse({'message': 'This is a test GET endpoint', 'function': 'organization_get',})
    


# @action.post('/test/')
# def  test_view(request):
#     return JsonResponse({'message': 'Function Hello, World! (POST)'})