from flask import jsonify
from flask import request
from flask import Response

from . import routes
from geek_pursuit.scrapers.user_profile_scraper import get_linkedin_user_profile
from geek_pursuit.scrapers.user_profile_scraper import InvalidPersonalProfileURL
from geek_pursuit.scrapers.user_profile_scraper import InvalidPersonalPublicID


@routes.route("/linkedin-user-profile", methods=["GET"])
def user_profile() -> Response:
    if not request.args.get("url_or_public_id"):
        return (
            jsonify({"success": False, "error": "Missing param `url_or_public_id`"}),
            400,
        )
    url_or_public_id: str = request.args.get("url_or_public_id")

    try:
        profile = get_linkedin_user_profile(url_or_public_id)
    except InvalidPersonalPublicID:
        return jsonify({"success": False, "error": "Bad public ID"}), 400
    except InvalidPersonalProfileURL:
        return jsonify({"success": False, "error": "Bad profile URL"}), 400

    return jsonify({"success": True, "data": profile.to_json()})
