from dataclasses import dataclass


@dataclass
class Wallet:
    user_id: int
    wallet_address: str
    balance: float


@dataclass
class WalletGetRequest:
    api_key: str
    wallet_address: str


@dataclass
class WalletGetResponse:
    balance_btc: float
    balance_usd: float
    wallet_address: str


@dataclass
class WalletPostRequest:
    api_key: str


@dataclass
class WalletPostResponse:
    balance_btc: float
    balance_usd: float
    wallet_address: str
