#!/usr/bin/env python3

from socket import *


def server_program():
    host = '0.0.0.0'
    port = 5000

    server_socket = socket()
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind((host, port))

    # configure how many client the server can listen simultaneously
    server_socket.listen(5)
    conn, address = server_socket.accept()
    print("Received Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            break

        print(str(data))

    conn.close()


if __name__ == '__main__':
    server_program()
