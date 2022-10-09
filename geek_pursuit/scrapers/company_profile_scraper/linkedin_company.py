import logging

from geek_pursuit.scrapers.jobs_scraper.datatypes import CompanyInfo


_logger = logging.getLogger(__name__)


_COMPANY_LINK_PREFIX = "https://www.linkedin.com/company/"


def get_linkedin_company_info(company: str) -> CompanyInfo:
    pass
