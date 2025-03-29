from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.template import RequestContext, Template
from djestful.types import DictStrAny

ABS_TPL_PATH = Path(__file__).parent.parent / 'templates/apidocs/'


class DocsBase(ABC):
    @abstractmethod
    def render_page(self, request: HttpRequest) -> HttpResponse:
        pass  # pragma: no cover

    # def get_openapi_url(self) -> str:
    #     return reverse(f'{api.urls_namespace}:openapi-json', kwargs=path_params)


class Swagger(DocsBase):
    template = ABS_TPL_PATH / 'swagger.html'
    default_settings = {
        'layout': 'BaseLayout',
        'deepLinking': True,
    }

    def __init__(self, settings: DictStrAny | None = None):
        self.settings = {}
        self.settings.update(self.default_settings)
        if settings:
            self.settings.update(settings)

    def render_page(self, request: HttpRequest, **kwargs: Any) -> HttpResponse:
        # TODO: add settings to swagger template
        # This we need to add into the settings to define the openapi
        # url and the swagger url
        context: DictStrAny = {
            'swagger_css_url': 'https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css',
            'swagger_js_url': 'https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js',
            'swagger_favicon_url': '',
            'title': 'Djestful Swagger UI',
            'openapi_url': 'https://raw.githubusercontent.com/readmeio/oas-examples/refs/heads/main/3.0/json/petstore.json',
            'openapi_json_url': 'https://raw.githubusercontent.com/readmeio/oas-examples/refs/heads/main/3.0/json/petstore.json',
        }

        template = Template(Path(self.template).read_text())
        html = template.render(RequestContext(request, context))
        return HttpResponse(html)
