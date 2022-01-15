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
    rate_getter: CoinGeckoApi

    INITIAL_WALLET_BALANCE: int = 100000000

    def sats_to_btc(self, wallet_balance_sats: float) -> float:
        sats_to_btc: float = self.rate_getter.get_rate("sats")
        return wallet_balance_sats / sats_to_btc

    def btc_to_usd(self, wallet_balance_btc: float) -> float:
        usd_to_btc: float = self.rate_getter.get_rate("usd")
        return wallet_balance_btc * usd_to_btc

    def get_wallet(self, request: WalletGetRequest) -> WalletGetResponse:
        address: str = request.wallet_address
        wallet_balance_sats: float = self.wallet_repo.get_balance(
            request.wallet_address
        )

        wallet_balance_btc: float = self.sats_to_btc(wallet_balance_sats)
        wallet_balance_usd: float = self.btc_to_usd(wallet_balance_btc)

        return WalletGetResponse(
            wallet_address=address,
            balance_usd=wallet_balance_usd,
            balance_btc=wallet_balance_btc,
        )
