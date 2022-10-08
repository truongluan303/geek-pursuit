from http.client import InvalidURL


class InvalidPersonalProfileURL(InvalidURL):
    def __init__(
        self, url: str, message: str = "Invalid personal profile URL."
    ) -> None:
        self._url = url
        super().__init__(message)

    @property
    def url(self) -> str:
        return self._url


class InvalidPersonalPublicID(Exception):
    def __init__(
        self,
        public_id: str,
        message: str = (
            "Public ID must contain 3-100 letters or numbers "
            "and no spaces, symbols, or special characters."
        ),
    ) -> None:
        self._public_id = public_id
        super().__init__(message)

    @property
    def public_id(self):
        return self._public_id
