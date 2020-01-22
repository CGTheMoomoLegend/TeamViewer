import _thread

import pygame

import Client
from CONSTANTS import *
from sockets_wrappers import *


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


def main(data_sock: client_socket, input_sock: client_socket):
    # creating pygame, screen, clock
    screen = pygame_init_display(SCREEN_SIZE)
    clock = pygame_init_clock(TICK_RATE)
    # creating client
    # info_sock = client_socket(SERVER_IP, 1234)
    # msg = "controller" + ':True'
    # print(msg)
    # info_sock.send(msg)
    # print(info_sock.receive())
    # info_sock.send("0")
    # info_sock.close()
    client = Client.Client(data_sock[0], input_sock[0])
    try:

        thread = _thread.start_new_thread(pygame_display_loop, (client, screen))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    client.send_close_msg()
                    return
                elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    print(event.type == pygame.KEYDOWN)
                    client.send_kb_msg(event.key, event.type == pygame.KEYDOWN)
                elif event.type == pygame.MOUSEMOTION:
                    client.send_mouse_loc_msg(pygame.mouse.get_pos())
                elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    client.send_mouse_btn_msg(event.button, event.type == pygame.MOUSEBUTTONDOWN)

    except Exception:
        pass

    finally:
        pass


if __name__ == '__main__':
    main()
