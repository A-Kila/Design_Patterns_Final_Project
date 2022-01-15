from dataclasses import dataclass, field
from typing import Protocol, List

from app.core.facade import IGetUserRepository
from app.core.transactions.tax_calculator import (
    DifferentUserTax,
    FreeTax,
    TaxCalculator,
)
from app.infra.in_memory.transactions_repository import Transaction, Statistics

SUCCESS_CODE = 200
PERMISSION_DENIED = 400
WALLET_DOES_NOT_EXIST = 404


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


class IWalletRepository(Protocol):
    def make_transaction(self, from_wallet: str, to_wallet: str, amount: float) -> None:
        pass

    def does_wallet_exist(self, wallet: str) -> bool:
        pass

    def is_my_wallet(self, user_id: int, wallet_address: str) -> bool:
        pass


class ITransactionRepository(Protocol):
    def store_transaction(
        self,
        user_id: int,
        from_wallet: str,
        to_wallet: str,
        amount: float,
        profit: float,
    ) -> None:
        pass

@dataclass
class TransactionInteractor:
    wallet_repo: IWalletRepository
    transaction_repo: ITransactionRepository
    user_repo: IGetUserRepository
    tax_calculator: TaxCalculator = field(default_factory=TaxCalculator)

    def make_transaction(self, request: TransactionRequest) -> TransactionResponse:
        user_id = self.user_repo.get_user_id(request.api_key)

        if self.wallet_repo.does_wallet_exist(
            request.wallet_from
        ) or not self.wallet_repo.does_wallet_exist(request.wallet_to):
            return TransactionResponse(
                status_code=WALLET_DOES_NOT_EXIST,
                msg="One of the wallets you passed does not exist",
            )

        if not self.wallet_repo.is_my_wallet(user_id, request.wallet_from):
            return TransactionResponse(
                status_code=PERMISSION_DENIED,
                msg="The wallet you are depositing from does not exist",
            )

        if self.wallet_repo.is_my_wallet(user_id, request.wallet_to):
            self.tax_calculator.tax = FreeTax()
        else:
            self.tax_calculator.tax = DifferentUserTax()

        tax = self.tax_calculator.get_tax(request.amount)
        amount_transfered = self.tax_calculator.get_money_transfered(request.amount)

        self.transaction_repo.store_transaction(
            user_id, request.wallet_from, request.wallet_to, amount_transfered, tax
        )

        return TransactionResponse(SUCCESS_CODE, "")
