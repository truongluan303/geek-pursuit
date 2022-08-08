import logging
import re
from dataclasses import dataclass
from datetime import timedelta
from typing import Optional
from typing import Union

import html2text
import requests
from bs4 import BeautifulSoup as bs

from scrapers.jobs_scrapers.exceptions import InvalidJobURL


_logger = logging.getLogger(__name__)


@dataclass
class JobInfo:
    title: str = None
    company: str = None
    description: str = None
    location: str = None
    posted_time_ago: timedelta = None
    summary: str = None
    company_pic_url: str = None
    url: str = None


class JobPostScraper:
    """
    Represents a LinkedIn job board
    """

    def __init__(self) -> None:
        self._TITLE_KEY = "top-card-layout__title"
        self._COMPANY_KEY = "topcard__org-name-link"
        self._COMPANY_PIC_KEY = "sub-nav-cta__image"
        self._IMG_SRC_KEY = "data-delayed-url"
        self._TIME_AGO_KEY = "posted-time-ago__text"
        self._DESCRIPTION_KEY = "description__text"
        self._LOCATION_KEY = "sub-nav-cta__meta-text"

        self._VIEW_LINK_PREFIX = "https://www.linkedin.com/jobs/view"
        self._RECOMMENDED_LINK_REGEX = re.compile(r".*\?currentJobId=[0-9]*")

        self._HTML2TEXT: html2text.HTML2Text = html2text.HTML2Text()
        self._HTML2TEXT.body_width = 0

    def get_job_info(self, job: Union[str, int]) -> Optional[JobInfo]:
        is_direct_view = False

        if isinstance(job, int):
            job = self._url_from_job_id(job)
            is_direct_view = True

        given_job_url = job

        is_direct_view = job.startswith(self._VIEW_LINK_PREFIX)

        # If a link is not a direct view link, there is a possible case that it is a
        # job in a list containing multiple jobs. For example, on LinkedIn, if you click on
        # jobs recommended for you, you will see a split view where on the left hand
        # you can browse jobs and on the right hand you can view the current selected job
        # information. In this case, we want to extract the current selected job only.
        #
        if not is_direct_view:
            if self._is_in_recommended_list(job):
                job_id = self._extract_current_job_id(job)
                job = self._url_from_job_id(job_id)
            else:
                _logger.error(f"Job ULR is not a valid URL: {given_job_url}")
                raise InvalidJobURL(given_job_url)

        # If the job is a directly viewed one, we want to grab only the url resource
        # patch and ignore all the query parameters so we can get a clean url.
        #
        else:
            job = job.split("?")[0]

        try:
            return self._extract_from_direct_view(job)
        except:
            _logger.error(f"Job ULR is not a valid URL: {given_job_url}")
            raise InvalidJobURL(given_job_url)

    def _extract_from_direct_view(self, url: str) -> JobInfo:
        """
        Extract the job information from a direct job view.
        Args:
            url (str): The URL to the job post on LinkedIn.
        Returns:
            Optional[JobInfo]: The basic information of the job.
        """
        response = requests.get(url)
        html = response.content
        soup = bs(html, "lxml")

        posted_time_ago = soup.find_all(class_=self._TIME_AGO_KEY)
        if not posted_time_ago:
            _logger.error("Given URL does not contain LinkedIn job post data.")
            raise InvalidJobURL(url)
        posted_time_ago = posted_time_ago[0].get_text(strip=True)

        summary = soup.find("title").get_text()
        job_title = soup.find_all(class_=self._TITLE_KEY)[0].get_text(strip=True)
        company = soup.find_all(class_=self._COMPANY_KEY)[0].get_text(strip=True)
        location = soup.find_all(class_=self._LOCATION_KEY)[0].get_text(strip=True)
        pic_url = soup.find_all(class_=self._COMPANY_PIC_KEY)[0][self._IMG_SRC_KEY]

        desc = soup.find_all(class_=self._DESCRIPTION_KEY)
        desc = desc[0]
        # remove the buttons components
        for data in desc(["button"]):
            data.decompose()
        # render the html to string
        desc = self._HTML2TEXT.handle(str(desc))

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

    def _is_in_recommended_list(self, url: str) -> bool:
        return self._RECOMMENDED_LINK_REGEX.search(url)

    def _extract_current_job_id(self, url: str) -> str:
        return self._RECOMMENDED_LINK_REGEX.findall(url)[0].split("=")[-1]

    def _url_from_job_id(self, job_id: Union[str, int]) -> str:
        return f"{self._VIEW_LINK_PREFIX}/{job_id}/"
