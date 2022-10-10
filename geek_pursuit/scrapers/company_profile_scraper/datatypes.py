from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import fields
from typing import Any
from typing import Dict
from typing import List

from geek_pursuit.utils.string_utils import clean_whitespace


@dataclass
class CompanyInfo:
    name: str
    linkedin_url: str = None
    industry: str = None
    logo: str = None
    head_quarters_locations: List[str] = None
    all_locations: List[str] = None
    number_of_employees: int = None
    website: str = None
    founded_time: str = None
    company_type: str = None
    specialties: str = None
    slogan: str = None
    description: str = None
    number_of_linkedin_followers: int = None
    opened_jobs: List[str] = None

    def __post_init__(self) -> None:
        for field in fields(self):
            val = getattr(self, field.name)
            if val is None:
                continue

            if field.type is int:
                setattr(self, field.name, int(val))
            elif field.type is str:
                setattr(self, field.name, clean_whitespace(str(val)))

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
