from abc import ABC, abstractmethod
from collections.abc import Callable
from inspect import getmembers
from typing import Any

from django.core.exceptions import ImproperlyConfigured
from django.urls import URLPattern
from django.urls import path as django_path

from djestful.constants import DJESTFUL_ATTRS
from djestful.func_attributes import FuncAttributes
from djestful.types import DictHttpMethodStr
from djestful.utils import is_djestful_action
from djestful.views import APIView

RouteMapping = tuple[str, type[APIView], str]


class BaseRouter(ABC):
    def __init__(self) -> None:
        self.register: list[RouteMapping] = []

    @abstractmethod
    def include(self, *args: Any, **kwargs: Any) -> None: ...

    @abstractmethod
    def get_urls(self) -> list[URLPattern]: ...

    @property
    def urls(self) -> list[URLPattern]:
        return self.get_urls()


class Router(BaseRouter):
    def include(self, prefix: str, view: type[APIView], *, basename: str | None = None) -> None:
        basename = basename or view.__class__.__name__.lower()

        ## check if the basename is already registered
        for _, _, registered_basename in self.register:
            if registered_basename == basename:
                raise ImproperlyConfigured(f'The basename "{basename}" is already registered.')

        self.register.append((prefix, view, basename))

    def get_view_actions(self, view: type[APIView]) -> list[Callable[..., Any]]:
        return [getattr(view, name) for name, method in getmembers(view, is_djestful_action)]

    def get_urls(self) -> list[URLPattern]:
        """
        Get the list of URL patterns for the router.

        Returns:
            A list of URLPattern objects representing the registered URLs.
        """
        _urls: list[URLPattern] = []

        ## {(url, basename): [action, ...]}
        url_mapping_actions: dict[tuple[str, str], list[Callable[..., Any]]] = {}

        for prefix, view, basename in self.register:
            url_mapping_actions.clear()

            for djestful_action in self.get_view_actions(view):
                djestful_attrs: FuncAttributes = getattr(djestful_action, DJESTFUL_ATTRS)
                url_mapping_actions.setdefault(
                    (f'{prefix}{djestful_attrs.path}', basename), []
                ).append(djestful_action)

            for (_url, _basename), action_list in url_mapping_actions.items():
                _actions: DictHttpMethodStr = {}
                _url_name_list: list[str] = []
                for djestful_action in action_list:
                    djestful_attrs = getattr(djestful_action, DJESTFUL_ATTRS)
                    _actions.update(
                        {method: djestful_action.__name__ for method in djestful_attrs.methods}
                    )
                    _url_name_list.append(
                        f'{_basename}_{djestful_attrs.url_name or djestful_action.__name__}'
                    )

                _view = view.as_view(actions=_actions)
                _urls.extend(
                    [django_path(_url, _view, name=url_name) for url_name in _url_name_list]
                )
        return _urls
