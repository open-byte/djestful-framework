import json
from typing import Any

from django.http import JsonResponse
from django.urls import URLPattern, URLResolver, get_resolver
from django.views import View

from djestful.views import APIView


def _describe_pattern(pattern: URLPattern) -> str:
    return str(pattern.pattern)


def get_urls_view_mapping() -> list[tuple[str, View]]:
    resolver = get_resolver()
    url_view_mapping: list[tuple[str, View]] = []

    def _get_urls_view_mapping(prefix: str, url_pattern: list[URLResolver]) -> Any:
        for item in url_pattern:
            _prefix = prefix + _describe_pattern(item)
            if (
                isinstance(item, URLPattern)
                and hasattr(item.callback, 'view_class')
                and issubclass(item.callback.view_class, APIView)
            ):
                url_view_mapping.append((_describe_pattern(item), item.callback))

            elif isinstance(item, URLResolver):
                if hasattr(item, 'url_patterns'):
                    _get_urls_view_mapping(_prefix, item.url_patterns)

                if hasattr(item, 'callback') and item.callback:
                    url_view_mapping.append((_prefix, item.callback))

    for item in resolver.url_patterns:
        if (
            isinstance(item, URLPattern)
            and hasattr(item.callback, 'view_class')
            and issubclass(item.callback.view_class, APIView)
        ):
            url_view_mapping.append((_describe_pattern(item), item.callback))

        elif isinstance(item, URLPattern) and hasattr(item.callback, '__djestful_flag'):
            url_view_mapping.append((_describe_pattern(item), item.callback))

        elif isinstance(item, URLResolver):
            if hasattr(item, 'url_patterns'):
                _get_urls_view_mapping(_describe_pattern(item), item.url_patterns)

            if hasattr(item, 'callback') and item.callback:
                url_view_mapping.append((_describe_pattern(item), item.callback))

    print(json.dumps(url_view_mapping, indent=4, default=str))
    return url_view_mapping
