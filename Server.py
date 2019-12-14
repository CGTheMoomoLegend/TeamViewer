import pyautogui
import _thread
from sockets_wrappers import *
import win32api
from CONSTANTS import MOUSE_MAP, DATA_PORT, INPUT_PORT
from image_encoding import get_screenshot, compress_screenshot

class Server:
    def __init__(self, ip='localhost', data_port=DATA_PORT, input_port=INPUT_PORT):
        self.ports = {'data': data_port, 'input': input_port}
        self.data_socket = client_socket(ip, data_port)
        self.input_socket = client_socket(ip, input_port)
        self.input_thread = _thread.start_new_thread(self.__input__loop, ())

    def send_screenshot(self):
        ss = get_screenshot()
        print("About to try and send screenshot on data_socket")
        self.data_socket.send(compress_screenshot(ss))

    def handle_keyboard_msg(self, key, is_down):
        key = chr(int(key))
        #  print('handling keyboard message:', key)
        if is_down:
            pyautogui.keyDown(key)
        else:
            pyautogui.keyUp(key)

    def handle_mouse_btn_msg(self, key, is_down):
        if int(key) not in MOUSE_MAP.keys():
            return
        mouse_event_val = MOUSE_MAP[int(key)]
        if not is_down:
            mouse_event_val *= 2
        mouse_x, mouse_y = win32api.GetCursorPos()
        win32api.mouse_event(mouse_event_val, mouse_x, mouse_y, 0, 0)

    def handle_mouse_mov_msg(self, pos_x, pos_y):
        print('pos: (', pos_x, ',', pos_y, ')')
        win32api.SetCursorPos((int(pos_x), int(pos_y)))

    def __input__loop(self):
        # print('input loop started')
        while 'listening':
            msg = self.input_socket.receive().decode('ascii').split(':')
            prefix = msg[0]
            #     print('prefix:', prefix)
            if prefix == "kd" or prefix == "ku":
                self.handle_keyboard_msg(msg[1], prefix == "kd")
            elif prefix == "md" or prefix == "mu":
                self.handle_mouse_btn_msg(msg[1], prefix == "md")
            elif prefix == "mm":
                self.handle_mouse_mov_msg(msg[1], msg[2])
