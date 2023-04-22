from flask import jsonify
from flask import request
from flask import Response

from . import routes
from geek_pursuit.linkedin import linkedin_api_instance


@routes.route("/linkedin-user-profile", methods=["GET"])
def user_profile() -> Response:
    if not request.args.get("url_or_public_id"):
        return (
            jsonify({"success": False, "error": "Missing param `url_or_public_id`"}),
            400,
        )
    url_or_public_id: str = request.args.get("url_or_public_id")

    profile: dict = linkedin_api_instance.get_profile(url_or_public_id)
    if not profile:
        return jsonify({"success": False, "error": "Bad profile URL"}), 400

    return jsonify({"success": True, "data": profile})
