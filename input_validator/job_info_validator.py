from typing import Optional

from flask import jsonify
from flask import Response

from config import JobInfoGetParams
from utils.validator import is_valid_url


def validate_input_args(args) -> Optional[Response]:
    if not args.get(JobInfoGetParams.JOB_URL_OR_ID):
        return jsonify(
            {
                "success": False,
                "error": "missing job_url_or_id param",
            }
        )


def invalid_job_url_result(url: str, is_job_id: bool) -> Response:
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
