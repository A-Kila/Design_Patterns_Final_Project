from dataclasses import dataclass, field

from app.core.interfaces.users_interface import IUserGenerator, IUserRepository
from app.core.users.user_generator import UserGenerator


@dataclass
class UsersInteractor:
    user_repo: IUserRepository
    user_generator: IUserGenerator = field(default_factory=UserGenerator)

    def generate_new_api_key(self) -> UsersResponse:
        user = self.user_generator.generate_new_user()
        self.user_repo.store_user(user.api_key)

        return UsersResponse(user.api_key)
