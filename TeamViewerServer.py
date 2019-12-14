import threading
import select
from CONSTANTS import *
from sockets_wrappers import *

dataSocket = server_socket(ACCEPT_ALL_IP, DATA_PORT, TIMEOUT)
inputSocket = server_socket(ACCEPT_ALL_IP, INPUT_PORT, TIMEOUT)
exitFlag = False
dataSocks = []
inputSocks = []


def listenForClients(sock, l):
    global exitFlag
    while not exitFlag:
        try:
            newClientData = sock.accept()
            print("new connection sock#" + str(newClientData.fileno()))
            l.append(newClientData)
            print("current data socks:")
            print([str(x.fileno()) + ", " for x in dataSocks])
            print("current input socks:")
            print([str(x.fileno()) + ", " for x in inputSocks])
        except socket.timeout:
            continue


def broadcastToClients(data: str, sockList, ignoreSock):
    if data is None:
        return
    for s in sockList:
        if s.fileno() == ignoreSock.fileno():
            continue
        s.send(data)


def handleSockList(l, isdata):
    global exitFlag
    while not exitFlag:
        dataBuf = None
        output = []
        try:
            if isdata and not l:
                s = l[1]
            elf:
                s = l[-1]
            dataBuf = s.receive()
            # print("received data on sock#" + str(s.fileno()))
            # print("data is " + str(dataBuf[:10]))
            broadcastToClients(dataBuf, l, s)
        except socket.error:
            print("sock#" + str(s.fileno()) + " got fucked, closing")
            s.close()
            l = list(filter(lambda item: item != s, l))


def main():
    listen1 = threading.Thread(target=listenForClients, args=(inputSocket, inputSocks, ))
    listen1.start()
    listen2 = threading.Thread(target=listenForClients, args=(dataSocket, dataSocks, ))
    listen2.start()
    dataSocksThread = threading.Thread(target=handleSockList, args=(dataSocks, True, ))
    dataSocksThread.start()
    handleSockList(inputSocks, False)
    inputSocksThread = threading.Thread(target=handleSockList, args=(inputSocks, False,  ))
    inputSocksThread.start()
    map(lambda x: x.close(), dataSocks)
    map(lambda x: x.close(), inputSocks)
    dataSocket.close()
    inputSocket.close()


if __name__ == "__main__":
    main()
