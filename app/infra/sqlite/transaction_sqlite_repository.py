from dataclasses import dataclass
from sqlite3 import Connection, Cursor

from app.core.interfaces.transitions_interface import Statistics, Transaction
from app.infra.connection.database import Database


@dataclass
class TransactionSqliteRepository:
    database: Database

    def __post_init__(self) -> None:
        con: Connection = self.database.get_connection()
        con.execute(
            """
            create table if not EXISTS transactions (
                user_id integer,
                wallet_from text,
                wallet_to TEXT,
                amount real,
                profit real,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN key(wallet_from) REFERENCES wallets(wallet_address),
                FOREIGN KEY(wallet_to) REFERENCES wallets(wallets_address)
            )
        """
        )

    def store_transaction(
        self,
        user_id: int,
        from_wallet: str,
        to_wallet: str,
        amount: float,
        profit: float,
    ) -> None:
        con: Connection = self.database.get_connection()
        cur: Cursor = con.cursor()

        cur.execute(
            "INSERT INTO transactions VALUES (?, ?, ?, ?, ?)",
            (user_id, from_wallet, to_wallet, amount, profit),
        )

        con.commit()

    def get_transactions(self, user_id: int) -> list[Transaction]:
        con: Connection = self.database.get_connection()
        cur: Cursor = con.cursor()

        cur.execute("SELECT * FROM transitions WHERE user_id=?", (user_id,))
        transactions_info = cur.fetchall()

        return self.__get_tranaction_list(transactions_info)

    def get_wallet_transactions(self, wallet_address: str) -> list[Transaction]:
        con: Connection = self.database.get_connection()
        cur: Cursor = con.cursor()

        cur.execute("SELECT * FROM transitions WHERE wallet_from=?", (wallet_address,))
        transactions_info = cur.fetchall()

        return self.__get_tranaction_list(transactions_info)

    def get_statistics(self) -> Statistics:
        con: Connection = self.database.connection
        cur: Cursor = con.cursor()

        cur.execute("SELECT COUNT(user_id), SUM(profit)")
        total_transactions, total_profit = cur.fetchone()

        return Statistics(total_transactions, total_profit)

    def __get_tranaction_list(
        self, info: list[tuple[int, str, str, float, float]]
    ) -> list[Transaction]:
        transactions: list[Transaction] = []
        for user, wallet_from, wallet_to, amount, profit in info:
            transactions.append(
                Transaction(user, wallet_from, wallet_to, amount, profit)
            )

        return transactions
