from functools import wraps
from typing import Any, Callable, Literal

from djestful.func_attributes import FuncAttributes
from djestful.types import HttpMethod

from .constants import DJESTFUL_ATTRS


class action:
    def __init__(
        self,
        path: str,
        *,
        methods: list[HttpMethod],
        description: str | None = None,
        summary: str | None = None,
        url_name: str | None = None,
    ) -> None:
        self.path = path
        self.methods = methods
        self.description = description
        self.summary = summary
        self.url_name = url_name

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        djestful_attrs = FuncAttributes(
            methods=self.methods,
            path=self.path,
            url_name=self.url_name,
        )
        setattr(func, DJESTFUL_ATTRS, djestful_attrs)
        return func

    @classmethod
    def get(
        cls,
        path: str,
        *,
        description: str | None = None,
        summary: str | None = None,
        url_name: str | None = None,
    ) -> Callable[..., Any]:
        """
        Decorator for defining a POST endpoint.

        Args:
            path (str): The URL path for the endpoint.
            description (str, optional): A description of the endpoint. Defaults to None.
            summary (str, optional): A summary of the endpoint. Defaults to None.

        Returns:
            Callable[..., Any]: The decorated function.
        """
        return cls(
            path,
            methods=['get'],
            description=description,
            summary=summary,
            url_name=url_name,
        )

    @classmethod
    def post(
        cls,
        path: str,
        *,
        description: str | None = None,
        summary: str | None = None,
        url_name: str | None = None,
    ) -> Callable[..., Any]:
        """
        Decorator for defining a POST endpoint.

        Args:
            path (str): The URL path for the endpoint.
            description (str, optional): A description of the endpoint. Defaults to None.
            summary (str, optional): A summary of the endpoint. Defaults to None.

        Returns:
            Callable[..., Any]: The decorated function.
        """
        return cls(
            path,
            methods=['post'],
            description=description,
            summary=summary,
            url_name=url_name,
        )

    @classmethod
    def put(
        cls,
        path: str,
        *,
        description: str | None = None,
        summary: str | None = None,
        url_name: str | None = None,
    ) -> Callable[..., Any]:
        """
        Decorator for defining a PUT endpoint.

        Args:
            path (str): The URL path for the endpoint.
            description (str, optional): A description of the endpoint. Defaults to None.
            summary (str, optional): A summary of the endpoint. Defaults to None.

        Returns:
            Callable[..., Any]: The decorated function.
        """
        return cls(
            path,
            methods=['put'],
            description=description,
            summary=summary,
            url_name=url_name,
        )

    @classmethod
    def patch(
        cls,
        path: str,
        *,
        description: str | None = None,
        summary: str | None = None,
        url_name: str | None = None,
    ) -> Callable[..., Any]:
        """
        Decorator for defining a PATCH endpoint.

        Args:
            path (str): The URL path for the endpoint.
            description (str, optional): A description of the endpoint. Defaults to None.
            summary (str, optional): A summary of the endpoint. Defaults to None.

        Returns:
            Callable[..., Any]: The decorated function.
        """
        return cls(
            path,
            methods=['patch'],
            description=description,
            summary=summary,
            url_name=url_name,
        )

    @classmethod
    def delete(
        cls,
        path: str,
        *,
        description: str | None = None,
        summary: str | None = None,
        url_name: str | None = None,
    ) -> Callable[..., Any]:
        """
        Decorator for defining a DELETE endpoint.

        Args:
            path (str): The URL path for the endpoint.
            description (str, optional): A description of the endpoint. Defaults to None.
            summary (str, optional): A summary of the endpoint. Defaults to None.

        Returns:
            Callable[..., Any]: The decorated function.
        """
        return cls(
            path,
            methods=['delete'],
            description=description,
            summary=summary,
            url_name=url_name,
        )

    @classmethod
    def generic(
        cls,
        path: str,
        *,
        methods: list[HttpMethod],
        description: str | None = None,
        summary: str | None = None,
        url_name: str | None = None,
    ) -> Callable[..., Any]:
        """
        Decorator for defining a generic endpoint.

        Args:
            path (str): The URL path for the endpoint.
            methods (list[str]): The HTTP methods allowed for the endpoint.
            description (str, optional): A description of the endpoint. Defaults to None.
            summary (str, optional): A summary of the endpoint. Defaults to None.

        Returns:

        """
        return cls(
            path,
            methods=methods,
            description=description,
            summary=summary,
            url_name=url_name,
        )
