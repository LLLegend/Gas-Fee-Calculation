from flask import Flask, jsonify, request
import monitor
import utils

app = Flask(__name__)

test = [
    {
        'id': 1,
        'chain': "eth",
    },
    {
        'id': 2,
        'chain': 'bsc',
    }
]


# Provide the price of fees in USD for a given transaction hash
@app.route('/api/v1.0/transaction_fees', methods=['GET'])
def get_transaction_fee():
    txn_hash = request.args.get('txn_hash')

    fees, timestamp = utils.get_fee_by_txn(txn_hash)
    price = utils.get_eth_price_by_timestamp(timestamp)
    fee_price = fees * price
    return jsonify({'txn_hash': txn_hash, 'fee_price': fee_price})


# Provide the historical data recording for a given period
@app.route('/api/v1.0/histories', methods=['GET'])
def get_histories():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    result = 0
    limit = 0
    return jsonify({'start_date': start_date, 'end_date': end_date, 'result': result})


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)
