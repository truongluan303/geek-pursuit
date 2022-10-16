import logging
from typing import List
from typing import Optional

import html2text
from bs4 import BeautifulSoup
from nullsafe import _

from geek_pursuit.scrapers.helper import generate_driver
from geek_pursuit.scrapers.helper import soup_from_js_site
from geek_pursuit.scrapers.linkedin_helper import LinkedinURLHelper
from geek_pursuit.scrapers.user_profile_scraper.datatypes import Education
from geek_pursuit.scrapers.user_profile_scraper.datatypes import Experience
from geek_pursuit.scrapers.user_profile_scraper.datatypes import Profile
from geek_pursuit.scrapers.user_profile_scraper.exceptions import (
    InvalidPersonalProfileURL,
)
from geek_pursuit.scrapers.user_profile_scraper.exceptions import (
    InvalidPersonalPublicID,
)
from geek_pursuit.utils.iter_utils import compact
from geek_pursuit.utils.string_utils import clean_whitespace
from geek_pursuit.utils.type_utils import nullreplace
from geek_pursuit.utils.validator import is_valid_linkedin_personal_public_id
from geek_pursuit.utils.validator import is_valid_url


HTML2TEXT: html2text.HTML2Text = html2text.HTML2Text()
HTML2TEXT.body_width = 0

_logger = logging.getLogger(__name__)


def get_profile(url_or_public_id: str) -> Profile:
    if not is_valid_url(url_or_public_id) and not is_valid_linkedin_personal_public_id:
        raise InvalidPersonalPublicID(url_or_public_id)
    if is_valid_url(url_or_public_id) and not url_or_public_id.startswith(
        LinkedinURLHelper.PROFILE_LINK_PREFIX
    ):
        raise InvalidPersonalProfileURL(url_or_public_id)

    is_public_id = not url_or_public_id.startswith(
        LinkedinURLHelper.PROFILE_LINK_PREFIX
    )
    if not is_public_id:
        url = url_or_public_id
    else:
        url = LinkedinURLHelper.PROFILE_LINK_PREFIX + url_or_public_id
    driver = generate_driver()
    soup = soup_from_js_site(url, driver)

    try:
        name = clean_whitespace(soup.find(class_="top-card-layout__title").get_text())
        if not name:
            raise (
                InvalidPersonalPublicID if is_public_id else InvalidPersonalProfileURL
            )(url_or_public_id)

        return Profile(
            **compact(
                {
                    "name": name,
                    "profile_image_url": soup.find("img", attrs={"alt": name})["src"],
                    "linkedin_url": url.strip(),
                    "headline": clean_whitespace(
                        _(soup.find(class_="top-card-layout__headline")).get_text()
                    ),
                    "about": (
                        None
                        if clean_whitespace(
                            _(
                                soup.find(class_="core-section-container__title")
                            ).get_text()
                        )
                        != "About"
                        else HTML2TEXT.handle(
                            str(soup.find(class_="core-section-container__content"))
                        ).strip()
                    ),
                    "experience": _extract_experience(
                        _(soup.find(class_="experience__list"))
                    ),
                    "education": _extract_education(
                        _(soup.find(class_="education__list")).find_all("li")
                    ),
                }
            )
        )
    except Exception:
        driver.quit()
        raise


def _extract_experience(
    experience_soups: Optional[List[BeautifulSoup]],
) -> Optional[List[Experience]]:
    if not experience_soups:
        return None

    experience = []

    for experience_soup in nullreplace(
        experience_soups.find_all("li", class_="profile-section-card experience-item"),
        [],
    ):
        exdata = {
            "title": clean_whitespace(
                experience_soup.find(class_="profile-section-card__title").get_text()
            ),
            "company_name": clean_whitespace(
                experience_soup.find(class_="profile-section-card__subtitle").get_text()
            ),
            "location": clean_whitespace(
                _(experience_soup.find(class_="experience-item__location")).get_text()
            ),
            "company_url": LinkedinURLHelper.clean_company_url(
                _(experience_soup.find("a")).get("href")
            ),
            "duration": clean_whitespace(
                _(experience_soup.find(class_="date-range__duration")).get_text()
            ),
            "start_date": clean_whitespace(
                experience_soup.find(class_="experience-item__duration")
                .find("time")
                .get_text()
            ),
            "end_date": clean_whitespace(
                "Present"
                if "Present"
                in nullreplace(
                    _(
                        experience_soup.find(class_="experience-item__duration")
                    ).get_text(),
                    "",
                )
                else _(experience_soup.find(class_="experience-item__duration"))
                .find_all("time")[1]
                .get_text()
            ),
            "description": (
                None
                if experience_soup.find(class_="show-more-less-text__text--less")
                is None
                else HTML2TEXT.handle(
                    str(experience_soup.find(class_="show-more-less-text__text--more"))
                    if experience_soup.find(class_="show-more-less-text__text--more")
                    else str(
                        experience_soup.find(class_="show-more-less-text__text--less")
                    )
                ).strip()
            ),
        }
        experience.append(Experience(**compact(exdata)))

    # In case the person has multiple positiions under one company,
    # the html will be quite different than a stand-alone position.
    for experience_soup in nullreplace(
        experience_soups.find_all("li", class_="experience-group experience-item"), []
    ):
        for exp_under_company_soup in experience_soup.find_all(
            class_="experience-group__positions"
        ):
            company = clean_whitespace(
                experience_soup.find(
                    class_="experience-group-header__company"
                ).get_text()
            )
            company_url = LinkedinURLHelper.clean_company_url(
                _(experience_soup.find("a")).get("href")
            )

            for position_soup in exp_under_company_soup.find_all(
                "li", class_="profile-section-card experience-group-position"
            ):
                position_data = {
                    "company_name": company,
                    "company_url": company_url,
                    "title": clean_whitespace(
                        position_soup.find(
                            class_="profile-section-card__title"
                        ).get_text()
                    ),
                    "location": clean_whitespace(
                        _(
                            position_soup.find(
                                class_="experience-group-position__location"
                            )
                        ).get_text()
                    ),
                    "duration": clean_whitespace(
                        _(
                            experience_soup.find(class_="date-range__duration")
                        ).get_text()
                    ),
                    "start_date": clean_whitespace(
                        position_soup.find(class_="experience-group-position__duration")
                        .find("time")
                        .get_text()
                    ),
                    "end_date": clean_whitespace(
                        "Present"
                        if "Present"
                        in nullreplace(
                            _(
                                experience_soup.find(
                                    class_="experience-group-position__duration"
                                )
                            ).get_text(),
                            "",
                        )
                        else _(
                            experience_soup.find(
                                class_="experience-group-position__duration"
                            )
                        )
                        .find_all("time")[1]
                        .get_text()
                    ),
                    "description": (
                        None
                        if position_soup.find(class_="show-more-less-text__text--less")
                        is None
                        else HTML2TEXT.handle(
                            str(
                                position_soup.find(
                                    class_="show-more-less-text__text--more"
                                )
                            )
                            if position_soup.find(
                                class_="show-more-less-text__text--more"
                            )
                            else str(
                                position_soup.find(
                                    class_="show-more-less-text__text--less"
                                )
                            )
                        ).strip()
                    ),
                }
                experience.append(Experience(**compact(position_data)))

    return experience


def _extract_education(education_soups) -> Optional[List[Education]]:
    if not education_soups:
        return None

    education = []
    for edsoup in education_soups:
        ed_items_soups = _(
            edsoup.find(class_="profile-section-card__subtitle")
        ).find_all("span")
        education_data = {
            "school": clean_whitespace(
                edsoup.find(class_="profile-section-card__title").get_text()
            ),
            "school_url": LinkedinURLHelper.clean_school_url(
                _(edsoup.find("a")).get("href")
            ),
            "degree": (
                None
                if not ed_items_soups
                else clean_whitespace(ed_items_soups[0].get_text())
            ),
            "major": (
                None
                if not ed_items_soups or len(ed_items_soups) < 2
                else clean_whitespace(ed_items_soups[1].get_text())
            ),
            "grade": (
                None
                if not ed_items_soups or len(ed_items_soups) < 3
                else clean_whitespace(ed_items_soups[2].get_text())
            ),
        }
        education.append(Education(**compact(education_data)))

    return education
