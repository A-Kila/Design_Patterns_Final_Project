import json

import requests


class CoinGeckoApi:
    RATE_URL: str = "https://api.coingecko.com/api/v3/exchange_rates"

    def get_rate(self, currency: str) -> float:
        response = requests.get(self.RATE_URL)
        response_data = json.loads(response.content)
        rates = response_data.get("rates", {})
        currency = rates.get(currency, {})

        return currency.get("value")
