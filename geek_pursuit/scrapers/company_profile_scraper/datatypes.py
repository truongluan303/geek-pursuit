from dataclasses import dataclass
from typing import List


@dataclass
class CompanyInfo:
    name: str = None
    industry: str = None
    head_quarter_location: str = None
    all_locations: List[str] = None
    number_of_employees: int = None
    website: str = None
    founded_year: int = None
    type: str = None
    specialties: str = None
    description: str = None
    number_of_linkedin_followers: int = None
    opened_jobs: List[str] = None


@dataclass
class CompanyHtmlKeys:
    name_key: str
    industry_key: str
    head_quarter_location_key: str
    all_locations_key: str
    number_of_employees_key: str
    website_key: str
    founded_year_key: str
    type_key: str
    specialties_key: str
    description_key: str
    number_of_linkedin_followers_key: str
    opened_jobs_key: str
