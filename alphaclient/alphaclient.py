#!/usr/bin/env python3

import socket
import tailer

def client_program():
    host = '172.17.0.2'
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))
    hostname = socket.gethostname()

    init_attempt = 0
    for line in tailer.follow(open('/var/log/sshd.log')):
        if 'password' in line:
            login_attempt = init_attempt + 1
            message = (str(hostname) + " had " + str(login_attempt) + " attempt of ssh session")
            client_socket.send(message.encode())
            init_attempt = login_attempt

    client_socket.close()


if __name__ == '__main__':
    client_program()
