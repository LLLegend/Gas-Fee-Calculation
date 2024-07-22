from flask import Flask, jsonify, request
import monitor
import utils
from db import DB

app = Flask(__name__)


# Provide the price of fees in USD for a given transaction hash
@app.route('/api/v1.0/transaction_fees', methods=['GET'])
def get_transaction_fee():
    txn_hash = request.args.get('txn_hash')
    db = DB()
    fee_price = db.get_fee_by_txn(txn_hash)
    db.close_connection()
    return jsonify({'txn_hash': txn_hash, 'fee_price': fee_price})


# Provide the historical data recording for a given period
@app.route('/api/v1.0/histories', methods=['GET'])
def get_histories():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    db = DB()
    result = db.get_histories(start_date, end_date)
    db.close_connection()
    return jsonify({'start_date': start_date, 'end_date': end_date, 'result': result})

@app.route('/api/v1.0/test', methods=['GET'])
def test():
    db = DB()
    result = db.test()
    db.close_connection()
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
