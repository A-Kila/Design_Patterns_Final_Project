import pytest

from app.core.interfaces.transitions_interface import ITransactionRepository
from app.infra.in_memory.transactions_repository import TransactionRepositoryInMemory


@pytest.fixture()
def transaction_repo() -> ITransactionRepository:
    return TransactionRepositoryInMemory()


def test_transaction_repository_store_get_transaction(
    transaction_repo: ITransactionRepository,
):
    transaction_repo.store_transaction(0, "01", "11", 85, 15)
    transaction_repo.store_transaction(0, "01", "21", 85, 15)
    transaction_repo.store_transaction(0, "01", "31", 85, 15)
    transaction_repo.store_transaction(1, "11", "12", 100, 0)
    transaction_repo.store_transaction(1, "11", "13", 100, 0)
    transaction_repo.store_transaction(1, "11", "01", 85, 15)
    for trans in transaction_repo.get_transactions(0):
        assert trans.amount == 85 and trans.profit == 15
    assert len(transaction_repo.get_transactions(1)) == 3


def test_transaction_repository_get_wallet_transactions(
    transaction_repo: ITransactionRepository,
):
    transaction_repo.store_transaction(0, "01", "11", 85, 15)
    transaction_repo.store_transaction(0, "01", "21", 85, 15)
    transaction_repo.store_transaction(0, "01", "31", 85, 15)
    transaction_repo.store_transaction(0, "01", "11", 85, 15)
    transaction_repo.store_transaction(0, "01", "21", 85, 15)
    transaction_repo.store_transaction(0, "01", "31", 85, 15)
    transaction_repo.store_transaction(1, "11", "01", 85, 15)
    transaction_repo.store_transaction(1, "11", "01", 85, 15)
    transaction_repo.store_transaction(1, "11", "01", 85, 15)
    for trans in transaction_repo.get_wallet_transactions("01"):
        assert trans.amount == 85 and trans.profit == 15
    assert len(transaction_repo.get_wallet_transactions("01")) == 9


def test_transaction_repository_get_statistics(
    transaction_repo: ITransactionRepository,
):
    transaction_repo.store_transaction(0, "01", "11", 85, 15)
    transaction_repo.store_transaction(0, "01", "21", 85, 15)
    transaction_repo.store_transaction(1, "11", "12", 100, 0)
    transaction_repo.store_transaction(1, "11", "13", 100, 0)
    transaction_repo.store_transaction(1, "11", "01", 85, 15)
    transaction_repo.store_transaction(0, "01", "21", 85, 15)
    stat: Statistics = transaction_repo.get_statistics()
    assert stat.total_transactions == 6 and stat.total_profit == 60
