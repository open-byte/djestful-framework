from functools import partial
from uuid import uuid4

from django.urls import URLPattern, path
from djestful.types import DictStrAny

from .models import OpenAPI
from .views import openapi_json, openapi_view

## Change later


class DefaultOpenAPISchema:
    """
    This is the default OpenAPI schema for the API.
    attributes:
        title: str
            The title of the API.
        description: str | None
            A short description of the API.
        termsOfService: str | None
            A URL to the Terms of Service for the API.
        version: str
            1.0.0
        contact: dict[str, str] | None
            {
                'name': 'Person Name',
                'url': 'https://example.com',
                'email': 'person@email.com'
            }
        license: dict[str, str] | None
            {
                'name': 'MIT',
                'identifier': 'MIT',
                'url': 'https://example.com/license'
            }
        servers: list[dict[str, str]] | None
            [
                {
                    'url': '/api/v1',
                    'description': None,
                    'variables': None,
                }
            ]
        docs_url: str
            The URL for the Swagger UI.
        openapi_json_url: str
            The URL for the OpenAPI JSON schema.
        swagger_css_url: str
            The URL for the Swagger UI CSS.
        swagger_js_url: str
            The URL for the Swagger UI JS.
        swagger_favicon_url: str
            The URL for the Swagger UI favicon.
        openapi_schema: OpenAPI | None
            The OpenAPI schema for the API if you want to override the default schema.
    """

    title: str = 'Djestful API'
    description: str | None = None
    termsOfService: str | None = None
    version: str = '1.0.0'
    contact: DictStrAny | None = None
    license: DictStrAny | None = None
    servers: list[DictStrAny] | None = None
    docs_url: str = 'docs/swagger/index.html'
    openapi_json_url: str = 'docs/openapi.json'

    # Swagger UI settings
    swagger_css_url: str = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css'
    swagger_js_url: str = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js'
    swagger_favicon_url: str = ''
    ## You can set this to add an custom OpenAPI schema
    openapi_schema: OpenAPI | None = None

    def __init__(self) -> None:
        if self.openapi_schema is None:
            self.openapi_schema = OpenAPI.model_validate(
                {
                    'info': {
                        'title': self.title,
                        'description': self.description,
                        'termsOfService': self.termsOfService,
                        'contact': self.contact,
                        'license': self.license,
                        'version': self.version,
                    },
                    'servers': self.servers,
                }
            )

    def get_openapi_urls(self, schema_name: str | None = None) -> list[URLPattern]:
        if self.openapi_schema is None:
            raise ValueError('OpenAPI schema is not set. Please set the openapi_schema attribute.')

        settings = {
            'swagger_css_url': self.swagger_css_url,
            'swagger_js_url': self.swagger_js_url,
            'swagger_favicon_url': self.swagger_favicon_url,
            'title': self.title,
            'openapi_json_view_name': f'{schema_name or uuid4()}-openapi-json',
            'swagger_ui_view_name': f'{schema_name or uuid4()}-swagger-ui',
        }

        return [
            path(
                self.docs_url.removeprefix('/'),
                partial(openapi_view, settings=settings),
                name=settings['swagger_ui_view_name'],
            ),
            path(
                self.openapi_json_url.removeprefix('/'),
                partial(openapi_json, openapi_schema=self.openapi_schema),
                name=settings['openapi_json_view_name'],
            ),
        ]
