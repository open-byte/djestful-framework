from django.http import HttpResponse, JsonResponse
from djestful.openapi.docs import get_swagger_ui_html
from djestful.views import APIView


class TestView(APIView):
    def _test(i: int):
        return i + 1

    def get(self, request: int, *args, **kwargs) -> HttpResponse:
        print(self._test.__annotations__)
        return get_swagger_ui_html(
            title='Test API',
            openapi_url='http://localhost:8000/openapi.json',
        )

    def post(self, request, *args, **kwargs) -> HttpResponse:
        return HttpResponse('Hello, World!')
