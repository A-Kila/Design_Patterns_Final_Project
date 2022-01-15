from dataclasses import dataclass
from typing import Protocol


@dataclass
class Transaction:
    user_id: int
    from_wallet: str
    to_wallet: str
    amount: float
    profit: float


@dataclass
class Statistics:
    total_transactions: int
    total_profit: float


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

    def get_transactions(self, user_id: int) -> list[Transaction]:
        pass

    def get_wallet_transactions(self, wallet_address: str) -> list[Transaction]:
        pass

    def get_statistics(self) -> Statistics:
        pass
