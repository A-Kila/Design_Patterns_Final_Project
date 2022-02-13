from fastapi import FastAPI

from app.core.facade import WalletService
from app.infra.connection.database import Database
from app.infra.fastapi.api import wallet_api
from app.infra.fastapi.exception_handler import HttpExceptionHandler
from app.infra.in_memory.rate_getter_in_memory import CoinGeckoApi
from app.infra.sqlite.transaction_sqlite_repository import TransactionSqliteRepository
from app.infra.sqlite.user_sqlite_repository import UserSqliteRepository
from app.infra.sqlite.wallet_sqlite_repository import WalletSqliteRepository
from definitions import DATABASE_NAME


def setup() -> FastAPI:
    app = FastAPI()

    app.include_router(wallet_api)

    database: Database = Database(DATABASE_NAME)
    exception_handler = HttpExceptionHandler()

    app.state.core = WalletService.create(
        UserSqliteRepository(database),
        WalletSqliteRepository(database),
        TransactionSqliteRepository(database),
        exception_handler,
        CoinGeckoApi(),
    )

    app.state.exception_handler = exception_handler

    return app
