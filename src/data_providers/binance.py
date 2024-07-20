class BinanceDataProvider:
    def __init__(self, api_key_path="api_keys/binance.key"):
        self.api_key = api_key_path
        self.api_url = "https://api.binance.com"
        self.headers = {}

    def get_eth_price_by_timestamp(self, timestamp):
        pass
