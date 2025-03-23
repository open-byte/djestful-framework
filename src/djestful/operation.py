from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from django.http import HttpRequest, HttpResponse

from .types import HttpMethod

if TYPE_CHECKING:
    from .views import APIView


class Operation:
    def __init__(
        self,
        view_func: Callable[..., HttpResponse],
        path: str,
        methods: list[HttpMethod],
        description: str | None = None,
        summary: str | None = None,
        url_name: str | None = None,
    ) -> None:
        self.view_func = view_func
        self.path = path
        self.methods = methods
        self.description = description
        self.summary = summary
        self.url_name = url_name

    def execute(
        self, func_parent_class: 'APIView', request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        if func_parent_class.view_is_function:
            return self.view_func(request, *args, **kwargs)

        return self.view_func(func_parent_class, request, *args, **kwargs)
