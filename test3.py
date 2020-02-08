a = ['ctrl_l', 'alt_l', 'shift', 'ctrl_r', 'alt_r', 'shift_r', 'enter', 'caps_lock', 'tab', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'print_screen', 'scroll_lock', 'pause', 'page_up', 'home', 'insert', 'delete', 'end', 'page_down', 'left', 'down', 'right', 'up', 'esc']
p = [306, 308, 304, 305, 307, 303, 13, 301, 9, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 316, 302, 19, 280, 278, 277, 127, 279, 281, 276, 274, 275, 273, 27]
dict = {}
for item, item2 in zip(p, a):
    dict[item] = item2

print(dict)