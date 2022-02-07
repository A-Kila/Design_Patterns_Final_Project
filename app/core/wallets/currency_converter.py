from typing import Protocol

from app.core.interfaces.wallets_interface import IRateApi


class CurrencyConverter(Protocol):
    @staticmethod
    def convert_to(amount: float, to_currency: str, rate_getter: IRateApi) -> float:
        pass

    @staticmethod
    def convert_from(amount: float, from_currency: str, rate_getter: IRateApi) -> float:
        pass


class BitcoinConverter:
    @staticmethod
    def convert_to(amount: float, to_currency: str, rate_getter: IRateApi) -> float:
        btc_to_usd: float = rate_getter.get_rate(to_currency)
        return amount * btc_to_usd

    @staticmethod
    def convert_from(amount: float, from_currency: str, rate_getter: IRateApi) -> float:
        sats_to_btc: float = rate_getter.get_rate(from_currency)
        return amount / sats_to_btc
