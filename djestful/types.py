from typing import Any, Literal

__all__ = ['HttpMethod', 'DictHttpMethodStr', 'DictStrAny']

HttpMethod = Literal['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

DictHttpMethodStr = dict[HttpMethod, str]
DictStrAny = dict[str, Any]
