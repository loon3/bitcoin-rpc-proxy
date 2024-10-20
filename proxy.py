from flask import Flask, jsonify, request
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

BITCOIND_RPC_URL = "http://counterparty-core-bitcoind-1:8332"
RPC_USER = "rpc"
RPC_PASSWORD = "rpc"

def call_rpc(method, params=None):
    headers = {'content-type': 'application/json'}
    payload = {
        "method": method,
        "params": params or [],
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(
        BITCOIND_RPC_URL,
        json=payload,
        headers=headers,
        auth=HTTPBasicAuth(RPC_USER, RPC_PASSWORD)
    )
    return response.json()

@app.route('/getblockchaininfo', methods=['GET'])
def get_blockchain_info():
    result = call_rpc("getblockchaininfo")
    return jsonify(result)

@app.route('/getrawtransaction/<txid>', methods=['GET'])
def get_raw_transaction(txid):
    result = call_rpc("getrawtransaction", [txid, True])
    return jsonify(result)

@app.route('/estimatesmartfee', methods=['GET'])
def estimate_smart_fee():
    result = call_rpc("estimatesmartfee", [6, "conservative"])
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
