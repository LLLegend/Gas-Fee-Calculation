import datetime

from data_providers.etherscan import EtherscanDataProvider
from data_providers.binance import BinanceDataProvider
from db import DB
import time
import utils
from datetime import datetime, date, timedelta


# Update ETH history prices in batch
def prepare_eth_price(db: DB, start_date=date(2021, 1, 1)):
    max_receive = 400

    binance_provider = BinanceDataProvider()

    current_date = db.get_current_price_date()
    newest_date = datetime.utcnow().date()

    # The prices are updated
    if current_date == newest_date:
        return True
    else:
        # Start to update from start_date
        if current_date is None:
            start_date = start_date
        # Start to update from the newest date in db
        else:
            start_date = current_date

        dates = []
        delta = newest_date - start_date
        for i in range(delta.days + 1):
            dates.append(start_date + timedelta(days=i))

        # Since Binance support maximum 500 return prices, the dates should split into groups
        dates_groups = utils.split_to_groups(dates, max_receive)
        for group in dates_groups:
            start_timestamp = utils.date_to_milli_timestamp(group[0])
            end_timestamp = utils.date_to_milli_timestamp(group[-1])
            # UTC+8
            prices = binance_provider.get_daily_eth_price_by_timestamp(start_timestamp, end_timestamp+28800000)
            if prices is False:
                return False
            if len(prices) != 0 and len(group) != 0 and len(prices) == len(group):
                db.insert_eth_history_prices(group, prices)
                print("Successfully update ETH price until {}".format(group[-1]))
    return True

# Update pool transaction histories in batch
def preparing_history_transactions(db: DB, created_block, pool_address, token_0, token_1):
    batch_update_interval = 5000

    etherscan_provider = EtherscanDataProvider()

    current_block = db.get_current_block_number()
    if current_block is None:
        current_block = created_block

    newest_block = etherscan_provider.get_newest_block()
    if newest_block is None or newest_block is False:
        return False

    print("Current block in Database is: ", current_block)
    print("Newest block is: ", newest_block)

    # update records in batch
    while newest_block - current_block > batch_update_interval:
        start_block = max(current_block+1, created_block)
        end_block = min(start_block + batch_update_interval-1, newest_block)
        print("Updating pool transfers from block {} to {}".format(start_block, end_block))
        is_succeed = update_token_transfers(db, pool_address, token_0, start_block, end_block)
        if not is_succeed:
            return False
        is_succeed = update_token_transfers(db, pool_address, token_1, start_block, end_block)
        if not is_succeed:
            return False
        print("Successfully updating pool transfers\n")
        current_block = end_block
        time.sleep(0.3)
    return True


def update_pool_transfers(pool_address, token_0, token_1, created_block=0):
    print("Updating pool transfers...")

    db = DB()
    binance_provider = BinanceDataProvider()
    etherscan_provider = EtherscanDataProvider()

    # Need to update ETH prices from exchanges in batch firstly
    print("Start preparing ETH prices")
    is_succeed = prepare_eth_price(db, start_date=date(2021, 1, 1))
    if not is_succeed:
        print("Please re-run your monitor.")
        return
    print("Finished/Skip batch updating ETH prices")

    is_succeed = preparing_history_transactions(db, created_block, pool_address, token_0, token_1)
    if not is_succeed:
        print("Please re-run your monitor.")
        return
    print("Finished/Skip batch updating history pool transactions")

    current_date = db.get_current_price_date()
    # update records every 5s (real-time)
    while True:
        newest_date = datetime.utcnow().date()
        if current_date != newest_date:
            print("Updating today's ETH price")
            start = utils.date_to_milli_timestamp(newest_date)
            end = start
            prices = binance_provider.get_daily_eth_price_by_timestamp(start, end)
            if (len(prices)) != 0:
                db.insert_eth_history_prices(dates=[newest_date], prices=prices)
                print("Finished updating today's ETH price")


        current_date = db.get_current_price_date()
        if current_date != newest_date:
            print("Failed updating today's ETH price, will try next round.")

        newest_block = etherscan_provider.get_newest_block()
        current_block = db.get_current_block_number()
        if current_block == newest_block:
            time.sleep(5)
            continue
        print("Updating pool transfers from block {} to {}".format(current_block+1, newest_block))
        update_token_transfers(db, pool_address, token_0, current_block+1, newest_block)
        update_token_transfers(db, pool_address, token_1, current_block+1, newest_block)
        print("Successfully updating pool transfers\n")
        time.sleep(5)


def update_token_transfers(db: DB, address, token_address, start_block, end_block):
    etherscan_provider = EtherscanDataProvider()
    block_number = []
    transaction_hash = []
    gas_price = []
    gas_used = []
    timestamp = []

    results = etherscan_provider.get_token_transfers(address, token_address, start_block, end_block)
    if results is None or results is False:
        return False
    if len(results) != 0:
        for k in results:
            block_number.append(int(k["blockNumber"]))
            transaction_hash.append(k["hash"])
            gas_price.append(int(k["gasPrice"]))
            gas_used.append(int(k["gasUsed"]))
            timestamp.append(int(k["timeStamp"]))
        db.insert_transactions(block_number, transaction_hash, gas_price, gas_used, timestamp)
    return True

if __name__ == "__main__":
    usdc_uniswap_v3_pool = "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640"
    usdc_token_address = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
    weth_token_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    while True:
        update_pool_transfers(
            pool_address=usdc_uniswap_v3_pool,
            token_0=usdc_token_address,
            token_1=weth_token_address,
            created_block=12376729
        )
