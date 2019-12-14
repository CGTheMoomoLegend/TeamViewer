# -*- coding: utf-8 -*-
from sockets_wrappers import *
from CONSTANTS import *
import threading

def constantReceive(s):
    while True:
        print(s.receive())

def main():
    data_sock = client_socket("localhost", DATA_PORT)
    input_sock = client_socket("localhost", INPUT_PORT)
    x = threading.Thread(target=constantReceive, args=(data_sock, ))
    x.start()
    while True:
        input_sock.send("FAKE INPUT DATA")


if __name__ == '__main__':
    main()