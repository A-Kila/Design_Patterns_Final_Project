import json

import requests


class CoinGeckoApi:
    RATE_URL: str = "https://api.coingecko.com/api/v3/exchange_rates"

    def get_rate(self, currency: str) -> float:
        response = requests.get(self.RATE_URL)
        response_data = json.loads(response.content)
        rates = response_data.get("rates", {})
        currency_rate = rates.get(currency, {})

        return float(currency_rate.get("value"))
