import ctypes
import sys
from time import sleep

import Server
from sockets_wrappers import *


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def main(data_sock: client_socket,
         input_sock: client_socket):
    if is_admin():
        # Code of your program here
        # info_sock = client_socket(SERVER_IP, 1234)
        # msg = "controlled" + ':False'
        # print(msg)
        # info_sock.send(msg)
        # info_sock.close()
        server = Server.Server(data_sock[0], input_sock[0])
        try:
            while 'recording':
                # getting, sending screenshot
                server.send_screenshot()

                sleep(0.100)
        except Exception as e:
            print(e)
            quit()
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)


if __name__ == '__main__':
    main()
