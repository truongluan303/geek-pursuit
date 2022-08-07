from validators import url
from validators import ValidationFailure


def is_valid_url(url_str: str) -> bool:
    res = url(url_str)

    if isinstance(res, ValidationFailure):
        return False

    return res
