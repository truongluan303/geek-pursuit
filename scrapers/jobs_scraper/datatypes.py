from dataclasses import dataclass
from datetime import timedelta


@dataclass
class JobInfo:
    title: str = None
    company: str = None
    description: str = None
    location: str = None
    posted_time_ago: timedelta = None
    summary: str = None
    company_pic_url: str = None
    url: str = None


@dataclass
class HtmlKeys:
    title_key: str
    company_key: str
    company_pic_key: str
    img_src_key: str
    time_ago_key: str
    description_key: str
    location_key: str
