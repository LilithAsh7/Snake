import pygame
import menus
# Size of the window
window_x = 720
window_y = 480

pygame.init()  # Initializing the game window
screen = pygame.display.set_mode((window_x, window_y), pygame.NOFRAME)  # Creating the game window using the x and y window sizes from earlier

menus.main_menu(screen, window_x, window_y)

