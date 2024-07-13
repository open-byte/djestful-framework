import json
from typing import Any, Callable

from django.apps import AppConfig
from django.urls import get_resolver

from djestful.urls import get_urls_view_mapping


class DjestFulConfig(AppConfig):
    name = 'djestful'
    label = 'djestful'
    verbose_name = 'Djestful Framework'

    def __init__(self, *args, **kwargs) -> None:
        self._url_view_mapping: list[tuple[str, Callable[...]]] = []

        super().__init__(*args, **kwargs)

    def ready(self) -> None:
        self.get_view_for_url()
        return super().ready()

    def get_view_for_url(self) -> None:
        self._url_view_mapping = get_urls_view_mapping()
