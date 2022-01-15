from dataclasses import dataclass, field
from typing import Protocol

from app.core.users.user_generator import User, UserGenerator


class IUserGenerator(Protocol):
    def generate_new_user(self) -> User:
        pass


class IUserRepository(Protocol):
    def store_user(self, api_key: str) -> None:
        pass


@dataclass
class UsersInteractor:
    user_repo: IUserRepository
    user_generator: IUserGenerator = field(default_factory=UserGenerator)

    def generate_new_api_key(self) -> str:
        user = self.user_generator.generate_new_user()
        self.user_repo.store_user(user.api_key)

        return str(user.api_key)
