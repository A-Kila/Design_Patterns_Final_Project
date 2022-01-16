from dataclasses import dataclass
from sqlite3 import Connection, Cursor
from typing import Optional

from app.infra.connection.database import Database


@dataclass
class UserSqliteRepository:
    database: Database

    def __post_init__(self) -> None:
        self.__create_table()

    def store_user(self, api_key: str) -> None:
        con: Connection = self.database.get_connection()
        cur: Cursor = con.cursor()

        cur.execute("INSERT into users (api_key) values (?)", (api_key,))

        con.commit()

    def get_user_id(self, api_key: str) -> Optional[int]:
        con: Connection = self.database.get_connection()
        cur: Cursor = con.cursor()

        cur.execute("SELECT id FROM users WHERE api_key=?", (api_key,))
        user_id: Optional[int] = cur.fetchone()[0]

        return user_id

    def clear(self) -> None:
        con: Connection = self.database.get_connection()
        cur: Cursor = con.cursor()

        cur.execute("DROP TABLE users")

        con.commit()
        self.__create_table()

    def __create_table(self) -> None:
        con: Connection = self.database.get_connection()
        cur: Cursor = con.cursor()

        cur.execute(
            """
            create table if not EXISTS users
            (id integer PRIMARY key AUTOINCREMENT, api_key text UNIQUE)
        """
        )

        con.commit()
