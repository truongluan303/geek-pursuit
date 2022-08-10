from linkedin_api import Linkedin

from config import LINKEDIN_ACCOUNT
from config import LINKEDIN_PASSWORD
from scrapers.profiles_scrapers.exceptions import InvalidPersonalProfileURL
from scrapers.profiles_scrapers.exceptions import InvalidPersonalPublicID
from utils.validator import is_valid_url


_li_api = Linkedin(LINKEDIN_ACCOUNT, LINKEDIN_PASSWORD)


_URL_PREFIX = "https://www.linkedin.com/in/"


def get_profile(url_or_public_id: str) -> dict:
    if not url_or_public_id.startswith(_URL_PREFIX):
        if (
            not url_or_public_id.isalnum()
            or len(url_or_public_id) > 100
            or len(url_or_public_id) < 100
        ):
            raise InvalidPersonalPublicID(url_or_public_id)
        url_or_public_id = f"{_URL_PREFIX}{url_or_public_id}/"

    if not is_valid_url(url_or_public_id):
        raise InvalidPersonalProfileURL(url_or_public_id)

    try:
        return _li_api.get_profile(url_or_public_id)
    except:
        raise InvalidPersonalProfileURL(url_or_public_id)
