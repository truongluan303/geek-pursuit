class LinkedinURLHelper:
    COMPANY_LINK_PREFIX = "https://www.linkedin.com/company/"
    SCHOOL_LINK_PREFIX = "https://www.linkedin.com/school/"
    PROFILE_LINK_PREFIX = "https://www.linkedin.com/in/"

    @staticmethod
    def clean_company_url(url: str) -> str:
        return LinkedinURLHelper._generic_clean(
            url, LinkedinURLHelper.COMPANY_LINK_PREFIX
        )

    @staticmethod
    def clean_profile_url(url: str) -> str:
        return LinkedinURLHelper._generic_clean(
            url, LinkedinURLHelper.PROFILE_LINK_PREFIX
        )

    @staticmethod
    def clean_school_url(url: str) -> str:
        return LinkedinURLHelper._generic_clean(
            url, LinkedinURLHelper.SCHOOL_LINK_PREFIX
        )

    def _generic_clean(url: str, prefix: str) -> str:
        if not url:
            return url
        return prefix + (url.replace(prefix, "").split("?")[0].split("/")[0])
