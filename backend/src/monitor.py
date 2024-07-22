import datetime

from data_providers.etherscan import EtherscanDataProvider
from data_providers.binance import BinanceDataProvider
from db import DB
import time
import utils
from datetime import datetime, date, timedelta


# Update ETH history prices
def prepare_eth_price(db: DB, start_date=date(2021, 1, 1)):
    binance_provider = BinanceDataProvider()

    current_date = db.get_current_price_date()
    newest_date = datetime.now().date()
    if current_date == newest_date:
        return
    else:
        if current_date is None:
            start_date = start_date
        else:
            start_date = current_date

        dates = []
        delta = newest_date - start_date
        for i in range(delta.days + 1):
            dates.append(start_date + timedelta(days=i))

        start_timestamp = utils.date_to_milli_timestamp(start_date)
        newest_timestamp = utils.date_to_milli_timestamp(newest_date)
        prices = binance_provider.get_daily_eth_price_by_timestamp(start_timestamp, newest_timestamp)

        if len(prices) != 0 and len(dates) != 0 and len(prices) == len(dates):
            db.insert_eth_history_prices_table(dates, prices)
            print("Successfully update ETH price until {}".format(newest_date))


def update_pool_transfers(pool_address, token_0, token_1, created_block=0):
    print("Updating pool transfers...")

    batch_update_interval = 5000

    db = DB()

    # Need to update ETH price from exchanges in batch firstly
    print("Start preparing ETH prices")
    prepare_eth_price(db, start_date=date(2021, 1, 1))

    etherscan_provider = EtherscanDataProvider()
    binance_provider = BinanceDataProvider()

    current_block = db.get_current_block_number()
    newest_block = etherscan_provider.get_newest_block()
    print("Current block in Database is: ", current_block)
    print("Newest block is: ", newest_block)

    # update records in batch
    while newest_block - current_block > batch_update_interval:
        start_block = max(current_block+1, created_block)
        end_block = min(start_block + batch_update_interval-1, newest_block)
        print("Updating pool transfers from block {} to {}".format(start_block, end_block))
        update_token_transfers(db, pool_address, token_0, start_block, end_block)
        update_token_transfers(db, pool_address, token_1, start_block, end_block)
        print("Successfully updating pool transfers\n")
        current_block = db.get_current_block_number()
        time.sleep(0.5)

    print("Finished/Skip batch updating")

    current_date = db.get_current_price_date()
    # update records every 5s (real-time)
    while True:
        newest_date = datetime.now().date()
        if current_date != newest_date:
            print("Updating today's ETH price")
            start = utils.date_to_milli_timestamp(newest_date)
            print("Finished updating today's ETH price")
            end = start
            price = binance_provider.get_daily_eth_price_by_timestamp(start, end)
            db.insert_eth_history_prices_table(dates=[newest_date], prices=price)
            current_date = db.get_current_price_date()

        newest_block = etherscan_provider.get_newest_block()
        if current_block == newest_block:
            time.sleep(5)
            continue
        print("Updating pool transfers from block {} to {}".format(current_block+1, newest_block))
        update_token_transfers(db, pool_address, token_0, current_block+1, newest_block)
        update_token_transfers(db, pool_address, token_1, current_block+1, newest_block)
        print("Successfully updating pool transfers\n")
        current_block = db.get_current_block_number()
        time.sleep(5)


def update_token_transfers(db: DB, address, token_address, start_block, end_block):
    etherscan_provider = EtherscanDataProvider()
    block_number = []
    transaction_hash = []
    gas_price = []
    gas_used = []
    timestamp = []

    results = etherscan_provider.get_token_transfers(address, token_address, start_block, end_block)
    for k in results:
        block_number.append(int(k["blockNumber"]))
        transaction_hash.append(k["hash"])
        gas_price.append(int(k["gasPrice"]))
        gas_used.append(int(k["gasUsed"]))
        timestamp.append(int(k["timeStamp"]))

    db.insert_transactions(block_number, transaction_hash, gas_price, gas_used, timestamp)


if __name__ == "__main__":
    usdc_uniswap_v3_pool = "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640"
    usdc_token_address = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
    weth_token_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    update_pool_transfers(
        pool_address=usdc_uniswap_v3_pool,
        token_0=usdc_token_address,
        token_1=weth_token_address,
        created_block=12376729
    )
