import logging
from typing import Optional
from typing import Union

from scrapers.jobs_scraper.datatypes import JobInfo


_logger = logging.getLogger(__name__)


def get_job_info(job: Union[str, int]) -> Optional[JobInfo]:
    pass
