import pytest
import transaction as transaction

from app.core.interfaces.transitions_interface import ITransactionRepository, Statistics
from app.core.interfaces.wallets_interface import IWalletRepository
from app.core.users.users_interactor import IUserRepository
from app.infra.in_memory.transactions_repository import TransactionRepositoryInMemory
from app.infra.in_memory.user_in_memory import UserInMemoryRepository
from app.infra.in_memory.wallet_repository import InMemoryWalletRepository

@pytest.fixture()
def starting_user_id() -> int:
    return 0

@pytest.fixture()
def user_repo() -> IUserRepository:
    return UserInMemoryRepository()


@pytest.fixture()
def wallet_repo() -> IWalletRepository:
    return InMemoryWalletRepository()

@pytest.fixture()
def transaction_repo() -> ITransactionRepository:
    return TransactionRepositoryInMemory()


def test_user_repository_store_get_user(user_repo: IUserRepository):
    user_repo.store_user("0imfnc8mVLWwsAawjYr4Rx")
    user_repo.store_user("1imfnc8mVLWwsAawjYr4Rx")
    assert user_repo.get_user_id("0imfnc8mVLWwsAawjYr4Rx") == user_repo.get_user_id(
        "0imfnc8mVLWwsAawjYr4Rx"
    )
    assert user_repo.get_user_id("1imfnc8mVLWwsAawjYr4Rx") != user_repo.get_user_id(
        "0imfnc8mVLWwsAawjYr4Rx"
    )
    user_repo.store_user("3imfnc8mVLWwsAawjYr4Rx")
    user_repo.store_user("4imfnc8mVLWwsAawjYr4Rx")
    assert user_repo.get_user_id("3imfnc8mVLWwsAawjYr4Rx") == user_repo.get_user_id(
        "3imfnc8mVLWwsAawjYr4Rx"
    )
    assert user_repo.get_user_id("4imfnc8mVLWwsAawjYr4Rx") != user_repo.get_user_id(
        "0imfnc8mVLWwsAawjYr4Rx"
    )


def test_user_repository_store_get_with_more_input(starting_user_id: int, user_repo: IUserRepository):
    for i in range(1000):
        api_key: str = "apy_key" + str(i)
        user_repo.store_user(api_key)
        cur_id: int = user_repo.get_user_id(api_key)
        assert cur_id == starting_user_id + i


def test_wallet_repository_create_wallet(starting_user_id: int,
                                         user_repo: IUserRepository,
                                         wallet_repo: IWalletRepository):
    user_repo.store_user("user_0")
    user_id: int = starting_user_id
    wallet_repo.create_wallet(user_id, "0wallet1", 1.0)
    assert wallet_repo.get_wallet_count(user_id) == 1 #needs to be finished


def test_wallet_repository_get_wallet_amount(starting_user_id: int,
                                             user_repo: IUserRepository,
                                             wallet_repo: IWalletRepository):
    user_repo.store_user("user_0")
    user_id: int = starting_user_id
    assert wallet_repo.get_wallet_count(user_id) == 0

    wallet_repo.create_wallet(user_id, "0wallet1", 1.0)
    assert wallet_repo.get_wallet_count(user_id) == 1

    wallet_repo.create_wallet(user_id, "0wallet2", 1.0)
    assert wallet_repo.get_wallet_count(user_id) == 2

    wallet_repo.create_wallet(user_id, "0wallet3", 1.0)
    assert wallet_repo.get_wallet_count(user_id) == 3


def test_wallet_repository_balance(starting_user_id: int,
                                   user_repo: IUserRepository,
                                   wallet_repo: IWalletRepository):
    user_repo.store_user("user_0")
    user_id: int = starting_user_id
    wallet_repo.create_wallet(user_id, "0wallet1", 1.0)
    wallet_repo.create_wallet(user_id, "0wallet2", 0.0)
    assert wallet_repo.get_balance("0wallet1") == 1
    wallet_repo.make_transaction("0wallet1", "0wallet2", 1.0)
    assert wallet_repo.get_balance("0wallet1") == 0


def test_wallet_repository_wallet_exists(wallet_repo: IWalletRepository,
                                         user_repo: IUserRepository,
                                         starting_user_id: int,
                                         ):
    user_repo.store_user("user_0")
    user_id: int = starting_user_id
    wallet_repo.create_wallet(user_id, "0wallet1", 1.0)
    assert wallet_repo.wallet_exists("0wallet1") is True
    assert wallet_repo.wallet_exists("wrongwalletaddress") is not True
    wallet_repo.create_wallet(user_id, "0wallet2", 1.0)
    assert wallet_repo.wallet_exists("0wallet2") is True
    assert wallet_repo.wallet_exists("wrongwalletaddress") is not True


def test_wallet_repository_is_my_wallet(wallet_repo: IWalletRepository,
                                        user_repo: IUserRepository,
                                        starting_user_id: int,
                                        ):
    user_id: int = starting_user_id
    user_repo.store_user("user_0")
    user_repo.store_user("user_1")
    assert user_repo.get_user_id("user_0") == user_id
    assert user_repo.get_user_id("user_1") == user_id+1

    wallet_repo.create_wallet(user_id, "0wallet1", 1.0)
    wallet_repo.create_wallet(user_id+1, "1wallet1", 1.0)

    assert wallet_repo.is_my_wallet(user_id, "0wallet1")  # needs to be finished
    assert not (wallet_repo.is_my_wallet(user_id, "1wallet1")) # wallet repo failed


def test_wallet_repository_make_transaction(wallet_repo: IWalletRepository,
                                            user_repo: IUserRepository,
                                            starting_user_id: int,):
    user_id: int = starting_user_id
    user_repo.store_user("user_0")
    user_repo.store_user("user_1")
    wallet_repo.create_wallet(user_id, "0wallet1", 1.0)
    wallet_repo.create_wallet(user_id, "0wallet2", 1.0)
    wallet_repo.create_wallet(user_id+1, "1wallet1", 1.0)
    wallet_repo.make_transaction("0wallet1", "1wallet1", 1.0)
    assert wallet_repo.get_balance("0wallet1") == 0
    assert wallet_repo.get_balance("1wallet1") == 2
    wallet_repo.make_transaction("1wallet1", "0wallet1", 2.0)
    assert wallet_repo.get_balance("1wallet1") == 0
    assert wallet_repo.get_balance("0wallet1") == 2
    wallet_repo.make_transaction("0wallet1", "0wallet2", 2.0)
    assert wallet_repo.get_balance("0wallet1") == 0
    assert wallet_repo.get_balance("0wallet2") == 3


def test_wallet_repository_take_money(wallet_repo: IWalletRepository,
                                      user_repo: IUserRepository,
                                      starting_user_id: int,):
    user_id: int = starting_user_id
    user_repo.store_user("user_0")
    user_repo.store_user("user_1")
    wallet_repo.create_wallet(user_id, "0wallet1", 1.0)
    wallet_repo.create_wallet(user_id, "0wallet2", 1.0)
    wallet_repo.create_wallet(user_id+1, "1wallet1", 1.0)
    wallet_repo.take_money("0wallet1", 1.0)
    assert wallet_repo.get_balance("0wallet1") == 0
    wallet_repo.take_money("1wallet1", 0.5)
    assert wallet_repo.get_balance("1wallet1") == 0.5
    wallet_repo.take_money("0wallet2", 0)
    assert wallet_repo.get_balance("0wallet2") == 1


def test_wallet_repository_give_money(wallet_repo: IWalletRepository,
                                      user_repo: IUserRepository,
                                      starting_user_id: int,):
    user_id: int = starting_user_id
    user_repo.store_user("user_0")
    user_repo.store_user("user_1")
    wallet_repo.create_wallet(user_id, "0wallet1", 1.0)
    wallet_repo.create_wallet(user_id, "0wallet2", 1.0)
    wallet_repo.create_wallet(user_id+1, "1wallet1", 1.0)
    wallet_repo.give_money("0wallet1", 1.0)
    assert wallet_repo.get_balance("0wallet1") == 2
    wallet_repo.give_money("1wallet1", 0.5)
    assert wallet_repo.get_balance("1wallet1") == 1.5
    wallet_repo.give_money("0wallet2", 0)
    assert wallet_repo.get_balance("0wallet2") == 1


def test_transaction_repository_store_get_transaction(transaction_repo: ITransactionRepository):
    transaction_repo.store_transaction(0, "01", "11", 85, 15)
    transaction_repo.store_transaction(0, "01", "21", 85, 15)
    transaction_repo.store_transaction(0, "01", "31", 85, 15)
    transaction_repo.store_transaction(1, "11", "12", 100, 0)
    transaction_repo.store_transaction(1, "11", "13", 100, 0)
    transaction_repo.store_transaction(1, "11", "01", 85, 15)
    for trans in transaction_repo.get_transactions(0):
        assert trans.amount == 85 and trans.profit == 15
    assert len(transaction_repo.get_transactions(1)) == 3


def test_transaction_repository_get_wallet_transactions(transaction_repo: ITransactionRepository):
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


def test_transaction_repository_get_statistics(transaction_repo: ITransactionRepository):
    transaction_repo.store_transaction(0, "01", "11", 85, 15)
    transaction_repo.store_transaction(0, "01", "21", 85, 15)
    transaction_repo.store_transaction(1, "11", "12", 100, 0)
    transaction_repo.store_transaction(1, "11", "13", 100, 0)
    transaction_repo.store_transaction(1, "11", "01", 85, 15)
    transaction_repo.store_transaction(0, "01", "21", 85, 15)
    stat: Statistics = transaction_repo.get_statistics()
    assert stat.total_transactions == 6 and stat.total_profit == 60
