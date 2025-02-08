from collections.abc import Callable
from typing import Any

from django.urls import URLPattern, URLResolver, get_resolver

from djestful.views import APIView


def _describe_pattern(pattern: URLPattern | URLResolver) -> str:
    return str(pattern.pattern)


def _get_urls_view_mapping(prefix: str, url_pattern: list[URLResolver | URLPattern]) -> Any:
    url_view_mapping: list[tuple[str, Callable[..., Any]]] = []
    for item in url_pattern:
        _prefix = prefix + _describe_pattern(item)
        if (
            isinstance(item, URLPattern)
            and hasattr(item.callback, 'view_class')
            and issubclass(item.callback.view_class, APIView)
        ):
            url_view_mapping.append((_describe_pattern(item), item.callback))

        elif isinstance(item, URLResolver) and hasattr(item, 'url_patterns'):
            if hasattr(item, 'url_patterns'):
                url_view_mapping.extend(_get_urls_view_mapping(_prefix, item.url_patterns))

            if hasattr(item, 'callback') and item.callback:
                url_view_mapping.append((_prefix, item.callback))

    return url_view_mapping


def get_urls_view_mapping() -> list[tuple[str, Callable[..., Any]]]:
    url_pattern: list[URLResolver | URLPattern] = get_resolver().url_patterns

    url_view_mapping: list[tuple[str, Callable[..., Any]]] = _get_urls_view_mapping('', url_pattern)

    return url_view_mapping
