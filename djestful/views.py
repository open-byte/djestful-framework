from typing import Any

from django.views import View
from django.views.decorators.csrf import csrf_exempt


class APIView(View):
    @classmethod
    def as_view(cls, **initkwargs: Any) -> Any:
        view = super().as_view(**initkwargs)
        view.cls = cls
        view.initkwargs = initkwargs

        return csrf_exempt(view)
