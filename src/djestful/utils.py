from typing import Any

from djestful.constants import DJESTFUL_ATTRS
from djestful.func_attributes import FuncAttributes


def is_djestful_action(attribute: Any) -> bool:
    """
    Check if the given attribute/method is a djestful action.

    Args:
        attribute (Any): The attribute or method to check.

    Returns:
        bool: True if the attribute or method is a djestful action, False otherwise.
    """
    return hasattr(attribute, DJESTFUL_ATTRS) and isinstance(
        getattr(attribute, DJESTFUL_ATTRS), FuncAttributes
    )
