from data_providers.etherscan import EtherscanDataProvider
from data_providers.binance import BinanceDataProvider
import time
from datetime import datetime, date

def timestamp_to_date(timestamp: int):
    date_time = datetime.fromtimestamp(timestamp)
    return date_time.date()

def date_to_milli_timestamp(date_: date):
    return int(time.mktime(date_.timetuple())) * 1000

def date_str_to_timestamp(date_: str):
    date_ = date_.split("-")
    date_ = date(int(date_[0]), int(date_[1]), int(date_[2]))
    return int(time.mktime(date_.timetuple()))

def cal_fee_price(gas_price: int, gas_used: int):
    fee_price = gas_price * 10 ** (-18) * gas_used
    return fee_price

def split_to_groups(candidates, max_members):
    groups = []
    for i in range(0, len(candidates), max_members):
        groups.append(candidates[i: i+max_members])
    return groups