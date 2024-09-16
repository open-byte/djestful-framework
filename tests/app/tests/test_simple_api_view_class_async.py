import pytest
from django.http import JsonResponse
from django.test import override_settings
from django.test.client import Client
from djestful.decorators import action
from djestful.routers import Router
from djestful.views import APIView


## views.py
class TestAPIView(APIView):
    @action.get('test/class')
    async def get_test_class(self, request):
        return JsonResponse({'message': 'get test class'})

    @action.post('test/class')
    async def post_test_class(self, request):
        return JsonResponse({'message': 'post test class'})

    @action.put('test/class')
    async def put_test_class(self, request):
        return JsonResponse({'message': 'put test class'})

    @action.patch('test/class')
    async def patch_test_class(self, request):
        return JsonResponse({'message': 'patch test class'})

    @action.delete('test/class')
    async def delete_test_class(self, request):
        return JsonResponse({'message': 'delete test class'})

    @action.generic('test/generic', methods=['get', 'post', 'put', 'patch', 'delete'])
    async def generic_test_class(self, request):
        return JsonResponse({'message': f'generic test class {request.method.lower()}'})


## urls.py
router = Router()
router.include('', TestAPIView, basename='test-api-view-class')


urlpatterns = router.urls


@pytest.fixture
def client() -> Client:
    return Client()


@override_settings(ROOT_URLCONF=__name__)
def test_api_view_class(client: Client) -> None:
    response = client.get('/test/class')
    assert response.status_code == 200
    assert response.json() == {'message': 'get test class'}

    response = client.post('/test/class')
    assert response.status_code == 200
    assert response.json() == {'message': 'post test class'}

    response = client.put('/test/class')
    assert response.status_code == 200
    assert response.json() == {'message': 'put test class'}

    response = client.patch('/test/class')
    assert response.status_code == 200
    assert response.json() == {'message': 'patch test class'}

    response = client.delete('/test/class')
    assert response.status_code == 200
    assert response.json() == {'message': 'delete test class'}


@override_settings(ROOT_URLCONF='tests.app.tests.test_simple_api_view_class')
def test_api_view_class_generic(client: Client) -> None:
    response = client.get('/test/generic')
    assert response.status_code == 200
    assert response.json() == {'message': 'generic test class get'}

    response = client.post('/test/generic')
    assert response.status_code == 200
    assert response.json() == {'message': 'generic test class post'}

    response = client.put('/test/generic')
    assert response.status_code == 200
    assert response.json() == {'message': 'generic test class put'}

    response = client.patch('/test/generic')
    assert response.status_code == 200
    assert response.json() == {'message': 'generic test class patch'}

    response = client.delete('/test/generic')
    assert response.status_code == 200
    assert response.json() == {'message': 'generic test class delete'}