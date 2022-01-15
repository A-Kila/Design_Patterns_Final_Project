from typing import Optional, Protocol

from app.core.users.user_generator import User


class IUserGenerator(Protocol):
    def generate_new_user(self) -> User:
        pass


class IUserRepository(Protocol):
    def store_user(self, api_key: str) -> None:
        pass

    def get_user_id(self, api_key: str) -> Optional[int]:
        pass
