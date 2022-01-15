from dataclasses import dataclass
from typing import Optional, Protocol

from app.core.transactions.transactions_interactor import (
    ITransactionRepository,
    IWalletRepository,
    TransactionInteractor,
)
from app.core.users.users_interactor import IUserRepository, UsersInteractor


@dataclass
class UsersResponse:
    api_key: str


@dataclass
class TransactionRequest:
    api_key: str
    wallet_from: str
    wallet_to: str
    amount: float


@dataclass
class TransactionResponse:
    status_code: int
    msg: str


class IGetUserRepository(Protocol):
    def get_user_id(self, api_key: str) -> Optional[int]:
        pass


@dataclass
class WalletService:
    user_interactor: UsersInteractor
    transaction_interactor: TransactionInteractor

    def register_user(self) -> UsersResponse:
        api_key = self.user_interactor.generate_new_api_key()

        return UsersResponse(api_key)

    def make_transaction(self, request: TransactionRequest) -> TransactionResponse:
        if self.transaction_interactor.make_transaction(
            request.api_key, request.wallet_from, request.wallet_to, request.amount
        ):
            return TransactionResponse(200, "")

        return TransactionResponse(
            400,
            "Wallet does not exist or the user does not have permission to acces it",
        )

    @classmethod
    def create(
        cls,
        user_repo: IUserRepository,
        wallet_repo: IWalletRepository,
        transaction_repo: ITransactionRepository,
    ) -> "WalletService":
        return cls(
            UsersInteractor(user_repo),
            TransactionInteractor(wallet_repo, transaction_repo, user_repo),
        )
