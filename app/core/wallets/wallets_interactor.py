from dataclasses import dataclass, field
from typing import Protocol

from app.core.wallets.wallet_generator import WalletGetRequest, WalletGetResponse
from app.infra.rateapi.coingecko import CoinGeckoApi


class IRateApi(Protocol):
    def get_rate(self, currency: str) -> float:
        pass


class IWalletRepository(Protocol):
    def create_wallet(self, user_id: int, wallet_address: str, balance: float) -> None:
        pass

    def get_wallet_amount(self, user_id: int) -> int:
        pass

    def get_balance(self, wallet_address: str) -> float:
        pass


@dataclass
class WalletsInteractor:

    wallet_repo: IWalletRepository
    rate_getter: CoinGeckoApi = field(default_factory=CoinGeckoApi())

    INITIAL_WALLET_BALANCE: int = 100000000
