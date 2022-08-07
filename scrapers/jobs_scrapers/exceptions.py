from http.client import InvalidURL


class InvalidJobURL(InvalidURL):
    def __init__(self, url: str, message: str = "Invalid LinkedIn job URL") -> None:
        self._url = url
        super().__init__(message)

    @property
    def url(self) -> str:
        return self._url
