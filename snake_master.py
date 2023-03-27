import pygame
import menus
# Size of the window
sp_window_x = 500
sp_window_y = 480
mp_window_x = 720
mp_window_y = 480

pygame.init()  # Initializing the game window
screen = pygame.display.set_mode((mp_window_x, mp_window_y), pygame.NOFRAME)  # Creating the game window using the x and y window sizes from earlier

menus.main_menu(screen, mp_window_x, mp_window_y)

