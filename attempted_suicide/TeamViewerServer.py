import threading
import select
import time
from CONSTANTS import *
from sockets_wrappers import *

dataSocket = server_socket(ACCEPT_ALL_IP, DATA_PORT, TIMEOUT)
inputSocket = server_socket(ACCEPT_ALL_IP, INPUT_PORT, TIMEOUT)
exitFlag = False
dataSocks = []
inputSocks = []

class Client(object):
    def __init__(self, dataSock: client_socket, inputSock: client_socket, isReceiver):
        self.dataSock = dataSock
        self.inputSock = inputSock
        self.isReceiver = isReceiver

rooms = []
num_of_rooms = 0

def listenForClients():
    global exitFlag, num_of_rooms
    while not exitFlag:
        try:
            newClientData = dataSocket.accept()
            newClientInput = inputSocket.accept()
            print("NEW CONNECTION YEET")
            dataSocks.append(newClientData)
            inputSocks.append(newClientInput)
            print(" number of room: " + str(num_of_rooms))
            if not rooms or not rooms[num_of_rooms]:
                # got new sharer client
                rooms.append([Client(newClientData, newClientInput, False)])
                print("adding new sharer to room number: " + str(num_of_rooms))
            else:
                rooms[num_of_rooms].append(Client(newClientData, newClientInput, True))
                print("adding receiver to room number: " + str(num_of_rooms))
                sharer = rooms[num_of_rooms][SHARER_INDEX]
                receiver = rooms[num_of_rooms][RECEIVER_INDEX]
                sharer_thread = threading.Thread(target=handle_client, args=(sharer, receiver))
                receiver_thread = threading.Thread(target=handle_client, args=(receiver, sharer))
                sharer_thread.start()
                receiver_thread.start()
                num_of_rooms += 1
        except socket.timeout:
            continue
        except IndexError as e:
            print(e)
            continue


def handle_client(c: Client, o: Client):
    global exitFlag
    if c.isReceiver:
        # loop on input and broadcast
        while not exitFlag:
            buf = c.inputSock.receive()
            o.inputSock.send(buf)
    else:
        # loop on data and broadcast
        while not exitFlag:
            buf = c.dataSock.receive()
            o.dataSock.send(buf)


def main():
    # listen = threading.Thread(target=listenForClients)
    # listen.start()
    listenForClients()

    map(lambda x: x.close(), dataSocks)
    map(lambda x: x.close(), inputSocks)
    dataSocket.close()
    inputSocket.close()


if __name__ == "__main__":
    main()
