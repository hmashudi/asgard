#!/usr/bin/env python3

from socket import *


def client_program():
    host = socket.gethostname()
    port = 5000

    client_socket = socket()
    client_socket.connect((host, port))

    message = input(" -> ")

    while message.lower().strip() != 'quit':
        client_socket.send(message.encode())
        message = input(" -> ")

    client_socket.close()


if __name__ == '__main__':
    client_program()
