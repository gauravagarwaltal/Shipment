#!/usr/bin/env python3
import socket
import threading


def handle_connection(connection):
    with connection:
        flag = True
        while flag:
            data = connection.recv(1024)
            if str(data).lower().strip() == 'bye':
                flag = False
            if not data:
                break
            connection.sendall(data)


def server(host=None, port=None):
    if host is None:
        host = '127.0.0.1'  # Standard loopback interface address (localhost)
    if port is None:
        port = 5000  # Port to listen on (non-privileged ports are > 1023)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            print('Connected by', addr)
            threading.Thread(target=handle_connection, args={conn}).start()


server()