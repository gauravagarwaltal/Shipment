#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:09:35 2019

@author: gaurava
"""
# from flask_cors import CORS
from uuid import uuid4

from flask import Flask, request, jsonify

from Redis.RedisHandler import RedisHandler

# os.system("clear")

# Instantiate the Node
app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')
redis_handler = RedisHandler()
'''
fetch_request
set_request
update_request
delete_request
'''


@app.route('/fetch_request', methods=['POST'])
def fetch_request():
    # _channel_id = request.form['channel_id']
    _address = request.form['address']
    _request_type = request.form['request_type']
    # fetched_request = redis_handler.get_list_value(_channel_id, _address, _request_type)
    fetched_request = redis_handler.get_list_value(_address, _request_type)
    str_requests = []
    for each in fetched_request:
        str_requests.append(each.decode("utf-8"))
    # payload = {'requests': fetched_request}
    print(str_requests)
    return jsonify(str_requests), 200


@app.route('/set_request', methods=['POST'])
def set_request():
    # _channel_id = request.form['channel_id']
    _address = request.form['address']
    _request_type = request.form['request_type']
    _request_data = request.form['request_data']
    # index = redis_handler.set_list_value(_channel_id, _address, _request_type, _request_data)
    index = redis_handler.set_list_value(_address, _request_type, _request_data)
    payload = {'index': index}
    return jsonify(payload), 200


@app.route('/update_request', methods=['POST'])
def update_request():
    # _channel_id = request.form['channel_id']
    _address = request.form['address']
    _request_type = request.form['request_type']
    _index = request.form['index']
    _request_data = request.form['request_data']
    # index = redis_handler.update_list_value(_channel_id, _address, _request_type, _index, _request_data)
    index = redis_handler.update_list_value(_address, _request_type, _index, _request_data)
    payload = {'index': index}
    return jsonify(payload), 200


@app.route('/delete_request', methods=['POST'])
def delete_request():
    # _channel_id = request.form['channel_id']
    _address = request.form['address']
    _request_type = request.form['request_type']
    _index = request.form['index']
    # index = redis_handler.delete_list_value(_channel_id, _address, _request_type, _index)
    index = redis_handler.delete_list_value(_address, _request_type, _index)
    payload = {'index': index}
    return jsonify(payload), 200


@app.route('/publish', methods=['POST'])
def publish():
    # _channel_id = request.form['channel_id']
    _address = request.form['address']
    _request_data = request.form['request_data']
    # index = redis_handler.publish_data(_channel_id, _address, _request_data)
    index = redis_handler.publish_data(_address, _request_data)
    payload = {'index': index}
    return jsonify(payload), 200


@app.route('/subscribe', methods=['POST'])
def subscribe():
    # _channel_id = request.form['channel_id']
    _address = request.form['address']
    # index = redis_handler.subscribe_channel(_channel_id, _address)
    index = redis_handler.subscribe_channel(_address)
    payload = {'index': index}
    return jsonify(payload), 200


@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    # _channel_id = request.form['channel_id']
    _address = request.form['address']
    # index = redis_handler.unsubscribe_channel(_channel_id, _address)
    index = redis_handler.unsubscribe_channel(_address)
    payload = {'index': index}
    return jsonify(payload), 200


@app.route('/', methods=['POST'])
def check_point():
    payload = {'index': "index"}
    return jsonify(payload), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5002, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app.run(host='0.0.0.0', port=port)
