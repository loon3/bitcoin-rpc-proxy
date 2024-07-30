from flask import Flask, jsonify, request
import requests
from requests.auth import HTTPBasicAuth
import hashlib
from pycoin.symbols.btc import network

app = Flask(__name__)

BITCOIND_RPC_URL = "http://counterparty-core-bitcoind-1:8332"
RPC_USER = "rpc"
RPC_PASSWORD = "rpc"

ADDRINDEX_RPC_URL = "http://counterparty-core-addrindex-1:8432"

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

def _script_hash(script):
    return hashlib.sha256(script).digest()[::-1].hex()

def address_to_script_hash(address):
    return _script_hash(network.parse.address(address).script())

def call_addrindex_rpc(method, params=None):
    headers = {'content-type': 'application/json'}
    payload = {
        "method": method,
        "params": params or [],
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(
        ADDRINDEX_RPC_URL,
        json=payload,
        headers=headers
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

@app.route('/listunspent/<address>', methods=['GET'])
def list_unspent(address):
    try:
        script_hash = address_to_script_hash(address)
        result = call_addrindex_rpc("blockchain.scripthash.listunspent", [script_hash])
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
