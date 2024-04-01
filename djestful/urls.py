import json

from django.http import JsonResponse
from django.urls import path
from django.views import View

TMP = 'openapi.json'
SCHEMA = {
    'openapi': '3.1.0',
    'info': {'title': 'Test', 'version': '0.1.0'},
    'paths': {},
    'components': {},
}


class OpenAPIView(View):
    def get(self, request, *args, **kwargs):  # type: ignore
        return JsonResponse(SCHEMA, safe=False)


urlpatterns = [
    path(TMP, OpenAPIView.as_view(), name='openapi'),
]
