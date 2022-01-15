from dataclasses import dataclass
from typing import Optional, Protocol

from app.core.transactions.transactions_interactor import (
    ITransactionRepository,
    IWalletRepository,
    TransactionInteractor,
    TransactionRequest,
    TransactionResponse,
)
from app.core.users.users_interactor import IUserRepository, UsersInteractor, UsersResponse


class IGetUserRepository(Protocol):
    def get_user_id(self, api_key: str) -> Optional[int]:
        pass


@dataclass
class WalletService:
    user_interactor: UsersInteractor
    transaction_interactor: TransactionInteractor

    def register_user(self) -> UsersResponse:
        return self.user_interactor.generate_new_api_key()

    def make_transaction(self, request: TransactionRequest) -> TransactionResponse:
        return self.transaction_interactor.make_transaction(request)

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
