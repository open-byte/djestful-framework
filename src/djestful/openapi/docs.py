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
        context = self.settings

        template = Template(Path(self.template).read_text())
        html = template.render(RequestContext(request, context))

        return HttpResponse(html)
