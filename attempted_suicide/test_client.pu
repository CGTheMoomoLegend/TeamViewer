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
    x = threading.Thread(target=constantReceive, args=(input_sock, ))
    x.start()
    while True:
        data_sock.send("FAKE DATA")


if __name__ == '__main__':
    main()