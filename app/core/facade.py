from dataclasses import dataclass

from app.core.users.users_interactor import IUserRepository, UsersInteractor
from app.core.wallets.wallets_interactor import WalletsInteractor


@dataclass
class UsersResponse:
    api_key: str


@dataclass
class WalletService:
    user_interactor: UsersInteractor
    wallet_interactor: WalletsInteractor

    def register_user(self) -> UsersResponse:
        api_key = self.user_interactor.generate_new_api_key()

        return UsersResponse(api_key)

    @classmethod
    def create(cls, user_repo: IUserRepository) -> "WalletService":
        return cls(UsersInteractor(user_repo), WalletsInteractor())
