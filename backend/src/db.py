import mysql.connector
from datetime import date


class DB:
    def __init__(self, host='db', user='test_user', password='test123', database='test_db'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def get_current_block_number(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT block_number FROM transactions ORDER BY block_number DESC LIMIT 1")
        data = cursor.fetchall()
        cursor.close()
        return data[0][0]

    def get_current_price_date(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT year(date), month(date), day(date) FROM prices ORDER BY price_date DESC LIMIT 1")
        data = cursor.fetchall()
        cursor.close()
        return date(data[0][0], data[0][1], data[0][2])

    def get_fee_by_txn(self, txn_hash):
        cursor = self.connection.cursor()
        sql = ""
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        return data[0][0]

    def get_histories(self, start_date, end_date):
        return

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
                INSERT INTO transactions (block_number, transaction_hash, gas_price, gas_used, timestamp)
                VALUES (%s, %s, %s, %s, %s)
               """
        value = [(block_number[i], transaction_hash[i], gas_price[i], gas_used[i], timestamp[i])
                 for i in range(len(block_number))]
        cursor.executemany(sql, value)

        self.connection.commit()

    def insert_eth_history_prices_table(self, dates: list, prices: list):
        cursor = self.connection.cursor()
        sql = "INSERT INTO prices (date, price) VALUES (%s, %s)"
        value = [(dates[i], prices[i])
                 for i in range(len(dates))]
        cursor.executemany(sql, value)

        self.connection.commit()

    def close_connection(self):
        self.connection.close()

    def test(self):
        cursor = self.connection.cursor()
        cursor.execute("SHOW TABLES;")
        return cursor.fetchall()