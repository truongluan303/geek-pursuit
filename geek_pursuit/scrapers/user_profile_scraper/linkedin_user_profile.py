import html2text
from nullsafe import _

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
from geek_pursuit.utils.validator import is_valid_personal_public_id
from geek_pursuit.utils.validator import is_valid_url


HTML2TEXT: html2text.HTML2Text = html2text.HTML2Text()
HTML2TEXT.body_width = 0


def get_profile(url_or_public_id: str) -> dict:
    if not is_valid_url(url_or_public_id) and not is_valid_personal_public_id:
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
    soup = soup_from_js_site(url)

    if not soup.find(class_="top-card-layout__title"):
        raise (InvalidPersonalPublicID if is_public_id else InvalidPersonalProfileURL)(
            url_or_public_id
        )

    experience_soups = _(soup.find(class_="experience__list")).find_all("li")
    if experience_soups:
        experience = [
            Experience(
                **compact(
                    {
                        "title": clean_whitespace(
                            exsoup.find(class_="profile-section-card__title").get_text()
                        ),
                        "company_name": clean_whitespace(
                            exsoup.find(
                                class_="profile-section-card__subtitle"
                            ).get_text()
                        ),
                        "location": clean_whitespace(
                            _(
                                exsoup.find(class_="experience-item__location")
                            ).get_text()
                        ),
                        "company_url": LinkedinURLHelper.clean_company_url(
                            _(exsoup.find("a")).get("href")
                        ),
                        "duration": clean_whitespace(
                            _(exsoup.find(class_="date-range__duration")).get_text()
                        ),
                        "start_date": clean_whitespace(
                            exsoup.find(class_="experience-item__duration")
                            .find("time")
                            .get_text()
                        ),
                        "end_date": clean_whitespace(
                            "Present"
                            if "Present"
                            in _(
                                exsoup.find(class_="experience-item__duration")
                            ).get_text()
                            else _(exsoup.find(class_="experience-item__duration"))
                            .find_all("time")[1]
                            .get_text()
                        ),
                        "description": (
                            None
                            if exsoup.find(class_="show-more-less-text__text--more")
                            is None
                            else HTML2TEXT.handle(
                                str(
                                    exsoup.find(
                                        class_="show-more-less-text__text--more"
                                    )
                                )
                            )
                        ),
                    }
                )
            )
            for exsoup in experience_soups
        ]
    else:
        experience = None

    education_soups = _(soup.find(class_="education__list")).find_all("li")
    if education_soups:
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
    else:
        education = None

    return Profile(
        **{
            "name": clean_whitespace(
                soup.find(class_="top-card-layout__title").get_text()
            ),
            "headline": clean_whitespace(
                _(soup.find(class_="top-card-layout__headline")).get_text()
            ),
            "about": HTML2TEXT.handle(
                str(_(soup.find(class_="core-section-container__content")))
            ),
            "experience": experience,
            "education": education,
        }
    )
