import time
import requests
import os


class BinanceDataProvider:
    def __init__(self):
        self.api_url = "https://api.binance.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
            "Connection": "close"
        }
        self.proxies = {
            'http': 'http://127.0.0.1:7890',
            'https': 'https://127.0.0.1:7890'
        }
        self.max_retries = 5

    def get_daily_eth_price_by_timestamp(self, start, end):
        symbol = "ETHUSDT"
        interval = "1d"

        for i in range(self.max_retries):
            if start <= end:
                request_url = (self.api_url + "/api/v3/klines?symbol={}&interval={}&startTime={}&endTime={}".
                        format(symbol, interval, start, end))

                resp = requests.get(request_url, headers=self.headers)
                if resp.status_code == 200:
                    # Use open price
                    close_prices = []
                    for j in range(len(resp.json())):
                        close_prices.append(float(resp.json()[j][1]))
                    return close_prices
                else:
                    continue
        print("Unable to get eth prices from Binance, please check your network or the arguments!")
        return False
