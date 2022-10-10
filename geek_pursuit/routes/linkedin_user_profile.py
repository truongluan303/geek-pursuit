from flask import jsonify
from flask import request
from flask import Response

from . import routes
from geek_pursuit.scrapers.company_profile_scraper import get_user_profile
from geek_pursuit.scrapers.company_profile_scraper import InvalidPersonalPublicID


@routes.route("/linkedin/linkedin-user-profile", methods=["GET"])
def user_profile() -> Response:
    url_or_public_id: str = request.args.get("url_or_public_id")
    try:
        profile = get_user_profile(url_or_public_id)
    except InvalidPersonalPublicID:
        return _invalid_personal_public_id_result(), 400
    return jsonify({"success": True, "data": [profile]})


_BAD_PUBLIC_ID_MSG = (
    "Public ID must contain 3-100 letters or numbers "
    "and no spaces, symbols, or special characters."
)


def _invalid_personal_public_id_result() -> Response:
    return jsonify(
        {
            "success": False,
            "error": _BAD_PUBLIC_ID_MSG,
        }
    )
