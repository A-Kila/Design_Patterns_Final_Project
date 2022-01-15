from dataclasses import dataclass

from app.core.users.users_interactor import UsersInteractor


@dataclass
class UsersResponse:
    api_key: str


@dataclass
class WalletService:
    user_interactor: UsersInteractor

    def register_user(self) -> UsersResponse:
        api_key = self.user_interactor.generate_new_api_key()

        return UsersResponse(api_key)
