from geek_pursuit.scrapers.profile_scraper.exceptions import InvalidPersonalProfileURL
from geek_pursuit.scrapers.profile_scraper.exceptions import InvalidPersonalPublicID
from geek_pursuit.utils.validator import is_valid_personal_public_id
from geek_pursuit.utils.validator import is_valid_url


_URL_PREFIX = "https://www.linkedin.com/in/"


def get_profile(url_or_public_id: str) -> dict:
    if url_or_public_id.startswith(_URL_PREFIX):
        if not is_valid_url(url_or_public_id):
            raise InvalidPersonalProfileURL(url_or_public_id)
        url_or_public_id = url_or_public_id.replace(_URL_PREFIX, "").split("/")[0]

    if not is_valid_personal_public_id(url_or_public_id):
        raise InvalidPersonalPublicID(url_or_public_id)

    try:
        return {}
    except:
        raise InvalidPersonalProfileURL(url_or_public_id)
