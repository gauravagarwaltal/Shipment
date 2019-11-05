import socket
import threading

import redis
from web3.auto import w3


class RedisHandler:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.redis_pub_sub = redis.StrictRedis(host='localhost', port=6379)
        self.subscription_flag = dict()
        # ( chanel_id + address => connection_object) socket_mapping
        # self.socket_mapping = dict()
        self.socket_server = None
        # self.server()

    def server(self, host=None, port=None):
        if host is None:
            host = '127.0.0.1'  # Standard loopback interface address (localhost)
        if port is None:
            port = 5000  # Port to listen on (non-privileged ports are > 1023)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.socket_server:
            self.socket_server.bind((host, port))
            self.socket_server.listen(5)
            while True:
                conn, addr = self.socket_server.accept()
                print('Connected by', addr)
                threading.Thread(target=self.handle_connection, args={conn}).start()

    def handle_connection(self, connection):
        with connection:
            flag = True
            while flag:
                data = connection.recv(1024)
                if str(data).lower().strip() == 'bye':
                    flag = False
                if not data:
                    break
                connection.sendall(data)

    def set_value(self, key, value):
        """
        This function simply set or override key-value pair in redis database and will return True in case of success.
        :param key:
        :param value:
        :return: True or False
        """
        return self.redis_client.set(key, value)

    def get_value(self, key):
        """
        This function returns previously mapping value to key or null
        :param key:
        :return: value or null
        """
        return self.redis_client.get(key)

    def remove_list_value(self, key):
        """
        This function will remove key-value pair from redis
        :param key:
        :return:
        """
        return self.redis_client.lpop(key)

    def set_list_value(self, address, request_type, request_content):
        """
        This function will add given content to a key which is created by given information
        this will add current content in either empty list or in old list if existed.
        It will return index number of given content.
        :param address:         Ethereum public address
        :param request_type:    pending_request_type or response_type
        :param request_content: state_update_data
        :return:                index_value or null
        """
        address = w3.toChecksumAddress(address)
        key = str(address) + str(request_type)
        return self.redis_client.rpush(key, request_content)

    def get_list_value(self, address, request_type):
        """
        This will fetch existed list using given details.
        :param address:         Ethereum public address
        :param request_type:    pending_request_type or response_type
        :return:                state_update_data
        """
        address = w3.toChecksumAddress(address)
        key = str(address) + str(request_type)
        return self.redis_client.lrange(key, 0, -1)

    def update_list_value(self, address, request_type, index, request_content):
        """
        This will update existed value with new given value in the list.
        :param address:         Ethereum public address
        :param request_type:    pending_request_type or response_type
        :param index:           state index in list
        :param request_content: state_update_data
        :return:                True or False
        """
        address = w3.toChecksumAddress(address)
        key = str(address) + str(request_type)
        return self.redis_client.lset(key, index, request_content)

    def delete_list_value(self, address, request_type, index, operation_type=None):
        """
        This will delete list item using index number
        :param address:         Ethereum public address
        :param request_type:    pending_request_type or response_type
        :param index:           state index in existed list
        :param operation_type:  delete operation type ( 0: all occurrence of value, 1: head to tail, -1: tail to head)
        :return:                In case of success index value or in case of failure -1
        """
        address = w3.toChecksumAddress(address)
        if operation_type is None:
            operation_type = 0
        key = str(address) + str(request_type)
        request_content = self.redis_client.lindex(key, index)
        if request_content is not None:
            print("the index value ", request_content)
            return self.redis_client.lrem(key, operation_type, request_content)
        return -1

    def publish_data(self, channel_id, address, data):
        # address = w3.toChecksumAddress(address)
        channel = str(channel_id) + str(address)
        print(channel)
        return self.redis_pub_sub.publish(channel, data)

    def subscribe_data(self, channel):
        pub_sub_object = self.redis_pub_sub.pubsub()
        pub_sub_object.subscribe(channel)
        print("Listening ", channel)
        while self.subscription_flag.get(channel):
            data = pub_sub_object.get_message()
            if data:
                print(channel, data)
        pub_sub_object.unsubscribe(channel)
        print("Listening closed ", channel)

    def subscribe_channel(self, channel_id, address):
        address = w3.toChecksumAddress(address)
        channel = str(channel_id) + str(address)
        self.subscription_flag[channel] = True
        print("subscribe ", channel)
        threading.Thread(target=self.subscribe_data, args={channel}).start()
        return 200

    def unsubscribe_channel(self, channel_id, address):
        address = w3.toChecksumAddress(address)
        channel = str(channel_id) + str(address)
        print("unsubscribe ", channel)
        self.redis_pub_sub.pubsub_numsub(channel)
        self.subscription_flag[channel] = False

        return 200

# redis_handler = RedisHandler()
# redis_handler.publish_data("agarwal", "",
#                            "{'channel_id': channel_id, 'count': 1, 'Alice_Cash': 11, 'Bob_Cash': 12, "
#                            "'signature': '0xd0237288eb37f958c75ff28f7e111e983a91b31a6b13ddd28d318fb0bb1d77d4', }")
