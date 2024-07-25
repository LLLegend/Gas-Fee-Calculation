import time

from flask import Flask, jsonify, request
import utils
from db import DB

app = Flask(__name__)

# Provide the price of fees in USD for a given transaction hash
# Argument: txn_hash
# Example: /api/v1.0/transaction_fees?txn_hash=
@app.route('/api/v1.0/transaction-fees', methods=['GET'])
def get_transaction_fee():
    txn_hash = request.args.get('txn_hash')
    if type(txn_hash) != str or len(txn_hash) != 66 or txn_hash[0: 2] != "0x":
        response = {
            "message": "Invalid Arguments",
            "results": ""
        }
        return jsonify(response)
    db = DB(host="db")
    gas_price, gas_used, timestamp = db.get_gas_by_txn(txn_hash)
    if gas_price is None:
        response = {
            "message": "Transaction Not Found",
            "results": ""
        }
        return jsonify(response)
    gas_in_ETH = utils.cal_fee_price(gas_price, gas_used)
    eth_price = db.get_price_by_date(utils.timestamp_to_date(timestamp))
    db.close_connection()
    if eth_price is None:
        response = {
            "message": "Transaction Not Found",
            "results": ""
        }
        return jsonify(response)

    results = {
        "txn_hash": txn_hash,
        "fee_price": gas_in_ETH * eth_price
    }
    response = {
        "message": "Succeed",
        "results": results
    }
    return jsonify(response)


# Provide the historical data recording for a given period
# Arguments: start_date, end_date
# Example: /api/v1.0/histories?start_date=2021-1-1&end_date=2023-1-1
@app.route('/api/v1.0/histories', methods=['GET'])
def get_histories():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    try:
        time.strptime(start_date, "%Y-%m-%d")
        time.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        response = {
            "message": "Invalid Arguments",
            "results": ""
        }
        return jsonify(response)
    db = DB(host="db")
    results= db.get_histories(start_date, end_date)
    db.close_connection()

    if results is None:
        response = {
            "message": "History Transactions Not Found",
            "results": ""
        }
        return jsonify(response)

    col_name = ["block_number", "transaction_hash", "gas_price", "gas_used", "timestamp"]
    for i in range(len(results)):
        results[i] = dict(zip(col_name, results[i]))
    response = {
        "message": "Succeed",
        "results": results
    }
    return jsonify(response)

@app.route('/api/v1.0/test', methods=['GET'])
def test():
    db = DB(host="db")
    result = db.test()
    db.close_connection()
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
