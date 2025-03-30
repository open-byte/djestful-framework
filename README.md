# DjestFul Framework

DjestFul is a framework which has the advantage of documenting the endpoints (views) of Django applications.

It is inspired by FastAPI, Django Ninja, and Django Restframework.


The main goal of DjestFul is to provide a simple way to document the endpoints of Django applications with the style of Django and FastAPI or Django Ninja.

For example, the following code is a simple Django view:


```python
from django.http import HttpResponse, JsonResponse
from djestful.views import APIView
from djestful.decorators import action
from django.http import HttpRequest
from pydantic import BaseModel

## schemas.py
class Item(BaseModel):
    id: int
    name: str
    description: str


## views.py
class TestView(APIView):

    @action.post(
        '/users/me',
        description='This is a test post endpoint',
        summary='This is a test post endpoint',
        tags=['test'],
    async def post_test_endpoint(self, item: Item) -> Item:
        return item

    @action.get('/users/me', description='This is a test get endpoint',summary='This is a test get endpoint',tags=['test'])
    async def get_test_endpoint(self, request: HttpRequest) -> list[Item]:
        return [
            Item(id=1, name='test', description='test'),
            Item(id=2, name='test2', description='test2'),
        ]


## urls.py

from django.urls import path
from djestful.routers import Router
from test_app.views import TestView, TestView2


router = Router()
router.include('api', TestView, basename='test_view')


urlpatterns = [
   path('', include(router.urls)),
]

```
