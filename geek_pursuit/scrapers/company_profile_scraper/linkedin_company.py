from functools import lru_cache
from json import loads

import validators
from bs4 import BeautifulSoup
from nullsafe import _

from geek_pursuit.scrapers.company_profile_scraper.datatypes import CompanyInfo
from geek_pursuit.scrapers.company_profile_scraper.exceptions import (
    InvalidLinkedInCompanyURL,
)
from geek_pursuit.scrapers.helper import html_source_from_js_site
from geek_pursuit.utils.iter_utils import compact
from geek_pursuit.utils.string_utils import clean_whitespace

_COMPANY_LINK_PREFIX = "https://www.linkedin.com/company/"


def get_linkedin_company_info(url_or_company_name: str) -> CompanyInfo:
    is_linkedin_comapny_url = url_or_company_name.startswith(_COMPANY_LINK_PREFIX)
    if validators.url(url_or_company_name) and not is_linkedin_comapny_url:
        raise InvalidLinkedInCompanyURL

    company_name = url_or_company_name.replace(_COMPANY_LINK_PREFIX, "").split("/")[0]
    url = f"{_COMPANY_LINK_PREFIX}{company_name}"

    return _get_linkedin_company_info(url)


@lru_cache(maxsize=500)
def _get_linkedin_company_info(url) -> CompanyInfo:
    htmlsrc = html_source_from_js_site(url)
    soup = BeautifulSoup(htmlsrc, "html.parser")

    if soup.find(attrs={"class": "top-card-layout__title"}) is None:
        raise InvalidLinkedInCompanyURL

    company_info_dict = CompanyInfo(
        name=soup.find(attrs={"class": "top-card-layout__title"}),
        industry=clean_whitespace(
            _(soup.find(attrs={"data-test-id": "about-us__industries"}))
            .find("dd")
            .get_text()
        ),
        head_quarters_locations=(
            None
            if not soup.find(attrs={"data-test-id": "about-us__headquarters"})
            else [
                clean_whitespace(dd.get_text())
                for dd in soup.find(
                    attrs={"data-test-id": "about-us__headquarters"}
                ).find_all("dd")
            ]
        ),
        all_locations=None,
        founded_time=clean_whitespace(
            _(soup.find(attrs={"data-test-id": "about-us__foundedOn"}))
            .find("dd")
            .get_text()
        ),
        company_type=clean_whitespace(
            _(soup.find(attrs={"data-test-id": "about-us__organizationType"}))
            .find("dd")
            .get_text()
        ),
        specialties=clean_whitespace(
            _(soup.find(attrs={"data-test-id": "about-us__specialties"}))
            .find("dd")
            .get_text()
        ),
        slogan=clean_whitespace(_(soup.find("line-clamp-2")).get_text()),
        description=clean_whitespace(
            _(
                soup.find("p", attrs={"data-test-id": "about-us__description"})
            ).get_text()
        ),
        number_of_linkedin_followers=(
            _(
                soup.find(
                    attrs={
                        "class": "text-xs text-color-text-low-emphasis leading-[1.33333] m-0 truncate"
                    },
                )
            )
            .get_text()
            .strip()
            .split()[0]
            .replace(",", "")
        ),
    ).to_dict()

    # if there is a script tag, get the data there
    # we then can combine both the data collected from the script tag and the data
    # collected from other html elements to get the most data we can
    script_soup = soup.find("script", attrs={"type": "application/ld+json"})
    data_from_script: dict = None if not script_soup else loads(script_soup.get_text())
    data_from_script["linkedin_url"] = data_from_script.pop("url", None)
    data_from_script["website"] = data_from_script.pop("sameAs", None)
    data_from_script["logo"] = data_from_script.pop("logo", {}).get("contentUrl", None)
    data_from_script["number_of_employees"] = data_from_script.pop(
        "numberOfEmployees", {}
    ).get("value")

    company_info_dict_from_script = CompanyInfo(
        **{
            k: v.strip() if isinstance(v, str) else v
            for k, v in data_from_script.items()
            if k
            in (
                "description",
                "logo_url",
                "name",
                "number_of_employees",
                "slogan",
                "linkedin_url",
                "website",
                "logo",
            )
            and v is not None
        }
    ).to_dict()

    return CompanyInfo(
        **{**compact(company_info_dict), **compact(company_info_dict_from_script)}
    )
