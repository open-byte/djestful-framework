from django.views import View
from django.views.decorators.csrf import csrf_exempt


class APIView(View):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)

        return csrf_exempt(view)
