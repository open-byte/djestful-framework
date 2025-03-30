from typing import TYPE_CHECKING, Any

from django.http import HttpRequest, HttpResponse, JsonResponse
from djestful.openapi.docs import DocsBase
from djestful.types import DictStrAny

## Testing purpose
from .docs import Swagger

# def default_home(request: HttpRequest, *args: Any, **kwargs: Any) -> NoReturn:
#     "This view is mainly needed to determine the full path for API operations"
#     docs_url = f'{request.path}{api.docs_url}'.replace('//', '/')
#     raise Http404(f'docs_url = {docs_url}')

if TYPE_CHECKING:
    from .models import OpenAPI


def openapi_json(request: HttpRequest, openapi_schema: 'OpenAPI', **kwargs: Any) -> HttpResponse:
    schema = openapi_schema.model_dump()
    return JsonResponse(schema)


def openapi_view(request: HttpRequest, settings: DictStrAny, **kwargs: Any) -> HttpResponse:
    # docs: DocsBase = api.docs
    docs: DocsBase = Swagger(settings=settings)
    return docs.render_page(request, **kwargs)
