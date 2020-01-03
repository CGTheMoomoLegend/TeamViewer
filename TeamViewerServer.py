import threading
import select
import time
from CONSTANTS import *
from sockets_wrappers import *
import json

input_socket = server_socket(ACCEPT_ALL_IP, INPUT_PORT, TIMEOUT)
data_socket = server_socket(ACCEPT_ALL_IP, DATA_PORT, TIMEOUT)
info_socket = server_socket(ACCEPT_ALL_IP, 1234, TIMEOUT)
exitFlag = False
dataSocks = []
inputSocks = []

class Client(object):
    def __init__(self,dataSock : client_socket, inputSock: client_socket, info_sock : client_socket ,isCtrl, roomNumber, username):
        self.dataSock = dataSock
        self.inputSock = inputSock
        self.info_sock = info_sock
        self.isCtrl = isCtrl
        self.roomNumber = roomNumber
        self.username = username

user_dict = {}
rooms = []
num_of_rooms = 0


def listenForClients():
    global exitFlag, num_of_rooms
    while not exitFlag:
        try:
            newClientInfo = info_socket.accept()
            newClientData = data_socket.accept()
            newClientInput = input_socket.accept()
            dataSocks.append(newClientData)
            inputSocks.append(newClientInput)
            print("NEW CONNECTION")
            print ("trying to receive")
            first_msg = newClientInfo.receive()
            print (first_msg)
            username, isCtrl = to_str(first_msg).split(':')
            print (username, isCtrl)
            isCtrl = isCtrl in ("True")
            if not isCtrl:
                rooms.append([Client(newClientData, newClientInput, newClientInfo, False, num_of_rooms, username)])
                print("adding new sharer to room number: " + username + ' : ' + str(num_of_rooms + 1))
                newClientInfo.close()
                print("closing info sock")

            else:
                send_rooms(newClientInfo)
                room_number = to_str(newClientInfo.receive())
                room_number = int(room_number)
                print(room_number)
                if room_number < -1 or room_number > -1:
                    rooms[room_number].append(Client(newClientData, newClientInput, newClientInfo, True, room_number, username))
                    print("adding receiver to room number: " + str(num_of_rooms))
                    sharer = rooms[room_number][SHARER_INDEX]
                    receiver = rooms[room_number][RECEIVER_INDEX]
                    newClientInfo.close()
                    print("closing info sock")
                    print("starting sharer thread")
                    sharer_thread = threading.Thread(target=handle_client, args=(sharer, receiver))
                    print("starting receiver thread")
                    receiver_thread = threading.Thread(target=handle_client, args=(receiver, sharer))
                    sharer_thread.start()
                    receiver_thread.start()
                    num_of_rooms += 1
                else:
                    continue

        except socket.timeout:
            continue
        except Exception as e:
            print (e.with_traceback())
            continue


def send_rooms(s: client_socket):
    global user_dict
    for room in rooms:
        if len(room) == 1:
            dict = {room[0].roomNumber : room[0].username}
            user_dict.update(dict)

    print(user_dict)
    json_dict = json.dumps(user_dict)
    s.send(json_dict)
    return


def bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result


def handle_client(c: Client, o: Client):
    global exitFlag

    if c.isCtrl:
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

    listenForClients()

    map(lambda x: x.close(), dataSocks)
    map(lambda x: x.close(), inputSocks)


if __name__ == "__main__":
    main()
