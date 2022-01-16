from sqlite3 import Connection, Cursor

from app.infra.connection.database import Database


def test_connection() -> None:
    database: Database = Database("test.db")
    connection: Connection = database.get_connection()
    cursor: Cursor = connection.cursor()

    connection.execute("""CREATE TABLE IF NOT EXISTS test(name text)""")

    cursor.execute(
        """ SELECT count(name) FROM sqlite_master WHERE type='table' AND name='test' """
    )

    assert cursor.fetchone()[0] == 1

    cursor.execute("DROP TABLE test")

    cursor.execute(
        """ SELECT count(name) FROM sqlite_master WHERE type='table' AND name='test' """
    )

    assert cursor.fetchone()[0] == 0

    cursor.close()
