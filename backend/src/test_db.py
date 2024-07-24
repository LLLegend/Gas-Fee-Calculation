from db import DB
import time
from datetime import date
import utils

db = DB()

a = int(time.mktime(date(2021, 1, 1).timetuple()))

s = utils.date_str_to_timestamp("2021-1-1")
print(s)

print(a)
cursor = db.connection.cursor()
sql = f"SELECT * FROM transactions WHERE transaction_timestamp >= 1612396800 AND transaction_timestamp <= 1614902400"
sql2 = "SELECT gas_price, gas_used FROM transactions WHERE transaction_hash = '0x48a0c6aba0e5f520f20e82d26ebd16fa672bd74f5cf6ffdecf742b25d837eb51'"
sql3 = "SELECT * FROM prices WHERE price_date = '2021-6-5'"
cursor.execute(sql2)
data = cursor.fetchall()
print(data)