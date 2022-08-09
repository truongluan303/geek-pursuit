from unittest import mock

from bs4 import BeautifulSoup as bs


def _read_mock_request_content(file: str) -> bytes:
    with open(file, "rb") as f:
        mocked_html = f.read()
    return bs(mocked_html)


@mock.patch(
    "scrapers.jobs_scapers.job_post_scraper.JobPostScraper._get_soup_from_url",
    _read_mock_request_content("tests/jobs_scrapers/data/mock.html"),
)
def test_get_job_info():
    pass
