import logging
import re
from typing import Optional
from typing import Union

from geek_pursuit.scrapers.jobs_scraper.base import extract_from_direct_view
from geek_pursuit.scrapers.jobs_scraper.datatypes import JobHtmlKeys
from geek_pursuit.scrapers.jobs_scraper.datatypes import JobInfo
from geek_pursuit.scrapers.jobs_scraper.exceptions import InvalidJobURL


_logger = logging.getLogger(__name__)


_VIEW_LINK_PREFIX = "https://www.linkedin.com/jobs/view"
_RECOMMENDED_LINK_REGEX = re.compile(r".*\?currentJobId=[0-9]*")


def get_job_info(job: Union[str, int]) -> Optional[JobInfo]:
    is_direct_view = False

    if isinstance(job, int):
        job = _url_from_job_id(job)
        is_direct_view = True

    given_job_url = job

    is_direct_view = job.startswith(_VIEW_LINK_PREFIX)

    # If a link is not a direct view link, there is a possible case that it is a
    # job in a list containing multiple jobs. For example, on LinkedIn, if you click on
    # jobs recommended for you, you will see a split view where on the left hand
    # you can browse jobs and on the right hand you can view the current selected job
    # information. In this case, we want to extract the current selected job only.
    #
    if not is_direct_view:
        if _is_in_recommended_list(job):
            job_id = _extract_current_job_id(job)
            job = _url_from_job_id(job_id)
        else:
            _logger.error(f"Job ULR is not a valid URL: {given_job_url}")
            raise InvalidJobURL(given_job_url)

    # If the job is a directly viewed one, we want to grab only the url resource
    # patch and ignore all the query parameters so we can get a clean url.
    #
    else:
        job = job.split("?")[0]

    try:
        return extract_from_direct_view(
            job,
            JobHtmlKeys(
                title_key="top-card-layout__title",
                company_key="topcard__org-name-link",
                company_pic_key="sub-nav-cta__image",
                img_src_key="data-delayed-url",
                time_ago_key="posted-time-ago__text",
                description_key="description__text",
                location_key="sub-nav-cta__meta-text",
            ),
        )
    except:
        _logger.error(f"Job ULR is not a valid URL: {given_job_url}")
        raise InvalidJobURL(given_job_url)


def _is_in_recommended_list(url: str) -> bool:
    return _RECOMMENDED_LINK_REGEX.search(url)


def _extract_current_job_id(url: str) -> str:
    return _RECOMMENDED_LINK_REGEX.findall(url)[0].split("=")[-1]


def _url_from_job_id(job_id: Union[str, int]) -> str:
    return f"{_VIEW_LINK_PREFIX}/{job_id}/"
