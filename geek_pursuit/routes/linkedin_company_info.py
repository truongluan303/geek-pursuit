from flask import jsonify
from flask import request
from flask import Response

from . import routes
from geek_pursuit.scrapers.company_profile_scraper import get_linkedin_company_info
from geek_pursuit.scrapers.company_profile_scraper import InvalidLinkedInCompanyURL
from geek_pursuit.utils.iter_utils import compact


class LinkedInCompanyInfoGetParams:
    URL_OR_COMPANY_NAME: str = "url_or_company_name"


@routes.route("/linkedin-company-info", methods=["GET"])
def linkedin_company_info() -> Response:
    if not request.args.get(LinkedInCompanyInfoGetParams.URL_OR_COMPANY_NAME):
        return (
            jsonify(
                {
                    "success": False,
                    "errors": [
                        f"missing {LinkedInCompanyInfoGetParams.URL_OR_COMPANY_NAME} param"
                    ],
                }
            ),
            400,
        )

    try:
        company_info = get_linkedin_company_info(
            request.args.get(LinkedInCompanyInfoGetParams.URL_OR_COMPANY_NAME)
        )
    except InvalidLinkedInCompanyURL:
        return (
            jsonify(
                {
                    "success": False,
                    "errors": ["The given URL or linkedin company name is invalid"],
                }
            ),
            400,
        )

    return jsonify({"data": compact(company_info.to_dict()), "success": True})
