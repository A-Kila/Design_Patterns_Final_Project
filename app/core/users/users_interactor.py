from dataclasses import dataclass, field
from typing import Protocol

from app.core.users.user_generator import User, UserGenerator


@dataclass
class UsersResponse:
    api_key: str


class IUserGenerator(Protocol):
    def generate_new_user(self) -> User:
        pass


class IUserRepository(Protocol):
    def store_user(self, api_key: str) -> None:
        pass

    def get_user_id(self, api_key: str) -> int:
        pass


@dataclass
class UsersInteractor:
    user_repo: IUserRepository
    user_generator: IUserGenerator = field(default_factory=UserGenerator)

    def generate_new_api_key(self) -> UsersResponse:
        user = self.user_generator.generate_new_user()
        self.user_repo.store_user(user.api_key)

        return UsersResponse(user.api_key)
