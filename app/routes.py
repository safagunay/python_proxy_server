from flask import Flask
from flask import jsonify
from flask import request
from flask import session
from web3 import Web3
import json

from app import app

ganacheUrl = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganacheUrl))

# connect account 0
web3.eth.defaultAccount = web3.eth.accounts[0]

abi = json.loads('[{"inputs": [], "payable": false, "stateMutability": "nonpayable", "type": "constructor", "signature": "constructor" }, { "constant": false, "inputs": [ { "name": "devId", "type": "uint256" }, { "name": "log", "type": "string" } ], "name": "addLog", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function", "signature": "0x36d10002" }, { "constant": true, "inputs": [ { "name": "devId", "type": "uint256" } ], "name": "getLogs", "outputs": [ { "name": "", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function", "signature": "0x1124c05a"}]')

# address where we deploy the contract
address = web3.toChecksumAddress("0x3bbD0d11ECdc0300298159afF2f8981A69F9Be89")
contract = web3.eth.contract(address=address, abi=abi)

logs = [];

@app.route("/addLog", methods=['POST'])
def add_log():
    params = request.get_json()
    id = int(params['id'])
    log = params['log']
    tx_hash = contract.functions.addLog(id, log).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    #session['log'] = log
    return jsonify({'id':id, 'log':log})


@app.route("/getLogs", methods=['POST'])
def getLogs():
    params = request.get_json()
    id = int(params['id'])
    logs = contract.functions.getLogs(id).call()
    return logs;
    #return session['log']