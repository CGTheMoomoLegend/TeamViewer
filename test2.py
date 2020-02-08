from pynput.keyboard import Listener

the_list = []


def on_press(key):
    global last_auto_press
    last_auto_press = key
    print("auto: " + str(key))
    the_list.append(str(key)[4:])
    if str(key) == "Key.esc":
        print(the_list)
        exit(0)


def do_stuff():
    with Listener(on_press=on_press) as listener:
        listener.join()


do_stuff()
