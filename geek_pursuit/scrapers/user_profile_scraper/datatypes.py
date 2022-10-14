from dataclasses import asdict
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import List


@dataclass
class Experience:
    title: str
    company_name: str
    start_date: str
    end_date: str = None
    duration: str = None
    location: str = None
    company_url: str = None
    description: str = None

    def to_json(self) -> Dict[str, str]:
        return {k: str(v) for k, v in asdict(self).items()}


@dataclass
class Education:
    school: str
    school_url: str = None
    degree: str = None
    major: str = None
    grade: str = None


@dataclass
class Profile:
    name: str
    headline: str = None
    about: str = None
    experience: List[Experience] = None
    education: List[Education] = None

    def to_json(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            "experience": [asdict(ex) for ex in self.experience],
            "education": [asdict(ed) for ed in self.education],
        }
