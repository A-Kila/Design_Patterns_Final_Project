from typing import Protocol


class IAddressGenerator(Protocol):
    @staticmethod
    def generate_address(user_id: str, num_wallets: int) -> str:
        pass


class SimpleAddressGenerator:
    @staticmethod
    def generate_address(user_id: str, number_of_wallets: int) -> str:
        return f"{user_id}_{number_of_wallets + 1}"
