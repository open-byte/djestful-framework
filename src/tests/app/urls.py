"""
URL configuration for tests project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from random import randint
from typing import Any

from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from djestful.decorators import action
from djestful.routers import Router
from djestful.views import APIView


class TestAPIView(APIView):
    def test_some_method(self):
        return {'message': f'test some method {randint(1, 100)}'}

    @action.get(
        'test/class/{test_id}/{test_name}',
        summary='Test class get method',
        description='Test class get method description',
    )
    @action.post('test/class')
    def post_test_class(self, request: Any) -> JsonResponse:
        return JsonResponse({'message': 'post test class'})

    @action.put('test/class')
    def put_test_class(self, request: Any) -> JsonResponse:
        return JsonResponse({'message': 'put test class'})

    @action.patch('test/class')
    def patch_test_class(self, request: Any) -> JsonResponse:
        return JsonResponse({'message': 'patch test class'})

    @action.delete('test/class')
    def delete_test_class(self, request: Any) -> JsonResponse:
        return JsonResponse({'message': 'delete test class'})

    @action.generic('test/generic', methods=['get', 'post', 'put', 'patch', 'delete'])
    def generic_test_class(self, request: Any) -> JsonResponse:
        return JsonResponse({'message': f'generic test class {request.method.lower()}'})


## views.py
@action.get('test/function', url_name='auth')
def get_test_function(request):
    return JsonResponse({'message': f'get test function {randint(1, 100)}'})


router = Router()
router.include('{test_t}/', TestAPIView, basename='test-api-view-class')
router.include('', get_test_function, basename='user')


urlpatterns = [
    path('admin/', admin.site.urls),
    *router.urls,
]
