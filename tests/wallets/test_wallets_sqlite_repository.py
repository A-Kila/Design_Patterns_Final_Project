import pytest

from app.infra.connection.database import Database
from app.infra.sqlite.user_sqlite_repository import UserSqliteRepository
from app.infra.sqlite.wallet_sqlite_repository import WalletSqliteRepository
from definitions import TEST_DATABASE_NAME


@pytest.fixture
def database() -> Database:
    return Database(TEST_DATABASE_NAME)


@pytest.fixture
def user_repository(database: Database) -> UserSqliteRepository:
    return UserSqliteRepository(database)


@pytest.fixture
def wallet_repository(database: Database) -> WalletSqliteRepository:
    return WalletSqliteRepository(database)


def test_wallets_repository(
    wallet_repository: WalletSqliteRepository, user_repository: UserSqliteRepository
) -> None:
    user_repository.clear()

    base_balance: float = 100000000.0

    api_key1: str = "test1"
    api_key2: str = "test2"
    api_key3: str = "test3"

    user_repository.store_user(api_key1)
    user_repository.store_user(api_key2)
    user_repository.store_user(api_key3)

    user_id1: int = user_repository.get_user_id(api_key1)
    user_id2: int = user_repository.get_user_id(api_key2)
    user_id3: int = user_repository.get_user_id(api_key3)

    wallet_address1_1: str = f"{user_id1}_1"
    wallet_address1_2: str = f"{user_id1}_2"
    wallet_address2_1: str = f"{user_id2}_1"

    wallet_repository.create_wallet(user_id1, wallet_address1_1, 100000000.0)
    wallet_repository.create_wallet(user_id1, wallet_address1_2, 100000000.0)
    wallet_repository.create_wallet(user_id2, wallet_address2_1, 100000000.0)

    assert wallet_repository.wallet_exists(wallet_address1_1)
    assert wallet_repository.wallet_exists(wallet_address1_2)
    assert wallet_repository.wallet_exists(wallet_address2_1)
    assert not wallet_repository.wallet_exists("Incorrect string")

    assert wallet_repository.get_wallet_count(user_id1) == 2
    assert wallet_repository.get_wallet_count(user_id2) == 1
    assert wallet_repository.get_wallet_count(user_id3) == 0

    assert wallet_repository.is_my_wallet(user_id1, wallet_address1_1)
    assert wallet_repository.is_my_wallet(user_id1, wallet_address1_2)
    assert wallet_repository.is_my_wallet(user_id2, wallet_address2_1)
    assert not wallet_repository.is_my_wallet(user_id1, wallet_address2_1)
    assert not wallet_repository.is_my_wallet(user_id2, wallet_address1_1)
    assert not wallet_repository.is_my_wallet(user_id2, wallet_address1_2)
    assert not wallet_repository.is_my_wallet(user_id3, wallet_address1_1)

    assert wallet_repository.get_balance(wallet_address1_1) == base_balance
    assert wallet_repository.get_balance(wallet_address1_2) == base_balance
    assert wallet_repository.get_balance(wallet_address2_1) == base_balance

    wallet_repository.make_transaction(wallet_address1_1, wallet_address1_2, 100, 100)

    assert wallet_repository.get_balance(wallet_address1_1) == base_balance - 100
    assert wallet_repository.get_balance(wallet_address1_2) == base_balance + 100

    wallet_repository.make_transaction(wallet_address1_2, wallet_address2_1, 200, 100)

    assert wallet_repository.get_balance(wallet_address1_2) == base_balance - 100
    assert wallet_repository.get_balance(wallet_address2_1) == base_balance + 100

    wallet_repository.drop_table()
