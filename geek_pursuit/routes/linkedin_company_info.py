from flask import jsonify
from flask import request
from flask import Response

from . import routes
from geek_pursuit.scrapers.helper import generate_driver


_webdriver = generate_driver()


@routes.route("/linkedin-company-info", methods=["GET"])
def company_info() -> Response:
    _webdriver.get(request.args.get("url"))

    with open("tempfile.html", "w") as f:
        f.write(_webdriver.page_source)

    return jsonify({"success": True})
