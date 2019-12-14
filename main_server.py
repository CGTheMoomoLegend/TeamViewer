from zlib import compress
from mss import mss, tools
import sockets_wrappers
import Server
from time import sleep
import ctypes, sys
import image_encoding

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False




def main():
    if is_admin():
        # Code of your program here
        server = Server.Server()
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
