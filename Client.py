from sockets_wrappers import client_socket
from pygame import image
from zlib import decompress
from CONSTANTS import  DATA_PORT, INPUT_PORT, SCREEN_SIZE


class Client:
    def __init__(self, ip, data_port=DATA_PORT, input_port=INPUT_PORT):
        self.ports = {'data': data_port, 'input': input_port}
        self.data_socket = client_socket(ip, data_port)
        self.input_socket = client_socket(ip, input_port)

    def receive_image(self):
        pixels = self.data_socket.receive()
        print(pixels, "\r\n", "len =" ,len(pixels), "\r\n")
        for pixel in pixels:
            if pixel == '\\':
                print("YES!!!!")
        pixels = decompress(pixels)
        return image.frombuffer(pixels, SCREEN_SIZE, 'RGB')

    def send_input_msg(self, prefix, *args):
        msg = prefix + ':'
        # split arguments by colon mark
        for arg in args:
            msg += str(arg) + ':'
        # remove last colon mark
        msg = msg[:-1]
        self.input_socket.send(msg)

    def send_kb_msg(self, key, is_down):
        # kd --> key down
        # ku --> key up
        if is_down:
            self.send_input_msg("kd", key)
        else:
            self.send_input_msg("ku", key)

    def send_mouse_loc_msg(self, pos):
        # mm --> mouse move
        self.send_input_msg("mm", pos[0], pos[1])

    def send_mouse_btn_msg(self, button, is_down):
        if is_down:
            self.send_input_msg("md", button)
        else:
            self.send_input_msg("mu", button)
