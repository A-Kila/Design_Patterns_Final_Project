import pytest

from app.infra.connection.database import Database

DATABASE_NAME = "test.db"


@pytest.fixture
def database() -> Database:
    return Database(DATABASE_NAME)
