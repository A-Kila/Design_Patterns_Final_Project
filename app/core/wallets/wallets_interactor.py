from dataclasses import dataclass, field
from typing import Protocol

from app.core.wallets.wallet_generator import (
    WalletGetRequest,
    WalletGetResponse,
    WalletPostResponse,
)
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

    def create_wallet(self, api_key: str) -> WalletPostResponse:
        user_id: int = 1  # TODO change use api_key
        number_of_wallets: int = self.wallet_repo.get_wallet_amount(user_id=user_id)
        wallet_address: str = f"{user_id}{number_of_wallets + 1}"
        balance = self.INITIAL_WALLET_BALANCE

        self.wallet_repo.create_wallet(
            user_id=user_id,
            wallet_address=wallet_address,
            balance=balance,
        )

        balance_usd = 1  # TODO change

        return WalletPostResponse(
            balance_btc=balance, balance_usd=1, wallet_address=wallet_address
        )
