import pygame
import Client
import _thread
from CONSTANTS import TICK_RATE, SCREEN_SIZE

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

def main():
    # creating pygame, screen, clock
    screen = pygame_init_display(SCREEN_SIZE)
    clock = pygame_init_clock(TICK_RATE)
    # creating client
    client = Client.Client('localhost')
    try:

        thread = _thread.start_new_thread(pygame_display_loop, (client, screen))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    client.send_kb_msg(event.key, event.type == pygame.KEYDOWN)
                elif event.type == pygame.MOUSEMOTION:
                    client.send_mouse_loc_msg(pygame.mouse.get_pos())
                elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    client.send_mouse_btn_msg(event.button, event.type == pygame.MOUSEBUTTONDOWN)



    finally:
        pass


if __name__ == '__main__':
    main()
