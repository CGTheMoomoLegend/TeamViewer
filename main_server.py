from zlib import compress
from mss import mss, tools
import Server
from time import sleep
import ctypes, sys
from sockets_wrappers import *
import image_encoding
from CONSTANTS import *


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False




def main(data_sock : client_socket = client_socket(SERVER_IP, DATA_PORT), input_sock : client_socket = client_socket(SERVER_IP, INPUT_PORT)):
    if is_admin():
        # Code of your program here
        server = Server.Server(data_sock, input_sock)
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

