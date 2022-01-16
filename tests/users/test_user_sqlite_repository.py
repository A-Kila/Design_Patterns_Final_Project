import pytest

from app.infra.connection.database import Database
from app.infra.sqlite.user_sqlite_repository import UserSqliteRepository
from definitions import TEST_DATABASE_NAME


@pytest.fixture
def database() -> Database:
    return Database(TEST_DATABASE_NAME)


@pytest.fixture
def repo(database: Database) -> UserSqliteRepository:
    return UserSqliteRepository(database)


def test_user_repository(repo: UserSqliteRepository) -> None:
    repo.clear()

    api_key1 = "key1"
    api_key2 = "key2"
    api_key3 = "key3"
    api_key4 = "key4"

    repo.store_user(api_key1)
    repo.store_user(api_key2)
    repo.store_user(api_key3)
    repo.store_user(api_key4)

    assert repo.get_user_id(api_key1) == 1
    assert repo.get_user_id(api_key2) == 2
    assert repo.get_user_id(api_key3) == 3
    assert repo.get_user_id(api_key4) == 4

    with pytest.raises(Exception):
        repo.store_user(api_key1)

    with pytest.raises(Exception):
        repo.get_user_id("Not a real key")

    repo.clear()
