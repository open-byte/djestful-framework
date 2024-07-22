import logging
from inspect import getmembers
from typing import Any, Callable

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
        self.handlers: list[Callable[..., Any]] = []

    @classproperty
    def view_is_async(cls) -> bool:  # type: ignore[override]
        """
        Check if the view is asynchronous.

        Returns:
            bool: True if the view is asynchronous, False otherwise.

        Raises:
            ImproperlyConfigured: If the HTTP handlers are not all synchronous or all asynchronous.
        """
        handlers = cls.handlers

        if not handlers:
            return False
        is_async = iscoroutinefunction(handlers[0])
        if not all(iscoroutinefunction(h) == is_async for h in handlers[1:]):
            raise ImproperlyConfigured(
                f'{cls.__qualname__} HTTP handlers must either be all sync or all ' 'async.'  # type: ignore[attr-defined]
            )
        return is_async

    @classonlymethod
    def as_view(
        cls, actions: DictHttpMethodStr | None = None, **initkwargs: Any
    ) -> Callable[..., Any]:
        """
        This method is used to create a view function that handles incoming requests and generates
        appropriate responses. It is typically called by the URL routing mechanism to associate a
        URL pattern with a view.

        Args:
            cls (type): The class object that the view function is being created for.
            actions (dict or None): A dictionary that maps HTTP methods to method names. Each key
                represents an HTTP method (e.g., 'get', 'post') and the corresponding value is the
                name of the method in the class that should be called for that HTTP method. If None,
                an ImproperlyConfigured exception is raised.
            **initkwargs (dict): Additional keyword arguments that are passed to the class
                constructor when creating an instance of the class.

        Returns:
            Callable[..., Any]: The view function that handles the request and generates the
            response.

        Raises:
            ImproperlyConfigured: If `actions` is None.
            TypeError: If `actions` is not a dictionary or if any of the keyword arguments in
                `initkwargs` are not valid attributes of the class.

        """

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
        view.actions = actions  # type: ignore[attr-defined]

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

        # Mark the callback if the view class is async.
        if cls.view_is_async:
            markcoroutinefunction(view)

        return csrf_exempt(view)

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Any:
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        method = request.method.lower()  # type: ignore[union-attr]
        if method not in self.http_method_names:
            handler = self.http_method_not_allowed

        else:
            handler = getattr(self, method)

            if not is_djestful_action(handler):
                handler = self.http_method_not_allowed

        return handler(request, *args, **kwargs)

    # def __check_pattern_path_with_the_same_method(self, request: HttpRequest) -> bool:
    #     """
    #     Check if the request path matches the pattern path and the request method matches the
    #     pattern method.

    #     Args:
    #         request (HttpRequest): The incoming request.

    #     Returns:
    #         bool: True if the request path matches the pattern path and the request method matches
    #         the pattern method, False otherwise.
    #     """
    #     return request.path == reverse(self.__class__.__name__.
