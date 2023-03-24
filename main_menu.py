import pygame
import pygame_menu
import one_player_snake
import two_player_snake

def main_menu(screen, window_x, window_y):
    def single_player():
        one_player_snake.onep_snake(screen, window_x, window_y)

    def multiplayer():
        two_player_snake.twop_snake(screen, window_x, window_y)

    menu_surface = pygame.surface((400, 300))

    menu = pygame_menu.Menu('Snek', 400, 300, theme=pygame_menu.themes.THEME_SOLARIZED)
    menu.add.button('One player', single_player)
    menu.add.button('Two Player', multiplayer)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)