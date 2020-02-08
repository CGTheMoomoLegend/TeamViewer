import pyautogui


a = ['ctrl_l', 'alt_l', 'shift', 'ctrl_r', 'alt_r', 'shift_r', 'enter', 'caps_lock', 'tab', 'f1', 'f2', 'f3', 'f4',
     'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'print_screen', 'scroll_lock', 'pause', 'page_up', 'home',
     'insert', 'delete', 'end', 'page_down', 'left', 'down', 'right', 'up', 'esc']
p = [306, 308, 304, 305, 307, 303, 13, 301, 9, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 316, 302, 19,
     280, 278, 277, 127, 279, 281, 276, 274, 275, 273, 27]

GAME_TO_AUTO = {306: 'ctrl_l', 308: 'alt_l', 304: 'shift', 305: 'ctrl_r', 307: 'alt_r', 303: 'shift_r', 13: 'enter',
                301: 'caps_lock', 9: 'tab', 282: 'f1', 283: 'f2', 284: 'f3', 285: 'f4', 286: 'f5', 287: 'f6', 288: 'f7',
                289: 'f8', 290: 'f9', 291: 'f10', 292: 'f11', 293: 'f12', 316: 'print_screen', 302: 'scroll_lock',
                19: 'pause', 280: 'page_up', 278: 'home', 277: 'insert', 127: 'delete', 279: 'end', 281: 'page_down',
                276: 'left', 274: 'down', 275: 'right', 273: 'up', 27: 'esc'}

pyautogui.keyDown('shift')
pyautogui.keyDown('a')
A