from dataclasses import dataclass, field

from app.core.interfaces.transitions_interface import Statistics, Transaction


@dataclass
class TransactionRepositoryInMemory:
    total_transactions: int = 0
    repo: list[Transaction] = field(default_factory=list[Transaction])

    def store_transaction(
        self,
        user_id: int,
        from_wallet: str,
        to_wallet: str,
        amount: float,
        profit: float,
    ) -> None:
        self.repo.append(
            Transaction(
                user_id=user_id,
                from_wallet=from_wallet,
                to_wallet=to_wallet,
                amount=amount,
                profit=profit,
            )
        )
        self.total_transactions += 1

    def get_transactions(self, user_id: int) -> list[Transaction]:
        trans_for_user: list[Transaction] = []
        for transaction in self.repo:
            if transaction.user_id == user_id:
                trans_for_user.append(transaction)
        return trans_for_user

    def get_wallet_transactions(self, wallet_address: str) -> list[Transaction]:
        trans_for_wallet: list[Transaction] = []
        for transaction in self.repo:
            if (
                transaction.to_wallet == wallet_address
                or transaction.from_wallet == wallet_address
            ):
                trans_for_wallet.append(transaction)
        return trans_for_wallet

    def get_statistics(self) -> Statistics:
        stat = Statistics(self.total_transactions, total_profit=0.0)
        for transaction in self.repo:
            stat.total_profit += transaction.profit
        return stat
