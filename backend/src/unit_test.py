import unittest
from db import DB
import requests

class TestSystem(unittest.TestCase):
    def test_db_connection(self):
        db = DB()
        result = db.test()
        db.close_connection()
        self.assertIsNotNone(result)

    def test_db_query(self):
        db = DB()
        result = db.get_current_block_number()
        db.close_connection()
        self.assertIsNotNone(result)

    def test_history_api_with_wrong_arguments(self):
        start_date = "2021-05-06"
        end_date = "2021-05-32"
        url = "http://127.0.0.1:5000"
        url += "/api/v1.0/histories?start_date={}&end_date={}".format(start_date, end_date)
        resp = requests.get(url)
        self.assertEqual(resp.status_code, 400)

    def test_history_api_query_non_exist_data(self):
        start_date = "2025-05-06"
        end_date = "2025-05-07"
        url = "http://127.0.0.1:5000"
        url += "/api/v1.0/histories?start_date={}&end_date={}".format(start_date, end_date)
        resp = requests.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_history_api_for_correct_data(self):
        start_date = "2021-05-06"
        end_date = "2021-05-07"
        url = "http://127.0.0.1:5000"
        url += "/api/v1.0/histories?start_date={}&end_date={}".format(start_date, end_date)
        resp = requests.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_gas_fee_api_with_wrong_arguments(self):
        txn_hash = "0x"
        url = "http://127.0.0.1:5000"
        url += "/api/v1.0/transaction-fees?txn_hash={}".format(txn_hash)
        resp = requests.get(url)
        self.assertEqual(resp.status_code, 400)

    def test_gas_fee_api_query_non_exist_data(self):
        txn_hash = "0x1463aa99450836d1a5f30bb2a4a327f0f5fdc24aabd5af085695c4b9360e8370"
        url = "http://127.0.0.1:5000"
        url += "/api/v1.0/transaction-fees?txn_hash={}".format(txn_hash)
        resp = requests.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_gas_fee_api_for_correct_data(self):
        txn_hash = "0x6d9dcc2254fcc904bb6966956aba709454e7b9937fb4bb9bbe3829e33155bb10"
        url = "http://127.0.0.1:5000"
        url += "/api/v1.0/transaction-fees?txn_hash={}".format(txn_hash)
        resp = requests.get(url)
        self.assertEqual(resp.status_code, 200)

if __name__ == '__main__':
    unittest.main()