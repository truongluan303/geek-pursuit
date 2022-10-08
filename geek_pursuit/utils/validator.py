from validators import url
from validators import ValidationFailure


def is_valid_url(url_str: str) -> bool:
    res = url(url_str)

    if isinstance(res, ValidationFailure):
        return False

    return res


def is_valid_personal_public_id(public_id: str) -> bool:
    return public_id.isalnum() and len(public_id) >= 3 and len(public_id) <= 100
