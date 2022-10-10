def clean_whitespace(s: str) -> str:
    return s if not s else " ".join(s.strip().split())
