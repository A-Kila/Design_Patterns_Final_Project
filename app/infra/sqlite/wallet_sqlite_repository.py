from dataclasses import dataclass
from sqlite3 import Connection, Cursor

from app.infra.connection.database import Database


@dataclass
class WalletSqliteRepository:

    database: Database

    def __post_init__(self) -> None:
        connection: Connection = self.database.get_connection()

        connection.execute(
            """CREATE TABLE IF NOT EXISTS wallets(
            user_id integer, 
            wallet_address text PRIMARY KEY, 
            balance real NOT NULL, 
            FOREIGN KEY(user_id) references users(id))
        """
        )
        connection.commit()

    def create_wallet(self, user_id: int, wallet_address: str, balance: float) -> None:
        connection: Connection = self.database.get_connection()
        cursor: Cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO wallets VALUES(?, ?, ?)", (user_id, wallet_address, balance)
        )

        connection.commit()

    def get_wallet_count(self, user_id: int) -> int:
        connection: Connection = self.database.get_connection()
        cursor: Cursor = connection.cursor()

        result = cursor.execute(
            "SELECT COUNT(*) FROM wallets WHERE user_id = ?", (user_id,)
        ).fetchone()

        if result is None:
            return 0
        return result[0]

    def get_balance(self, wallet_address: str) -> float:
        connection: Connection = self.database.get_connection()
        cursor: Cursor = connection.cursor()

        result = cursor.execute(
            "SELECT balance FROM wallets WHERE wallet_address = ?", (wallet_address,)
        ).fetchone()

        if result is None:
            return -1
        return result[0]

    def wallet_exists(self, wallet_address: str) -> bool:
        connection: Connection = self.database.get_connection()
        cursor: Cursor = connection.cursor()

        result = cursor.execute(
            "SELECT * FROM wallets WHERE wallet_address = ?", (wallet_address,)
        ).fetchone()

        return result is not None

    def is_my_wallet(self, user_id: int, wallet_address: str) -> bool:
        connection: Connection = self.database.get_connection()
        cursor: Cursor = connection.cursor()

        result = cursor.execute(
            "SELECT * FROM wallets WHERE user_id = ? AND wallet_address = ?",
            (
                user_id,
                wallet_address,
            ),
        ).fetchone()

        return result is not None

    def make_transaction(self, from_wallet: str, to_wallet: str, amount: float) -> None:
        self.take_money(from_wallet, amount)
        self.give_money(to_wallet, amount)

    def take_money(self, from_wallet: str, amount: float) -> None:
        new_balance: float = self.get_balance(from_wallet) - amount
        self.set_balance(from_wallet, new_balance)

    def give_money(self, to_wallet: str, amount: float) -> None:
        new_balance: float = self.get_balance(to_wallet) + amount
        self.set_balance(to_wallet, new_balance)

    def set_balance(self, wallet_address, new_balance: float):
        connection: Connection = self.database.get_connection()
        cursor: Cursor = connection.cursor()

        cursor.execute(
            "UPDATE wallets SET balance = ? WHERE wallet_address = ?",
            (new_balance, wallet_address),
        )

        connection.commit()

    def drop_table(self) -> None:
        connection: Connection = self.database.get_connection()
        cursor: Cursor = connection.cursor()

        cursor.execute("DROP TABLE wallets")

        connection.commit()
