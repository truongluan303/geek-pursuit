from dataclasses import asdict

from flask import Flask
from flask import jsonify
from flask import request
from flask import Response

from input_validator import job_info_validator
from scrapers.jobs_scrapers.exceptions import InvalidJobURL
from scrapers.jobs_scrapers.job_post_scraper import JobPostScraper


app = Flask(__name__)


_job_post_scraper = JobPostScraper()


@app.route("/job-info", methods=["GET"])
def get_job_info() -> Response:
    validation_result = job_info_validator.validate_input_args(request.args)
    if validation_result:
        return validation_result, 400

    url_or_id: str = request.args.get("job_url_or_id")

    job = int(url_or_id) if url_or_id.isnumeric() else url_or_id
    try:
        job_info = _job_post_scraper.get_job_info(job)
    except InvalidJobURL as error:
        return (
            job_info_validator.invalid_job_url_result(error.url, isinstance(job, int)),
            400,
        )

    return jsonify(
        {
            "success": True,
            "data": [asdict(job_info)],
        }
    )


if __name__ == "__main__":
    app.run()
