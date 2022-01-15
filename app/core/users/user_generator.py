from dataclasses import dataclass
from secrets import token_urlsafe


API_KEY_LENGHT = 32


@dataclass
class User:
    user_id: str
    api_key: str


class UserGenerator:
    def __init__(self) -> None:
        self.user_id_int = 0
        self.api_key_length = API_KEY_LENGHT

    def generate_new_user(self) -> User:
        api_key = token_urlsafe(self.api_key_length)
        user = User(str(self.user_id_int), api_key)

        self.user_id_int += 1

        return user
