import os
from typing import List


class OSEnvKeys:
    """
    Containing the names of the OS environment keys
    """

    LINKEDIN_ACCOUNT = "LINKEDIN_ACCOUNT"
    LINKEDIN_PASSWORD = "LINKEDIN_PASSWORD"

    @classmethod
    def to_a(cls) -> List[str]:
        """Return a list of the OS environment keys"""
        condition = lambda x: not callable(getattr(cls, x)) and not x.startswith("__")
        return [getattr(cls, attr) for attr in dir(cls) if condition(attr)]


for os_env_key in OSEnvKeys.to_a():
    globals()[os_env_key] = os.environ.get(os_env_key)
