import threading

from sockets_wrappers import *


def server():
    s = server_socket("0.0.0.0", 4040, 1)
    c = s.accept()
    print("received on server: " + str(c.receive()))


def client():
    c = client_socket("127.0.0.1", 4040)
    c.send("asdasdljkhaslkjdhaslkjdhaslkjdhalksjhdlkj")


x = threading.Thread(target=server)
x.start()

client()
