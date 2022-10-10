import logging

import html2text
import requests
from bs4 import BeautifulSoup as bs

from geek_pursuit.scrapers.jobs_scraper.datatypes import JobHtmlKeys
from geek_pursuit.scrapers.jobs_scraper.datatypes import JobInfo
from geek_pursuit.scrapers.jobs_scraper.exceptions import InvalidJobURL

_logger = logging.getLogger(__name__)


HTML2TEXT: html2text.HTML2Text = html2text.HTML2Text()
HTML2TEXT.body_width = 0


def extract_from_direct_view(url: str, html_keys: JobHtmlKeys) -> JobInfo:
    """
    Extract the job information from a direct job view.
    Args:
        url (str): The URL to the job post.
    Returns:
        Optional[JobInfo]: The basic information of the job.
    """
    response = requests.get(url)
    html = response.content
    soup = bs(html, "lxml")

    posted_time_ago = soup.find_all(class_=html_keys.time_ago_key)
    if not posted_time_ago:
        _logger.error("Given URL does not contain LinkedIn job post data.")
        raise InvalidJobURL(url)
    posted_time_ago = posted_time_ago[0].get_text(strip=True)

    summary = soup.find("title").get_text()
    job_title = soup.find_all(class_=html_keys.title_key)[0].get_text(strip=True)
    company = soup.find_all(class_=html_keys.company_key)[0].get_text(strip=True)
    location = soup.find_all(class_=html_keys.location_key)[0].get_text(strip=True)
    pic_url = soup.find_all(class_=html_keys.company_pic_key)[0][html_keys.img_src_key]

    desc = soup.find_all(class_=html_keys.description_key)
    desc = desc[0]
    # remove the buttons components
    for data in desc(["button"]):
        data.decompose()
    # render the html to string
    desc = HTML2TEXT.handle(str(desc))

    return JobInfo(
        title=job_title,
        company=company,
        description=desc,
        company_pic_url=pic_url,
        location=location,
        summary=summary,
        posted_time_ago=posted_time_ago,
        url=url,
    )
