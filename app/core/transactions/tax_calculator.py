from dataclasses import dataclass
from typing import Protocol


class ITax(Protocol):
    @property
    def tax_rate(self) -> float:
        pass


class DifferentUserTax:
    @property
    def tax_rate(self) -> float:
        return 0.015


class FreeTax(ITax):
    @property
    def tax_rate(self) -> float:
        return 0


@dataclass
class TaxCalculator:
    tax: ITax = FreeTax()

    def get_money_transfered(self, amount: float) -> float:
        return amount * (1 - self.tax.tax_rate)

    def get_tax(self, amount: float) -> float:
        return amount * self.tax.tax_rate
