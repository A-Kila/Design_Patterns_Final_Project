from dataclasses import dataclass

from app.core.users.users_interactor import IUserRepository, UsersInteractor
from app.core.wallets.wallet_generator import (
    WalletGetRequest,
    WalletGetResponse,
    WalletPostRequest,
    WalletPostResponse,
)
from app.core.wallets.wallets_interactor import IWalletRepository, WalletsInteractor
from app.infra.rateapi.coingecko import CoinGeckoApi


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

    def get_wallet(self, request: WalletGetRequest) -> WalletGetResponse:
        return self.wallet_interactor.get_wallet(request)

    def create_wallet(self, request: WalletPostRequest) -> WalletPostResponse:
        return self.wallet_interactor.create_wallet(request=request)

    @classmethod
    def create(
        cls, user_repo: IUserRepository, wallet_repo: IWalletRepository
    ) -> "WalletService":
        return cls(
            UsersInteractor(user_repo), WalletsInteractor(wallet_repo, CoinGeckoApi())
        )
