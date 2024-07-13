from functools import wraps
from typing import Any, Callable


def operation(method: str, *args, **kwargs):
    def decorator(func: Callable[..., Any]):
        setattr(func, '__djestful_flag', {'method': method})
        return func

    return decorator
