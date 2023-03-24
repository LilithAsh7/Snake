import pygame
import pygame_menu
import one_player_snake
import two_player_snake

# Size of the window
window_x = 720
window_y = 480

# Defining colors that will be used later
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
pink = pygame.Color(250, 147, 241)

pygame.init()  # Initializing the game window
screen = pygame.display.set_mode((window_x, window_y), pygame.NOFRAME)  # Creating the game window using the x and y window sizes from earlier
pygame.display.set_caption('Snake game')  # Setting the title of the window

def single_player():
    one_player_snake.onep_snake(screen, window_x, window_y)

def multiplayer():
    two_player_snake.twop_snake(screen, window_x, window_y)

menu = pygame_menu.Menu('Snek', 400, 300, theme=pygame_menu.themes.THEME_SOLARIZED)
menu.add.button('One player', single_player)
menu.add.button('Two Player', multiplayer)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(screen)