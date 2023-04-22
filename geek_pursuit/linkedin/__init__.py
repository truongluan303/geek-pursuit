from linkedin_api import Linkedin

from config import LINKEDIN_ACCOUNT
from config import LINKEDIN_PASSWORD

linkedin_api_instance = Linkedin(LINKEDIN_ACCOUNT, LINKEDIN_PASSWORD)

__all__ = ["linkedin"]
