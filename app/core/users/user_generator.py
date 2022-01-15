from dataclasses import dataclass
from secrets import token_urlsafe


API_KEY_LENGHT = 32


@dataclass
class User:
    api_key: str


class UserGenerator:
    def __init__(self) -> None:
        self.api_key_length = API_KEY_LENGHT

    def generate_new_user(self) -> User:
        api_key = token_urlsafe(self.api_key_length)

        return User(api_key)
