from typing import Iterable

from nullsafe import undefined


def compact(iter: Iterable) -> Iterable:
    """
    Remove null values from an iterable.
    """

    def not_null(val) -> bool:
        return val is not None and val is not undefined

    if isinstance(iter, dict):
        return {k: v for k, v in iter.items() if not_null(k) and not_null(v)}
    return iter.__class__(filter(lambda v: not_null(v), iter))
