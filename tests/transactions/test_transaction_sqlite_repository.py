import pytest

from app.core.interfaces.transitions_interface import Statistics, Transaction
from app.infra.connection.database import Database
from app.infra.sqlite.transaction_sqlite_repository import TransactionSqliteRepository
from app.infra.sqlite.user_sqlite_repository import UserSqliteRepository
from app.infra.sqlite.wallet_sqlite_repository import WalletSqliteRepository
from definitions import TEST_DATABASE_NAME

USER_KEY1 = "user1"
USER_KEY2 = "user2"
WALLET_ADRESS1 = "wallet1"
WALLET_ADRESS2 = "wallet2"
WALLET_ADRESS3 = "wallet3"
START_BALANCE = 100000


@pytest.fixture
def database() -> Database:
    return Database(TEST_DATABASE_NAME)


@pytest.fixture
def transaction_repo(database: Database) -> TransactionSqliteRepository:
    transaction_repo = TransactionSqliteRepository(database)

    yield transaction_repo

    transaction_repo.clear()


@pytest.fixture(autouse=True)
def user_repo(database: Database) -> UserSqliteRepository:
    user_repo = UserSqliteRepository(database)

    user_repo.store_user(USER_KEY1)
    user_repo.store_user(USER_KEY2)

    yield user_repo

    user_repo.clear()


@pytest.fixture(autouse=True)
def wallet_repo(database: Database) -> WalletSqliteRepository:
    wallet_repo = WalletSqliteRepository(database)

    wallet_repo.create_wallet(USER_KEY1, WALLET_ADRESS1, START_BALANCE)
    wallet_repo.create_wallet(USER_KEY1, WALLET_ADRESS2, START_BALANCE)
    wallet_repo.create_wallet(USER_KEY2, WALLET_ADRESS3, START_BALANCE)

    yield wallet_repo

    wallet_repo.drop_table()


def test_transactions(
    transaction_repo: TransactionSqliteRepository,
    user_repo: UserSqliteRepository,
) -> None:
    user1 = user_repo.get_user_id(USER_KEY1)
    user2 = user_repo.get_user_id(USER_KEY2)

    transaction1 = Transaction(user1, WALLET_ADRESS1, WALLET_ADRESS3, 1.0, 0.5)
    transaction2 = Transaction(user2, WALLET_ADRESS3, WALLET_ADRESS2, 2.0, 1.0)
    transaction3 = Transaction(user1, WALLET_ADRESS1, WALLET_ADRESS3, 3.0, 0.0)
    transaction4 = Transaction(user1, WALLET_ADRESS2, WALLET_ADRESS2, 4.0, 0.0)

    transaction_repo.store_transaction(
        transaction1.user_id,
        transaction1.from_wallet,
        transaction1.to_wallet,
        transaction1.amount,
        transaction1.profit,
    )
    transaction_repo.store_transaction(
        transaction2.user_id,
        transaction2.from_wallet,
        transaction2.to_wallet,
        transaction2.amount,
        transaction2.profit,
    )
    transaction_repo.store_transaction(
        transaction3.user_id,
        transaction3.from_wallet,
        transaction3.to_wallet,
        transaction3.amount,
        transaction3.profit,
    )
    transaction_repo.store_transaction(
        transaction4.user_id,
        transaction4.from_wallet,
        transaction4.to_wallet,
        transaction4.amount,
        transaction4.profit,
    )

    assert transaction_repo.get_transactions(user1) == [transaction1, transaction3, transaction4]
    assert transaction_repo.get_transactions(user2) == [transaction2]

    assert transaction_repo.get_wallet_transactions(WALLET_ADRESS1) == [transaction1, transaction3]
    assert transaction_repo.get_wallet_transactions(WALLET_ADRESS2) == [transaction4]
    assert transaction_repo.get_wallet_transactions(WALLET_ADRESS3) == [transaction2]
    assert transaction_repo.get_wallet_transactions("Not a rea wallet") == []


def test_statistics(
    transaction_repo: TransactionSqliteRepository,
    user_repo: UserSqliteRepository,
) -> None:
    assert transaction_repo.get_statistics() == Statistics(0, 0.0)

    user1 = user_repo.get_user_id(USER_KEY1)
    user2 = user_repo.get_user_id(USER_KEY2)

    transaction1 = Transaction(user1, WALLET_ADRESS1, WALLET_ADRESS3, 1.0, 0.5)
    transaction_repo.store_transaction(
        transaction1.user_id,
        transaction1.from_wallet,
        transaction1.to_wallet,
        transaction1.amount,
        transaction1.profit,
    )

    assert transaction_repo.get_statistics() == Statistics(1, 0.5)

    transaction2 = Transaction(user2, WALLET_ADRESS3, WALLET_ADRESS2, 2.0, 1.0)
    transaction_repo.store_transaction(
        transaction2.user_id,
        transaction2.from_wallet,
        transaction2.to_wallet,
        transaction2.amount,
        transaction2.profit,
    )

    assert transaction_repo.get_statistics() == Statistics(2, 1.5)

    transaction3 = Transaction(user1, WALLET_ADRESS2, WALLET_ADRESS2, 4.0, 0.0)
    transaction_repo.store_transaction(
        transaction3.user_id,
        transaction3.from_wallet,
        transaction3.to_wallet,
        transaction3.amount,
        transaction3.profit,
    )

    assert transaction_repo.get_statistics() == Statistics(3, 1.5)
