import requests

def func1():
    f = open("channel/abi.txt", "r")
    contents = f.read()
    return contents


def func():
    string = func1()
    string = str(string).replace("\n", "")
    string = str(string).replace("	", "")
    f = open("channel/formattedABI.txt", 'w')
    f.write(string)
    f.close()


# func()
flag = False
if flag:
    payload = {'count': "2", 'sender_bal': "17000", 'recipient_bal': "3000",
               'sign': "0x133689f9b10ebe0799a6bd34ce34468c0e14151f5daa6ec0f3e4ccbc120e89ae3f81e5170b4e57fa16f9e9573ec8576d34ff11b7418a82d8a7ca8f26ab844bf11c",
               'pub_add': "0xd7b02e3bdf2eddbb5793d4728eafa83ec8c07d0b"}
    receiver_address = "http://localhost:5000"
    response = requests.post(f"{receiver_address}/sign", json=payload)
    print(response.status_code)

    # response = requests.get(f"{receiver_address}/get_pending_state")
    # print(response.content)
    # data = str(response.content).split('"')[1]
    # print(data)
    # print((response.content))
    # hey = dict()
    #
    # hey["1"] = "333"
    # hey["2"] = "(payload)"
    #
    # print(len(hey))
else:
    func()
