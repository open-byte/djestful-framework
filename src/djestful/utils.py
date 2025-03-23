from collections.abc import Callable
from typing import Any

from djestful.constants import DJESTFUL_OPERATION
from djestful.operation import Operation


def is_djestful_action(func: Callable[..., Any]) -> bool:
    """
    Check if the given function is a djestful action.

    Args:
        func (Callable[..., Any]): The function to check.

    Returns:
        bool: True if the function is a djestful action, False otherwise.
    """
    return hasattr(func, DJESTFUL_OPERATION) and isinstance(
        getattr(func, DJESTFUL_OPERATION), Operation
    )


def replace_path_param_notation(path: str) -> str:
    """
    Replace the path parameter notation with the Django path parameter notation.

    Args:
        path (str): The path to replace.

    Returns:
        str: The path with the Django path parameter notation.
    """
    return path.replace('{', '<').replace('}', '>')
