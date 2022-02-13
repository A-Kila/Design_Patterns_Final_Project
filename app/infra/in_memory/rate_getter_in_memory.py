class RateGetterInMemory:
    RATES: dict[str, float] = {
        "sats": 100000000,
        "usd": 100000,
    }

    def get_rate(self, currency: str) -> float:
        return self.RATES[currency]
