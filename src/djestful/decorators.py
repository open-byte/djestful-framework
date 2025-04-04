from collections.abc import Callable
from typing import Any

from djestful.operation import Operation
from djestful.types import HttpMethod

from .constants import DJESTFUL_OPERATION


class action:
    def __init__(
        self,
        path: str,
        *,
        methods: list[HttpMethod],
        summary: str | None = None,
        description: str | None = None,
        url_name: str | None = None,
    ) -> None:
        self.path = path
        self.methods = methods
        self.description = description
        self.summary = summary
        self.url_name = url_name

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        djestful_operation = Operation(
            view_func=func,
            path=self.path,
            methods=self.methods,
            description=self.description,
            summary=self.summary,
            url_name=self.url_name,
        )
        setattr(func, DJESTFUL_OPERATION, djestful_operation)

        return func

    @classmethod
    def get(
        cls,
        path: str,
        *,
        summary: str | None = None,
        description: str | None = None,
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
        summary: str | None = None,
        description: str | None = None,
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
            summary=summary,
            description=description,
            url_name=url_name,
        )

    @classmethod
    def put(
        cls,
        path: str,
        *,
        summary: str | None = None,
        description: str | None = None,
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
            summary=summary,
            description=description,
            url_name=url_name,
        )

    @classmethod
    def patch(
        cls,
        path: str,
        *,
        summary: str | None = None,
        description: str | None = None,
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
            summary=summary,
            description=description,
            url_name=url_name,
        )

    @classmethod
    def delete(
        cls,
        path: str,
        *,
        summary: str | None = None,
        description: str | None = None,
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
            summary=summary,
            description=description,
            url_name=url_name,
        )

    @classmethod
    def generic(
        cls,
        path: str,
        *,
        methods: list[HttpMethod],
        summary: str | None = None,
        description: str | None = None,
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
            summary=summary,
            description=description,
            url_name=url_name,
        )
