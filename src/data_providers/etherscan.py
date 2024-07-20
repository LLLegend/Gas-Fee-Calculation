class EtherscanDataProvider:
    def __init__(self, api_key_path="api_keys/etherscan.key"):
        self.api_key = ""
        self.api_url = "https://api.etherscan.io"
        self.headers = {}
        self.rate = 0

    def get_token_transfers(self, address, contract_address):
        resp = ""
        return resp.json()

    def get_transaction(self, transaction_hash):
        resp = ""
        return resp.json()

