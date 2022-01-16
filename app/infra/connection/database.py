import sqlite3
from sqlite3 import Connection

import definitions


class Database:

    products_connection: Connection

    def __init__(self, database_name: str):
        self.connection = sqlite3.connect(
            definitions.ROOT_DIR + "\\database\\" + database_name,
            check_same_thread=False,
        )

    def get_connection(self) -> Connection:
        return self.connection
