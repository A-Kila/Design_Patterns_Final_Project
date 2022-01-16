from dataclasses import dataclass, field

from app.core.interfaces.transitions_interface import (
    ITransactionRepository,
    Transaction,
)
from app.core.interfaces.users_interface import IUserRepository
from app.core.interfaces.wallets_interface import IWalletRepository
from app.core.transactions.tax_calculator import (
    DifferentUserTax,
    FreeTax,
    TaxCalculator,
)


@dataclass
class CreateTransactionRequest:
    api_key: str
    wallet_from: str
    wallet_to: str
    amount: float


@dataclass
class WalletTransactionsRequest:
    api_key: str
    wallet_address: str


@dataclass
class GetUserTransactionsRequest:
    api_key: str


@dataclass
class GetTransactionsResponse:
    transactions: list[Transaction]


@dataclass
class TransactionInteractor:
    wallet_repo: IWalletRepository
    transaction_repo: ITransactionRepository
    user_repo: IUserRepository
    tax_calculator: TaxCalculator = field(default_factory=TaxCalculator)

    def get_transactions(
        self, request: GetUserTransactionsRequest
    ) -> GetTransactionsResponse:
        user_id = self.user_repo.get_user_id(request.api_key)

        return GetTransactionsResponse(self.transaction_repo.get_transactions(user_id))

    def make_transaction(self, request: CreateTransactionRequest) -> None:
        user_id = self.user_repo.get_user_id(request.api_key)

        if not self.wallet_repo.wallet_exists(
            request.wallet_from
        ) or not self.wallet_repo.wallet_exists(request.wallet_to):
            raise Exception("One of the wallets you passed does not exist")

        if not self.wallet_repo.is_my_wallet(user_id, request.wallet_from):
            raise Exception("The user does not have permission to transfer from wallet")

        if self.wallet_repo.get_balance(request.wallet_from) < request.amount:
            raise Exception("Not enough money on wallet")

        self.__transfer_money(user_id, request)

    def __transfer_money(self, user_id: int, request: CreateTransactionRequest) -> None:
        if self.wallet_repo.is_my_wallet(user_id, request.wallet_to):
            self.tax_calculator.tax = FreeTax()
        else:
            self.tax_calculator.tax = DifferentUserTax()

        tax = self.tax_calculator.get_tax(request.amount)
        amount_transfered = self.tax_calculator.get_money_transfered(request.amount)

        self.transaction_repo.store_transaction(
            user_id, request.wallet_from, request.wallet_to, amount_transfered, tax
        )

    def get_wallet_transactions(
        self, request: WalletTransactionsRequest
    ) -> GetTransactionsResponse:
        wallet_address: str = request.wallet_address

        if not self.wallet_repo.wallet_exists(wallet_address=wallet_address):
            raise Exception("Wallet do not exists")

        transactions = self.transaction_repo.get_wallet_transactions(
            wallet_address=wallet_address
        )

        return GetTransactionsResponse(transactions=transactions)
