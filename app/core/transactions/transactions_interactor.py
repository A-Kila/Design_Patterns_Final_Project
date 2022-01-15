from dataclasses import dataclass, field
from typing import Protocol, List

from app.core.facade import IGetUserRepository
from app.core.transactions.tax_calculator import (
    DifferentUserTax,
    FreeTax,
    TaxCalculator,
)
from app.infra.in_memory.transactions_repository import Transaction, Statistics


class IWalletRepository(Protocol):
    def make_transaction(self, from_wallet: str, to_wallet: str, amount: float) -> None:
        pass

    def does_wallet_exist(self, wallet: str) -> bool:
        pass

    def is_my_wallet(self, user_id: int, wallet_address: str) -> bool:
        pass


class ITransactionRepository(Protocol):
    def store_transaction(
        self, user_id: int, from_wallet: str, to_wallet: str, amount: float, profit: float
    ) -> None:
        pass

    def get_transactions(self, user_id) -> List[Transaction]:
        pass

    def get_wallet_transations(self, wallet_address: str) -> List[Transaction]:
        pass

    def get_statistics(self) -> Statistics:
        pass

@dataclass
class TransactionInteractor:
    wallet_repo: IWalletRepository
    transaction_repo: ITransactionRepository
    user_repo: IGetUserRepository
    tax_calculator: TaxCalculator = field(default_factory=TaxCalculator)

    def make_transaction(
        self, api_key: str, wallet_from: str, wallet_to: str, amount: float
    ) -> bool:
        user_id = self.user_repo.get_user_id(api_key)

        if not self.wallet_repo.is_my_wallet(
            user_id, wallet_from
        ) or not self.wallet_repo.does_wallet_exist(wallet_to):
            return False

        if self.wallet_repo.is_my_wallet(user_id, wallet_to):
            self.tax_calculator.tax = FreeTax()
        else:
            self.tax_calculator.tax = DifferentUserTax()

        tax = self.tax_calculator.get_tax(amount)
        amount_transfered = self.tax_calculator.get_money_transfered(amount)

        self.transaction_repo.store_transaction(
            user_id, wallet_from, wallet_to, amount_transfered, tax
        )

        return True
