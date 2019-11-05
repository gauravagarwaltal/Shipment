let payload = { 'channel_id': "channel_id", 'count': 1, 'Alice_Cash': 11, 'Bob_Cash': 12, 'signature': '0xd0237288eb37f958c75ff28f7e111e983a91b31a6b13ddd28d318fb0bb1d77d4', }

console.log(JSON.stringify(payload))

let jsonify = { "channel_id": "channel_id", "count": 1, "Alice_Cash": 11, "Bob_Cash": 12, "signature": "0xd0237288eb37f958c75ff28f7e111e983a91b31a6b13ddd28d318fb0bb1d77d4", }

// jsonify = JSON.parse(jsonify)
console.log(jsonify.count)