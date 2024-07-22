import time
import requests


class EtherscanDataProvider:
    def __init__(self, api_key_path="api_keys/etherscan.key"):
        with open(api_key_path, "r") as f:
            self.api_key = f.readline()
        self.api_url = "https://api.etherscan.io"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
            "Connection": "close"
        }
        self.rate = 0

    def get_token_transfers(self, address, token_address, start_block, end_block):
        # ERC-20 transfers from an address filtered by a token contract

        if start_block < end_block:
            request_url = (
                        self.api_url + "/api?sort=asc&module=account&action=tokentx&address={}&contractaddress={}&startblock={}&endblock={}&sort=asc&apikey={}"
                        .format(address, token_address, start_block, end_block, self.api_key))
            resp = requests.get(request_url, headers=self.headers)
            if resp.status_code == 200:
                return resp.json()["result"]
            else:
                return None

    def get_newest_block(self):
        request_url = (
            self.api_url + "/api?module=block&action=getblocknobytime&timestamp={}&apikey={}&closest=before"
            .format(time.time(), self.api_key)
        )
        resp = requests.get(request_url, headers=self.headers)
        if resp.status_code == 200:
            return resp.json()["result"]
        else:
            return None

