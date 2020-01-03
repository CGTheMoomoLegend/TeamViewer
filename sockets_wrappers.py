import socket

from CONSTANTS import MSG_LEN_SIZE, MAX_CLIENTS


# general utilities
def to_str(msg):
    if isinstance(msg, bytes):
        return msg.decode(encoding="ascii")
    return str(msg)


def to_bytes(text):
    if isinstance(text, str):
        return bytes(text, encoding="ascii")
    # only if type is already bytes
    return text


def get_len_str(msg: str):
    hex_str = hex(len(msg)).replace("0x", "")
    hex_str = ((MSG_LEN_SIZE - len(hex_str)) * '0') + hex_str
    return to_bytes(hex_str)


def get_socket_bytes(msg: str):
    return get_len_str(msg) + to_bytes(msg)


class client_socket:
    def __init__(self, ip=None, port=None, sockNumber=-1):
        self.ip = ip
        self.port = port
        if ip is None and port is None:
            self.socket = sockNumber
        else:
            # create client socket
            print('creating client socket')
            self.socket = socket.socket()
            # connect to server
            print('connecting to server')
            self.socket.connect((ip, port))
            print('connected to server')

    def __eq__(self, other):
        return self.fileno() == other.fileno()

    def send(self, msg: str):
        self.socket.send(get_socket_bytes(msg))

    def receive(self):
        msg_len = int(to_str(self.socket.recv(MSG_LEN_SIZE)), 16)
        msg = b""
        while len(msg) < msg_len:
            msg += self.socket.recv(msg_len - len(msg))
        return msg

    def fileno(self):
        return self.socket.fileno()

    def close(self):
        self.socket.close()


class server_socket:
    def __init__(self, ip, port, timeout):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        # create, bind socket
        print('creating server socket')
        self.server_socket = socket.socket()
        self.server_socket.bind((ip, port))
        self.server_socket.settimeout(timeout)
        print('binding server socket')
        self.server_socket.listen(MAX_CLIENTS)
        print("listening for clients")

    def accept(self):
        newSock, _ = self.server_socket.accept()
        # newSock.settimeout(self.timeout)
        return client_socket(sockNumber=newSock)

    def fileno(self):
        return self.server_socket.fileno()

    def close(self):
        self.server_socket.close()
