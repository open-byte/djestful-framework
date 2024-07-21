from typing import Any, Callable, Literal

HttpMethod = Literal['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

DictHttpMethodStr = dict[HttpMethod, str]
DictStrAny = dict[str, Any]
