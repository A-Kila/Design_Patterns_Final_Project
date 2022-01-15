from typing import Protocol


class IRateApi(Protocol):
    def get_rate(self, currency: str) -> float:
        pass
