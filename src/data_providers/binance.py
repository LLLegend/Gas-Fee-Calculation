import time
import requests


class BinanceDataProvider:
    def __init__(self):
        self.api_url = "https://api.binance.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
            "Connection": "close"
        }

    def get_daily_eth_price_by_timestamp(self, start, end):
        symbol = "ETHUSDT"
        interval = "1d"

        request_url = (self.api_url + "/api/v3/klines?symbol={}&interval={}&startTime={}&endTime={}".
                       format(symbol, interval, start, end))

        resp = requests.get(request_url, headers=self.headers)
        if resp.status_code == 200:
            # Use open price
            close_prices = []
            for i in range(len(resp.json())):
                close_prices.append(float(resp.json()[i][1]))
            return close_prices
        else:
            print(f"Failed connect to {request_url}.")
            return []
