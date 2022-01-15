from dataclasses import field, dataclass

# user_id_from, user_id_to, wallet_from, wallet_to, amount, profit
from typing import List


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


@dataclass
class TransactionRepositoryInMemory:
    total_transactions: int
    repo: List[Transaction] = field(default_factory=List[Transaction])

    def store_transaction(
            self, user_id, from_wallet: str, to_wallet: str, amount: float, profit: float
    ) -> None:
        self.repo.append(Transaction(
            user_id=user_id,
            from_wallet=from_wallet,
            to_wallet=to_wallet,
            amount=amount,
            profit=profit))
        self.total_transactions += 1

    def get_transactions(self, user_id) -> List[Transaction]:
        trans_for_user: List[Transaction] = []
        for transaction in self.repo:
            if transaction.user_id == user_id:
                trans_for_user.append(transaction)
        return trans_for_user

    def get_wallet_transations(self, wallet_address: str) -> List[Transaction]:
        trans_for_wallet: List[Transaction] = []
        for transaction in self.repo:
            if transaction.to_wallet == wallet_address or transaction.from_wallet == wallet_address:
                trans_for_wallet.append(transaction)
        return trans_for_wallet

    def get_statistics(self) -> Statistics:
        stat = Statistics(total_transactions=self.transactions, total_profit=0.0)
        for transaction in self.repo:
            stat.total_profit += transaction.profit
