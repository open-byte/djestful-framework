from typing import Any, Callable

from djestful.constants import DJESTFUL_ATTRS
from djestful.func_attributes import FuncAttributes


def is_djestful_action(func: Callable[..., Any]) -> bool:
    """
    Check if the given function is a djestful action.

    Args:
        func (Callable[..., Any]): The function to check.

    Returns:
        bool: True if the function is a djestful action, False otherwise.
    """
    return hasattr(func, DJESTFUL_ATTRS) and isinstance(
        getattr(func, DJESTFUL_ATTRS), FuncAttributes
    )
