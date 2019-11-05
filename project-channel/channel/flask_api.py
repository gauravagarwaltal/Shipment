#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:09:35 2019

@author: gaurava
"""
# from flask_cors import CORS
import configparser
import json
import os
import pickle
from uuid import uuid4

import requests
from flask import Flask, request, jsonify
from flask.logging import default_handler

from channel.User import User

os.system("clear")

# Instantiate the Node
app = Flask(__name__)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')


@app.route('/get_pending_state', methods=['GET'])
def get_pending_state():
    return jsonify(user.get_pending_requests()), 200


@app.route('/get_state', methods=['GET'])
def get_channel_state():
    return jsonify(user.get_state()), 200


@app.route('/validate', methods=['POST'])
def validate():
    try:
        address = request.form['address']
        key = request.form['privateKey']
        flag = User.validate_address(address, key)
        if flag:
            user.add_address(address, key)
        return jsonify(flag), 200
    except:
        return jsonify(False), 200


@app.route('/', methods=['GET'])
def empty():
    payload = {'client': user.address, 'vendor': user.opponent,
               'amount': str(user.contract.functions.getBalance().call())}
    return jsonify(payload), 200


@app.route('/balance', methods=['GET'])
def balance():
    try:
        address = request.args.get('address')
        bal = user.get_balance(address)
        if bal is not None:
            return jsonify(bal), 200
    except:
        return jsonify("error"), 200


@app.route('/verify_state_change', methods=['POST'])
def verify_state_change():
    # try:
    values = request.get_json()
    count = int(values.get('count'))
    sender_bal = int(values.get('sender_bal'))
    recipient_bal = int(values.get('recipient_bal'))
    hex_sign = values.get('sign')
    signature = str(hex_sign)[2:]
    signature = bytes.fromhex(signature)
    if user.check_sign(count, sender_bal, recipient_bal, signature, user.opponent):
        user.pending_requests[len(user.pending_requests)+1] = json.dumps(
            {'count': count, 'sender_bal': sender_bal, 'recipient_bal': recipient_bal,
             'sign': hex_sign})
        return jsonify("request processed and added to pending queue"), 200
    else:
        return jsonify("request processed and discarded"), 201
# except:
#     return jsonify(False), 201


@app.route('/state_change_response', methods=['POST'])
def update_response():
    values = request.get_json()
    count = int(values.get('count'))
    sender_bal = int(values.get('sender_bal'))
    recipient_bal = int(values.get('recipient_bal'))
    print(values.get('signature'))
    signature = str(values.get('signature'))[2:]
    print(signature)
    signature = bytes.fromhex(signature)
    if user.check_sign(count, sender_bal, recipient_bal, signature, user.opponent):
        user.state.update_state(count, sender_bal, recipient_bal, signature.hex())
    else:
        pass
    return jsonify("state change response processed"), 200


@app.route('/process_state_change', methods=['POST'])
def process_state_change():
    # try:
    flag = request.form['flag']
    key = int(request.form['key'])
    print("pro ", flag, key)
    if flag == "true":
        new_state = user.pending_requests.get(key)
        if new_state is not None:
            new_state = json.loads(new_state)
            count = int(new_state.get('count'))
            sender_bal = int(new_state.get('sender_bal'))
            recipient_bal = int(new_state.get('recipient_bal'))
            signature = bytes.fromhex(str(new_state.get('sign'))[2:])
            if user.check_sign(count, sender_bal, recipient_bal, signature, user.opponent):
                my_signature, _bool = user.sign_new_state(count, sender_bal, recipient_bal)
                payload = {'count': count, 'sender_bal': sender_bal, 'recipient_bal': recipient_bal,
                           'signature': my_signature}
                if str(port) == str(5000):
                    to_address = "http://localhost:5001"
                else:
                    to_address = "http://localhost:5000"
                response = requests.post(f"{to_address}/state_change_response", json=payload)
                user.state.update_state(count, sender_bal, recipient_bal, signature.hex())
                print(response.status_code)
                user.remove_pending_state(key)
                print("pro ", new_state)
                return jsonify("requested state change done"), 200
            else:
                user.remove_pending_state(key)
                return jsonify("requested state change done"), 201
        else:
            print("pro new state None")
            return jsonify("requested state change done"), 400
    else:
        user.remove_pending_state(key)
        return jsonify("requested state change done"), 202
# except:
#     return jsonify(False), 201


@app.route('/transfer_bal', methods=['GET'])
def transfer_bal():
    try:
        address = request.args.get('address')
        key = request.args.get('privateKey')
        flag = User.validate_address(address, key)
        print(address, key, flag)
        return jsonify(flag), 200
    except:
        return jsonify(False), 200


@app.route('/request_state_change', methods=['POST'])
def request_state_change():
    # try:

    count = int(request.form['count'])
    sender_bal = int(request.form['sender_bal'])
    recipient_bal = int(request.form['recipient_bal'])
    # receiver_address = request.form['rec_add']

    if str(port) == str(5000):
        receiver_address = "http://localhost:5001"
        address = "http://localhost:5000"
    else:
        receiver_address = "http://localhost:5000"
        address = "http://localhost:5001"
    print(count, sender_bal, recipient_bal)
    signature, flag = user.sign_state(count, sender_bal, recipient_bal)
    print(signature, flag)
    payload = {'count': count, 'sender_bal': sender_bal, 'recipient_bal': recipient_bal,
               'sign': signature}
    response = requests.post(f"{receiver_address}/verify_state_change", json=payload)
    print(response.status_code)
    if response.status_code == 200:
        return jsonify(True), response.status_code
    else:
        return jsonify(False), response.status_code


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5002, type=int, help='port to listen on')
    parser.add_argument('-r', '--random', default="", type=str, help='key number')
    args = parser.parse_args()
    port = args.port
    temp = args.random
    config = configparser.RawConfigParser()
    config.read('channel/user.properties')

    contract_address = config.get('contract', 'contract_address')
    contract_abi = config.get('contract', 'contract_abi')
    contract_abi = json.loads(contract_abi)
    user = User(_contract_address=contract_address, _contract_abi=contract_abi)
    user.add_address("0xa5547c75b3c989a4fcd6f0456f5aa6e91e3734cf",
                     "0x1bb00ed95652a818ff64043d9f098bbd637c5c90aae597eac4ea8f9f089e7c99")

    # user.sign_new_state(1, 18000, 2000)
    app.logger.removeHandler(default_handler)
    app.run(host='0.0.0.0', port=port)
