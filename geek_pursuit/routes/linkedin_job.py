from dataclasses import asdict
from typing import Optional

from flask import jsonify
from flask import request
from flask import Response

from . import routes
from geek_pursuit.scrapers.jobs_scraper import get_linkedin_job_info
from geek_pursuit.scrapers.jobs_scraper import InvalidJobURL
from geek_pursuit.utils.validator import is_valid_url


class JobInfoGetParams:
    JOB_URL_OR_ID = "job_url_or_id"


@routes.route("/linkedin-job-info", methods=["GET"])
def job_info() -> Response:
    validation_result = _validate_input_args(request.args)
    if validation_result:
        return validation_result, 400

    url_or_id: str = request.args.get("job_url_or_id")

    job = int(url_or_id) if url_or_id.isnumeric() else url_or_id
    try:
        job_info = get_linkedin_job_info(job)
    except InvalidJobURL as error:
        return (
            _invalid_job_url_result(error.url, isinstance(job, int)),
            400,
        )

    return jsonify(
        {
            "success": True,
            "data": [asdict(job_info)],
        }
    )


def _invalid_job_url_result(url: str, is_job_id: bool) -> Response:
    if is_job_id:
        message = "Cannot find a job with the given job ID."
    elif not is_valid_url(url):
        message = "The given URL is not a valid URL."
    elif not url.startswith("https://www.linkedin.com/jobs/"):
        message = "The given URL is not a LinkedIn job URL."
    else:
        message = "Unable to extract job information from the given URL"
    return jsonify(
        {
            "success": False,
            "error": message,
        }
    )


def _validate_input_args(args) -> Optional[Response]:
    if not args.get(JobInfoGetParams.JOB_URL_OR_ID):
        return jsonify(
            {
                "success": False,
                "error": "missing job_url_or_id param",
            }
        )
