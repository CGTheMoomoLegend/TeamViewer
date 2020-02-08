import threading

import pygame
from pynput.keyboard import Listener

from CONSTANTS import *

fix_dict = []

last_auto_press = ''


def pygame_init_display(screen_size):
    pygame.init()
    pygame.display.set_caption("TeamViewer")
    return pygame.display.set_mode(screen_size)


def pygame_init_clock(tick_count):
    clock = pygame.time.Clock()
    clock.tick(tick_count)
    return clock


def pygame_display_loop(client, screen):
    while True:
        screen.blit(client.receive_image(), (0, 0))
        pygame.display.update()


def on_press(key):
    global last_auto_press
    last_auto_press = key
    print("auto: " + str(key))


def do_stuff():
    with Listener(on_press=on_press) as listener:
        listener.join()


def do_stuff_2():
    global fix_dict
    done = False
    i = 0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                fix_dict.append(event.key)
                i += 1
                print("game:" + str(event.key))


def main():
    # creating pygame, screen, clock
    screen = pygame_init_display((300, 300))
    clock = pygame_init_clock(TICK_RATE)
    do_stuff_2()
    print("dict:" + str(fix_dict))


if __name__ == '__main__':
    main()
