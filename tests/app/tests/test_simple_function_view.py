import pytest
from django.http import JsonResponse
from django.test import override_settings
from django.test.client import Client
from djestful.decorators import action
from djestful.routers import Router


## views.py
@action.get('test/function')
def get_test_function(request):
    return JsonResponse({'message': 'get test function'})


@action.post('test/function')
def post_test_function(request):
    return JsonResponse({'message': 'post test function'})


@action.put('test/function')
def put_test_function(request):
    return JsonResponse({'message': 'put test function'})


@action.patch('test/function')
def patch_test_function(request):
    return JsonResponse({'message': 'patch test function'})


@action.delete('test/function')
def delete_test_function(request):
    return JsonResponse({'message': 'delete test function'})


@action.generic('test/generic', methods=['get', 'post', 'put', 'patch', 'delete'])
def generic_test_function(request):
    return JsonResponse({'message': f'generic test function {request.method.lower()}'})


## urls.py
router = Router()

router.include('function/', get_test_function, basename='test-api-view-function')
router.include('function/', post_test_function, basename='test-api-view-function')
router.include('function/', put_test_function, basename='test-api-view-function')
router.include('function/', patch_test_function, basename='test-api-view-function')
router.include('function/', delete_test_function, basename='test-api-view-function')
router.include(
    'function-generic/', generic_test_function, basename='test-api-view-function-generic'
)


urlpatterns = router.urls


@pytest.fixture
def client() -> Client:
    return Client()


@override_settings(ROOT_URLCONF=__name__)
def test_api_view_function(client: Client) -> None:
    response = client.get('/function/test/function')
    assert response.status_code == 200
    assert response.json() == {'message': 'get test function'}

    response = client.post('/function/test/function')
    assert response.status_code == 200
    assert response.json() == {'message': 'post test function'}

    response = client.put('/function/test/function')
    assert response.status_code == 200
    assert response.json() == {'message': 'put test function'}

    response = client.patch('/function/test/function')
    assert response.status_code == 200
    assert response.json() == {'message': 'patch test function'}

    response = client.delete('/function/test/function')
    assert response.status_code == 200
    assert response.json() == {'message': 'delete test function'}


@override_settings(ROOT_URLCONF=__name__)
def test_api_view_function_generic(client: Client) -> None:
    response = client.get('/function-generic/test/generic')
    assert response.status_code == 200
    assert response.json() == {'message': 'generic test function get'}

    response = client.post('/function-generic/test/generic')
    assert response.status_code == 200
    assert response.json() == {'message': 'generic test function post'}

    response = client.put('/function-generic/test/generic')
    assert response.status_code == 200
    assert response.json() == {'message': 'generic test function put'}

    response = client.patch('/function-generic/test/generic')
    assert response.status_code == 200
    assert response.json() == {'message': 'generic test function patch'}

    response = client.delete('/function-generic/test/generic')
    assert response.status_code == 200
    assert response.json() == {'message': 'generic test function delete'}
