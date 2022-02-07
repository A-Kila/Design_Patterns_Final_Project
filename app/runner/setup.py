from fastapi import FastAPI

from app.core.facade import WalletService
from app.infra.connection.database import Database
from app.infra.fastapi.api import wallet_api
from app.infra.sqlite.transaction_sqlite_repository import TransactionSqliteRepository
from app.infra.sqlite.user_sqlite_repository import UserSqliteRepository
from app.infra.sqlite.wallet_sqlite_repository import WalletSqliteRepository
from definitions import DATABASE_NAME


def setup() -> FastAPI:
    app = FastAPI()

    app.include_router(wallet_api)

    database: Database = Database(DATABASE_NAME)
    app.state.core = WalletService.create(
        UserSqliteRepository(database),
        WalletSqliteRepository(database),
        TransactionSqliteRepository(database),
    )

    return app
