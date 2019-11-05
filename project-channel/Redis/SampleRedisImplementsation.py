import json

from web3.auto import w3

from Redis.RedisHandler import RedisHandler

redis_handler = RedisHandler()
# channel_id = 1212
# address = "0x52b112ceeDc6a020ff755bb2be68796cd45bae3e"
# address = w3.toChecksumAddress(address)
#
# request_type = "request"
# payload = {'channel_id': channel_id,
#            'count': 1,
#            'Alice_Cash': 11,
#            'Bob_Cash': 12,
#            'signature': "0xd0237288eb37f958c75ff28f7e111e983a91b31a6b13ddd28d318fb0bb1d77d4", }
# jsonify_payload = json.dumps(payload)

# flag = redis_handler.set_list_value(channel_id, address, request_type, jsonify_payload)

# fetched_list = redis_handler.get_list_value(channel_id, address, request_type)
# print("fetched data ", len(fetched_list))
# print("delete return ", redis_handler.delete_list_value(channel_id, address, request_type, 1))
fetched_list = redis_handler.get_list_value(1, "0x19DbcfB1E970EB0ac300936824de350EE248e803", 1)
print("fetched data ", fetched_list)
for each in fetched_list:
    print(each.decode("utf-8") )

# print("publish data ", redis_handler.set_value("hello", jsonify_payload))

# print("subscribe data", redis_handler.subscribe_data("channel_1"))
if False:
    redis_handler.subscribe_data("channel_1")
