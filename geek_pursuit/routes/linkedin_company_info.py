from dataclasses import asdict

from flask import jsonify
from flask import request
from flask import Response

from . import routes
from geek_pursuit.scrapers.company_profile_scraper import get_linkedin_company_info


@routes.route("/linkedin-company-info", methods=["GET"])
def linkedin_company_info() -> Response:
    company_info = get_linkedin_company_info(request.args.get("url"))
    return jsonify({"data": asdict(company_info), "success": True})
