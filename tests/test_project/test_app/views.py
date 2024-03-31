from django.http import HttpResponse
from django.views import View
from djestful import main


class TestView(View):
    def get(self, request, *args, **kwargs):
        main()
        return HttpResponse('Hello, World!')
