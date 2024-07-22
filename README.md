# DjestFul Framework

DjestFul is a framework which has the advantage of documenting the endpoints (views) of Django applications.

It is inspired by FastAPI, Django Ninja, and Django Restframework.


The main goal of DjestFul is to provide a simple way to document the endpoints of Django applications with the style of Django and FastAPI or Django Ninja.

For example, the following code is a simple Django view:

```python

```python
from django.http import HttpResponse, JsonResponse
from djestful.views import APIView
from djestful.decorators import action
from django.http import HttpRequest

class TestView(APIView):

    @action.post('/users/me', summary='This is a test post endpoint')
    async def post_test_endpoint(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return JsonResponse(
            {
                'message': 'This is a test POST endpoint',
                'function': 'post_test_endpoint',
            }
        )

    @action.get('/users/me', summary='This is a test get endpoint')
    async def get_test_endpoint(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return JsonResponse(
            {
                'message': 'This is a test endpoint',
                'function': 'get_test_endpoint',
            }
        )

## urls.py

from django.urls import path
from djestful.routers import Router
from test_app.views import TestView, TestView2


router = Router()
router.include('api', TestView, basename='test_view')


urlpatterns = [
   path('api/', include(router.urls)),
]


```