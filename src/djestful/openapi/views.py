from typing import Any

from django.http import HttpRequest, HttpResponse
from djestful.openapi.docs import DocsBase

## Testing purpose
from .docs import Swagger

# def default_home(request: HttpRequest, *args: Any, **kwargs: Any) -> NoReturn:
#     "This view is mainly needed to determine the full path for API operations"
#     docs_url = f'{request.path}{api.docs_url}'.replace('//', '/')
#     raise Http404(f'docs_url = {docs_url}')


# def openapi_json(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
#     schema = api.get_openapi_schema(path_params=kwargs)
#     return HttpResponse(schema)


def openapi_view(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    # docs: DocsBase = api.docs
    docs: DocsBase = Swagger()
    return docs.render_page(request, *args, **kwargs)
