from dataclasses import dataclass
from typing import Optional, Protocol

from app.core.transactions.transactions_interactor import (
    ITransactionRepository,
    IWalletRepository,
    TransactionInteractor,
    TransactionRequest,
    TransactionResponse,
)
from app.core.users.users_interactor import (
    IUserRepository,
    UsersInteractor,
    UsersResponse,
)
from app.core.wallets.wallets_interactor import (
    IWalletRepository,
    WalletGetRequest,
    WalletPostRequest,
    WalletResponse,
    WalletsInteractor,
)
from app.infra.rateapi.coingecko import CoinGeckoApi


@dataclass
class UsersResponse:
    api_key: str


class IGetUserRepository(Protocol):
    def get_user_id(self, api_key: str) -> Optional[int]:
        pass


@dataclass
class WalletService:
    user_interactor: UsersInteractor
    wallet_interactor: WalletsInteractor
    transaction_interactor: TransactionInteractor

    def register_user(self) -> UsersResponse:
        return self.user_interactor.generate_new_api_key()

    def make_transaction(self, request: TransactionRequest) -> TransactionResponse:
        return self.transaction_interactor.make_transaction(request)

    def get_wallet(self, request: WalletGetRequest) -> WalletResponse:
        return self.wallet_interactor.get_wallet(request)

    def create_wallet(self, request: WalletPostRequest) -> WalletResponse:
        return self.wallet_interactor.create_wallet(request=request)

    @classmethod
    def create(
        cls,
        user_repo: IUserRepository,
        wallet_repo: IWalletRepository,
        transaction_repo: ITransactionRepository,
    ) -> "WalletService":
        return cls(
            UsersInteractor(user_repo),
            WalletsInteractor(wallet_repo, CoinGeckoApi()),
            TransactionInteractor(wallet_repo, transaction_repo, user_repo),
        )
