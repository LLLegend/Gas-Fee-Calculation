from data_providers.etherscan import EtherscanDataProvider
from data_providers.binance import BinanceDataProvider
import time
from datetime import datetime, date


def date_to_milli_timestamp(date_: date):
    return int(time.mktime(date_.timetuple())) * 1000
