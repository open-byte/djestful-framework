import logging
from inspect import getmembers
from typing import Any

from asgiref.sync import iscoroutinefunction, markcoroutinefunction
from django.core.exceptions import ImproperlyConfigured
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseGone,
    HttpResponseNotAllowed,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.decorators import classonlymethod
from django.utils.functional import classproperty
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from djestful.constants import DJESTFUL_ATTRS
from djestful.types import DictHttpMethodStr
from djestful.utils import is_djestful_action


class APIView(View):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    @classproperty
    def view_is_async(cls):
        handlers = cls.handlers
        if not handlers:
            return False
        is_async = iscoroutinefunction(handlers[0])
        if not all(iscoroutinefunction(h) == is_async for h in handlers[1:]):
            raise ImproperlyConfigured(
                f'{cls.__qualname__} HTTP handlers must either be all sync or all ' 'async.'
            )
        return is_async

    @classonlymethod
    def as_view(cls, actions: DictHttpMethodStr | None = None, **initkwargs: Any) -> Any:
        """Main entry point for a request-response process."""

        if actions is None:  ## change this
            raise ImproperlyConfigured(
                f"'{cls.__name__}' should be called with an action method."
                "For example, MyView.as_view(action={'get': 'list'})."
            )

        if not isinstance(actions, dict):
            raise TypeError(
                f'The actions parameter must be a dictionary, not {type(actions).__name__}.'
                'For example, {"get": "list", "post": "create"}, '
                ' keys are HTTP methods and values are method names.'
            )

        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError(
                    f'The method name {key} is not accepted as a keyword argument '
                    f'to {cls.__name__}().'
                )
            if not hasattr(cls, key):
                raise TypeError(
                    f'{cls.__name__}() received an invalid keyword {key!r}. as_view '
                    'only accepts arguments that are already '
                    'attributes of the class.'
                )

        def view(request: HttpRequest, *args: Any, **kwargs: Any) -> Any:
            self = cls(**initkwargs)

            for http_method, action in actions.items():
                handler = getattr(self, action)
                setattr(self, http_method, handler)

            self.setup(request, *args, **kwargs)

            if not hasattr(self, 'request'):
                raise AttributeError(
                    f"{cls.__name__} instance has no 'request' attribute. Did you override "
                    'setup() and forget to call super()?'
                )
            return self.dispatch(request, *args, **kwargs)

        view.view_class = cls  # type: ignore[attr-defined]
        view.view_initkwargs = initkwargs  # type: ignore[attr-defined]

        # __name__ and __qualname__ are intentionally left unchanged as
        # view_class should be used to robustly determine the name of the view
        # instead.
        view.__doc__ = cls.__doc__
        view.__module__ = cls.__module__
        view.__annotations__ = cls.dispatch.__annotations__
        # Copy possible attributes set by decorators, e.g. @csrf_exempt, from
        # the dispatch method.
        view.__dict__.update(cls.dispatch.__dict__)

        cls.handlers = [getattr(cls, name) for name, method in getmembers(cls, is_djestful_action)]
        print(cls.handlers)
        # Mark the callback if the view class is async.
        if cls.view_is_async:
            markcoroutinefunction(view)

        return csrf_exempt(view)
