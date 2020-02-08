import _thread

import pyautogui
import win32api

from CONSTANTS import *
from image_encoding import get_screenshot, compress_screenshot
from sockets_wrappers import *


class Server:
    def __init__(self, data_sock: client_socket, input_sock: client_socket):
        self.ports = {'data': DATA_PORT, 'input': INPUT_PORT}
        self.data_socket = data_sock
        self.input_socket = input_sock
        self.input_thread = _thread.start_new_thread(self.__input__loop, ())

    def send_screenshot(self):
        ss = get_screenshot()
        # print("About to try and send screenshot on data_socket")
        self.data_socket.send(compress_screenshot(ss))

    def handle_keyboard_down(self, key):
        key = chr(int(key))
        pyautogui.keyDown(key)

    def handle_keyboard_up(self, key):
        key = chr(int(key))
        pyautogui.keyUp(key)

    def handle_mouse_btn_msg(self, key, is_down):
        if int(key) not in MOUSE_MAP.keys():
            return
        if int(key) == 4 or key == 5:
            self.handle_mouse_scroll(int(key) == 4)
            return
        mouse_event_val = MOUSE_MAP[int(key)]
        if not is_down:
            mouse_event_val *= 2
        mouse_x, mouse_y = win32api.GetCursorPos()
        win32api.mouse_event(mouse_event_val, mouse_x, mouse_y, 0, 0)

    def handle_mouse_mov_msg(self, pos_x, pos_y):
        print('pos: (', pos_x, ',', pos_y, ')')
        win32api.SetCursorPos((int(pos_x), int(pos_y)))

    def handle_mouse_scroll(self, prefix):
        if prefix:
            pyautogui.scroll(MOUSE_SCROLL_CLICKS_STD)
        else:
            pyautogui.scroll(-MOUSE_SCROLL_CLICKS_STD)

    def __input__loop(self):
        # print('input loop started')
        print(self.input_socket)
        while 'listening':
            msg = self.input_socket.receive().decode('ascii').split(':')

            prefix = msg[0]
            print("Received prefix: " + prefix)
            #     print('prefix:', prefix)
            if prefix == "kd":
                self.handle_keyboard_down(msg[1])
            elif prefix == "ku":
                self.handle_keyboard_up(msg[1])
            elif prefix == "md" or prefix == "mu":
                self.handle_mouse_btn_msg(msg[1], prefix == "md")
            elif prefix == "mm":
                self.handle_mouse_mov_msg(msg[1], msg[2])



