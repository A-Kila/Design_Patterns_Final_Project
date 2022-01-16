from dataclasses import dataclass

from app.core.interfaces.transitions_interface import ITransactionRepository
from app.core.interfaces.users_interface import IUserRepository
from app.core.interfaces.wallets_interface import IWalletRepository
from app.core.transactions.transactions_interactor import (
    CreateTransactionRequest,
    GetTransactionsResponse,
    GetUserTransactionsRequest,
    TransactionInteractor,
)
from app.core.users.users_interactor import UsersInteractor, UsersResponse
from app.core.wallets.wallets_interactor import (
    WalletGetRequest,
    WalletPostRequest,
    WalletResponse,
    WalletsInteractor,
)
from app.infra.rateapi.coingecko import CoinGeckoApi


@dataclass
class WalletService:
    user_interactor: UsersInteractor
    wallet_interactor: WalletsInteractor
    transaction_interactor: TransactionInteractor

    def register_user(self) -> UsersResponse:
        return self.user_interactor.generate_new_api_key()

    def make_transaction(self, request: CreateTransactionRequest) -> None:
        self.transaction_interactor.make_transaction(request)

    def get_wallet(self, request: WalletGetRequest) -> WalletResponse:
        return self.wallet_interactor.get_wallet(request)

    def create_wallet(self, request: WalletPostRequest) -> WalletResponse:
        return self.wallet_interactor.create_wallet(request=request)

    def get_transactions(
        self, request: GetUserTransactionsRequest
    ) -> GetTransactionsResponse:
        return self.transaction_interactor.get_transactions(request)

    @classmethod
    def create(
        cls,
        user_repo: IUserRepository,
        wallet_repo: IWalletRepository,
        transaction_repo: ITransactionRepository,
    ) -> "WalletService":
        return cls(
            UsersInteractor(user_repo),
            WalletsInteractor(
                user_repo=user_repo,
                wallet_repo=wallet_repo,
                rate_getter=CoinGeckoApi(),
            ),
            TransactionInteractor(wallet_repo, transaction_repo, user_repo),
        )
