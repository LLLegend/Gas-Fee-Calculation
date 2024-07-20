from data_providers.etherscan import EtherscanDataProvider
from data_providers.binance import BinanceDataProvider


def get_fee_by_txn(transaction_hash):
    etherscan_provider = EtherscanDataProvider()
    resp = etherscan_provider.get_transaction(transaction_hash=transaction_hash)

    gas_price = int(resp['gasPrice'])
    gas_used = int(resp['gasUsed'])
    eth_used = gas_used * gas_price ** -18

    timestamp = int(resp['timestamp'])
    return eth_used, timestamp


def get_eth_price_by_timestamp(timestamp):
    binance_provider = BinanceDataProvider()
    return