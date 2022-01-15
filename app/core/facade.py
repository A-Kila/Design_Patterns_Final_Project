from dataclasses import dataclass

from app.core.users.users_interactor import IUserRepository, UsersInteractor
from app.core.wallets.wallet_generator import WalletPostRequest, WalletPostResponse
from app.core.wallets.wallets_interactor import IWalletRepository, WalletsInteractor


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

    def create_wallet(self, request: WalletPostRequest) -> WalletPostResponse:
        api_key: str = request.api_key
        return self.wallet_interactor.create_wallet(api_key=api_key)

    @classmethod
    def create(
        cls, user_repo: IUserRepository, wallet_repo: IWalletRepository
    ) -> "WalletService":
        return cls(UsersInteractor(user_repo), WalletsInteractor(wallet_repo))
