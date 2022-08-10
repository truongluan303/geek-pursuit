from linkedin_api import Linkedin

from config import LINKEDIN_ACCOUNT
from config import LINKEDIN_PASSWORD
from linkedin_api_wrapper.exceptions import InvalidPersonalProfileURL
from linkedin_api_wrapper.exceptions import InvalidPersonalPublicID
from utils.validator import is_valid_personal_public_id
from utils.validator import is_valid_url


_li_api = Linkedin(LINKEDIN_ACCOUNT, LINKEDIN_PASSWORD)


_URL_PREFIX = "https://www.linkedin.com/in/"


def get_profile(url_or_public_id: str) -> dict:
    if url_or_public_id.startswith(_URL_PREFIX):
        if not is_valid_url(url_or_public_id):
            raise InvalidPersonalProfileURL(url_or_public_id)
        url_or_public_id = url_or_public_id.replace(_URL_PREFIX, "").split("/")[0]

    if not is_valid_personal_public_id(url_or_public_id):
        raise InvalidPersonalPublicID(url_or_public_id)

    try:
        return _li_api.get_profile(url_or_public_id)
    except:
        raise InvalidPersonalProfileURL(url_or_public_id)
