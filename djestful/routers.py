from abc import ABC, abstractmethod
from typing import Any

from djestful.views import APIView

RouteMapping = tuple[str, APIView, str]


class BaseRouter(ABC):
    def __init__(self) -> None:
        self.register: list[RouteMapping] = []

    @abstractmethod
    def include(self, *args: Any, **kwargs: Any) -> None: ...

    @abstractmethod
    def get_urls(self) -> list[RouteMapping]: ...

    @property
    def urls(self) -> list[RouteMapping]:
        return self.get_urls()


class Router(BaseRouter):
    def include(self, prefix: str, view: APIView, *, basename: str | None = None) -> None:
        basename = basename or view.__class__.__name__.lower()

    def get_urls(self) -> list[RouteMapping]:
        return self.register
