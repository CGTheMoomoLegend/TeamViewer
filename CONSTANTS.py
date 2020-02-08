# screen related

MONITOR_NUMBER = 1
WIDTH = 1920
HEIGHT = 1080
SCREEN_SIZE = (WIDTH, HEIGHT)
GUI_X = 500
GUI_Y = 500
GUI_SIZE = (GUI_X, GUI_Y)

# image related

COMPRESSION_LEVEL = 6
CHUNK_COUNT = 8

# socket related

DATA_PORT = 3595
INPUT_PORT = 3596
PENDING_PORT = 3597
MAX_CLIENTS = 5
MSG_LEN_SIZE = 8
ACCEPT_ALL_IP = "0.0.0.0"
TIMEOUT = 10
EXIT_FLAG_MESSAGE = "SHUTDOWN_SERVER"
CONTROLLED_INDEX = 0
CONTROLLER_INDEX = 1
SERVER_IP = 'localhost'

# input related

MOUSE_MAP = {1: 2, 2: 32, 3: 8, 4: 0, 5: 0}
MOUSE_SCROLL_CLICKS_STD = 200

# pygame related

TICK_RATE = 60

# code related

FIRST_INDEX = 0
LAST_INDEX = -1

GAME_TO_AUTO = {306: 'ctrlleft', 308: 'altleft', 304: 'shift', 305: 'ctrlright', 307: 'altright', 303: 'shiftright', 13: 'enter',
                301: 'capslock', 9: 'tab', 282: 'f1', 283: 'f2', 284: 'f3', 285: 'f4', 286: 'f5', 287: 'f6', 288: 'f7',
                289: 'f8', 290: 'f9', 291: 'f10', 292: 'f11', 293: 'f12', 316: 'printscreen', 302: 'scrolllock',
                19: 'pause', 280: 'pageup', 278: 'home', 277: 'insert', 127: 'delete', 279: 'end', 281: 'pagedown',
                276: 'left', 274: 'down', 275: 'right', 273: 'up', 27: 'esc'}
