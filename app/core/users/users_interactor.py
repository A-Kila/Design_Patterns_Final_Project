from dataclasses import dataclass

from app.core.users.user_generator import User


class IUserGenerator:
    def generate_new_user(self) -> User:
        pass


class IUserRepository:
    def store_user(self, user: str, api_key: str) -> None:
        pass


@dataclass
class UsersInteractor:
    user_repo: IUserRepository
    user_generator: IUserGenerator

    def generate_new_api_key(self) -> str:
        user = self.user_generator.generate_new_user()
        self.user_repo.store_user(user.user_id, user.api_key)

        return str(user.api_key)
