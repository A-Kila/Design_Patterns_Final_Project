from dataclasses import dataclass, field

from app.core.interfaces.transitions_interface import ITransactionRepository
from app.core.interfaces.users_interface import IUserRepository
from app.core.interfaces.wallets_interface import IWalletRepository
from app.core.transactions.tax_calculator import (
    DifferentUserTax,
    FreeTax,
    TaxCalculator,
)


@dataclass
class TransactionInteractor:
    wallet_repo: IWalletRepository
    transaction_repo: ITransactionRepository
    user_repo: IUserRepository
    tax_calculator: TaxCalculator = field(default_factory=TaxCalculator)

    def make_transaction(
        self, api_key: str, wallet_from: str, wallet_to: str, amount: float
    ) -> bool:
        user_id = self.user_repo.get_user_id(api_key)

        if not self.wallet_repo.is_my_wallet(
            user_id, wallet_from
        ) or not self.wallet_repo.wallet_exists(wallet_to):
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
