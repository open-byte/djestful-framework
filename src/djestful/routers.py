from abc import ABC, abstractmethod
from collections.abc import Callable, Iterator
from inspect import getmembers
from typing import Any, NamedTuple, overload

from django.core.exceptions import ImproperlyConfigured
from django.urls import URLPattern
from django.urls import path as django_path

from djestful.constants import DJESTFUL_OPERATION
from djestful.operation import Operation
from djestful.types import DictHttpMethodStr
from djestful.utils import is_djestful_action, replace_path_param_notation
from djestful.views import APIView, APIViewContainer


class RouteMapping(NamedTuple):
    prefix: str
    view: type[APIView]
    basename: str


class BaseRouter(ABC):
    def __init__(self) -> None:
        self.register: dict[str, RouteMapping] = {}

    @abstractmethod
    def include(self, *args: Any, **kwargs: Any) -> None: ...

    @abstractmethod
    def get_urls(self) -> Iterator[URLPattern]: ...

    @property
    def urls(self) -> Iterator[URLPattern]:
        return self.get_urls()


class Router(BaseRouter):
    def _build_wrapper_class_by_basename(
        self, prefix: str, view: Callable[..., Any], basename: str
    ) -> None:
        wrapper_class: type[APIView]
        route = self.register.get(basename)
        if route is None:
            wrapper_class = type('WrapperAPIView', (APIViewContainer,), {})
            self.register[basename] = RouteMapping(prefix, wrapper_class, basename)

        elif not (isinstance(route.view, type) and issubclass(route.view, APIViewContainer)):
            raise Exception('the basename is already registered in another APIView')

        elif route.prefix != prefix:
            raise Exception(
                'the basename is already registered in another prefix.'
                'The prefix and basename must be unique.'
            )
        else:
            wrapper_class = route.view
        setattr(wrapper_class, view.__name__, staticmethod(view))

    @overload
    def include(self, prefix: str, view: type[APIView], *, basename: str | None = None) -> None: ...

    @overload
    def include(
        self, prefix: str, view: Callable[..., Any], *, basename: str | None = None
    ) -> None: ...

    def include(
        self, prefix: str, view: type[APIView] | Callable[..., Any], *, basename: str | None = None
    ) -> None:
        basename = basename or view.__class__.__name__.lower()

        if callable(view) and is_djestful_action(view):
            self._build_wrapper_class_by_basename(prefix, view, basename)
            return
        elif not isinstance(view, type) or not issubclass(view, APIView):
            raise ImproperlyConfigured(f'The view "{view}" must be a subclass of APIView.')

        if basename in self.register:
            raise ImproperlyConfigured(f'The basename "{basename}" is already registered.')

        self.register[basename] = RouteMapping(prefix, view, basename)

    def get_view_actions(self, view: type[APIView]) -> list[Callable[..., Any]]:
        return [getattr(view, name) for name, method in getmembers(view, is_djestful_action)]

    def get_urls(self) -> Iterator[URLPattern]:
        """
        Get the list of URL patterns for the router.

        Returns:
            A list of URLPattern objects representing the registered URLs.
        """
        _urls: list[URLPattern] = []

        ## {(url, basename): [action, ...]}
        url_mapping_actions: dict[tuple[str, str], list[Callable[..., Any]]] = {}

        for basename, route in self.register.items():
            if not issubclass(route.view, APIView):
                continue

            url_mapping_actions.clear()
            for djestful_action in self.get_view_actions(route.view):
                djestful_operation: Operation = getattr(djestful_action, DJESTFUL_OPERATION)
                _normalized_url = replace_path_param_notation(
                    f'{route.prefix}{djestful_operation.path}'
                )
                url_mapping_actions.setdefault((_normalized_url, basename), []).append(
                    djestful_action
                )

            for (_url, _basename), action_list in url_mapping_actions.items():
                _actions: DictHttpMethodStr = {}
                _url_name_list: list[str] = []
                for djestful_action in action_list:
                    djestful_operation = getattr(djestful_action, DJESTFUL_OPERATION)
                    _actions.update(
                        {method: djestful_action.__name__ for method in djestful_operation.methods}
                    )
                    _url_name_list.append(
                        f'{_basename}_{djestful_operation.url_name or djestful_action.__name__}'
                    )

                _view = route.view.as_view(actions=_actions)

                for _url_name in _url_name_list:
                    yield django_path(_url, _view, name=_url_name)
