import json
from collections.abc import Callable
from typing import Any

from django.apps import AppConfig
from django.conf import settings as django_settings
from django.utils.module_loading import import_string

from .config import settings as djestful_settings
from .openapi.schemas import DefaultOpenAPISchema
from .urls import get_urls_view_mapping


class DjestFulConfig(AppConfig):
    name = 'djestful'
    label = 'djestful'
    verbose_name = 'Djestful Framework'

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._url_view_mapping: list[tuple[str, Callable[..., Any]]] = []
        self._openapi_schemas: dict[str, DefaultOpenAPISchema] = {
            key: import_string(klass)() for key, klass in djestful_settings.OPENAPI_SCHEMAS.items()
        }

        super().__init__(*args, **kwargs)

    def ready(self) -> None:
        self._internal_configure()
        return super().ready()

    def _internal_configure(self) -> None:
        """
        This method is called when the app is loaded.
        It is used to configure the app and add the OpenAPI URLs to the URL view mapping.
        """

        from djestful import config  # noqa: F401

        self.__add_openapi_urls()

    def get_view_for_url(self) -> None:
        self._url_view_mapping = get_urls_view_mapping()
        print(json.dumps(self._url_view_mapping, indent=4, default=str))

    def __add_openapi_urls(self) -> None:
        """
        Add the OpenAPI URLs to the URL view mapping.
        """
        try:
            root_urls = __import__(django_settings.ROOT_URLCONF, fromlist=['urlpatterns'])
            if hasattr(root_urls, 'urlpatterns'):
                root_urls.urlpatterns.extend(
                    _path
                    for schema_name, schema in self._openapi_schemas.items()
                    for _path in schema.get_openapi_urls(schema_name=schema_name)
                )

            else:
                print('No urlpatterns found in ROOT_URLCONF')
        except ImportError:
            print('Invalid ROOT_URLCONF, cannot add dynamic URLs')
