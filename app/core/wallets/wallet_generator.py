from dataclasses import dataclass


@dataclass
class Wallet:
    user_id: int
    wallet_address: str
    balance: float
