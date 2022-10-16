from typing import Any

from nullsafe import undefined


def nullreplace(value: Any, default: Any):
    return default if value in (None, undefined) else value
