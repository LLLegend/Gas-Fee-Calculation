import mysql.connector
from datetime import date
import utils

class DB:
    def __init__(self, host='127.0.0.1', user='test_user', password='test123', database='test_db'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=3306
        )

    def get_current_block_number(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT block_number FROM transactions ORDER BY block_number DESC LIMIT 1")
        data = cursor.fetchall()
        cursor.close()
        if data:
            return data[0][0]
        else:
            return None

    def get_current_price_date(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT year(price_date), month(price_date), day(price_date) FROM prices ORDER BY price_date DESC LIMIT 1")
        data = cursor.fetchall()
        cursor.close()
        if data:
            return date(data[0][0], data[0][1], data[0][2])
        else:
            return None

    def get_price_by_date(self, price_date: date):
        year = price_date.year
        month = price_date.month
        day = price_date.day
        cursor = self.connection.cursor()
        sql = f"SELECT price FROM prices WHERE year(price_date) = {year} AND month(price_date) = {month} AND day(price_date) = {day}"
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        if data:
            return data[0][0]
        else:
            return None

    def get_gas_by_txn(self, txn_hash):
        cursor = self.connection.cursor()
        sql = f"SELECT gas_price, gas_used, transaction_timestamp FROM transactions WHERE transaction_hash = '{txn_hash}'"
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        if data:
            return int(data[0][0]), int(data[0][1]), int(data[0][2])
        else:
            return None, None, None

    def get_histories(self, start_date, end_date):
        cursor = self.connection.cursor()
        start_timestamp = utils.date_str_to_timestamp(start_date)
        end_timestamp = utils.date_str_to_timestamp(end_date)
        print(start_timestamp, end_timestamp)
        sql = f"SELECT DISTINCT * FROM transactions WHERE transaction_timestamp >= {start_timestamp} AND transaction_timestamp <= {end_timestamp}"
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        if data:
            return data
        else:
            return None

    def insert_transactions(
            self,
            block_number: list[int],
            transaction_hash: list[str],
            gas_price: list[int],
            gas_used: list[int],
            timestamp: list[int]
    ):
        cursor = self.connection.cursor()
        sql = """
                INSERT INTO transactions (block_number, transaction_hash, gas_price, gas_used, transaction_timestamp)
                VALUES (%s, %s, %s, %s, %s)
               """
        value = [(block_number[i], transaction_hash[i], gas_price[i], gas_used[i], timestamp[i])
                 for i in range(len(block_number))]
        cursor.executemany(sql, value)

        self.connection.commit()

    def insert_eth_history_prices(self, dates: list, prices: list):
        cursor = self.connection.cursor()
        sql = "INSERT INTO prices (price_date, price) VALUES (%s, %s)"
        value = [(dates[i], prices[i])
                 for i in range(len(dates))]
        cursor.executemany(sql, value)

        self.connection.commit()

    def close_connection(self):
        self.connection.close()

    def test(self):
        cursor = self.connection.cursor()
        cursor.execute("select * from transactions order by block_number desc limit 10;")
        return cursor.fetchall()
