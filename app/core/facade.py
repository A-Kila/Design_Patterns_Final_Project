from dataclasses import dataclass

from app.core.interfaces.users_interface import IUserRepository
from app.core.transactions.transactions_interactor import (
    ITransactionRepository,
    IWalletRepository,
    TransactionInteractor,
    TransactionRequest,
    TransactionResponse,
)
from app.core.users.users_interactor import UsersInteractor, UsersResponse


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
