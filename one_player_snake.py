import pygame
import random
import menus
import time


# This function shows the score in the top left of the game window
def show_score(game_window, p1_score):
    pink = pygame.Color(250, 147, 241)

    score_font = pygame.font.SysFont('times new roman', 20)

    # Creates object to render "Score :" in desired font and color (pink)
    score_surface = score_font.render(
        'Score : ' + str(p1_score), True, pink)

    # Gets rectangular area of the score surface
    score_rect = score_surface.get_rect()

    # Use blit to draw score_surface at the coordinates score_rect
    game_window.blit(score_surface, score_rect)


# This function displays the game over message
def game_over(game_window, window_x, window_y, p1_score):
    red = pygame.Color(255, 0, 0)

    main_font = pygame.font.SysFont('times new roman', 50)

    # Creates object to render game over message
    game_over_surface = main_font.render(
        'Your score is : ' + str(p1_score), True, red)

    # Gets rectangular area of game over surface
    game_over_rect = game_over_surface.get_rect()

    # Sets the position of the game over message to be middle top
    game_over_rect.midtop = (window_x / 2, window_y / 4)

    # Draws the game over surface at the coordinates game_over_rect
    game_window.blit(game_over_surface, game_over_rect)

    # Updates the display
    pygame.display.flip()


def one_player_snake(game_window, window_x, window_y):
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    pink = pygame.Color(250, 147, 241)

    snake_speed = 13  # Speed of the snake
    fps = pygame.time.Clock()  # Defines the intended frames per second

    p1_position = [100, 50]  # Sets the initial position of the snake
    p1_body = [[100, 50], [90, 50], [80, 50], [70, 50]]  # Sets the positions of the nodes that make the snakes body

    # Sets a random fruit position within the window range and sets fruit_spawn to TRUE,
    # meaning that a fruit is on the board
    fruit_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]
    fruit_spawn = True
    spawn = True

    # Sets the initial direction that the snake is moving to "RIGHT"
    p1_direction = 'RIGHT'  # direction is the current direction of the snake

    # change_to is used to check whether the snake can move from the current direction to the next direction
    p1_change_to = p1_direction  # for example, if the snake is moving up it can't immediately switch to moving down
    # so if direction = "UP" and change_to = "DOWN" then nothing will happen

    p1_score = 0  # Set initial score to zero

    # Main while loop of the game
    while True:

        # Changes "change_to" based on keyboard input
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    p1_change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    p1_change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    p1_change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    p1_change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    game_over(game_window, window_x, window_y, p1_score)
                    time.sleep(2)
                    menus.sp_score_input_menu(game_window, p1_score)

        # Compares change_to with direction to make sure move is valid, if it's valid it changed direction to that move
        if p1_change_to == 'UP' and p1_direction != 'DOWN':
            p1_direction = 'UP'
        if p1_change_to == 'DOWN' and p1_direction != 'UP':
            p1_direction = 'DOWN'
        if p1_change_to == 'LEFT' and p1_direction != 'RIGHT':
            p1_direction = 'LEFT'
        if p1_change_to == 'RIGHT' and p1_direction != 'LEFT':
            p1_direction = 'RIGHT'

        # Moves snake based on direction
        if p1_direction == 'UP':
            p1_position[1] -= 10
        if p1_direction == 'DOWN':
            p1_position[1] += 10
        if p1_direction == 'LEFT':
            p1_position[0] -= 10
        if p1_direction == 'RIGHT':
            p1_position[0] += 10

        # Grows snake body
        p1_body.insert(0, list(p1_position))  # Grows head of body in correct position

        # If a piece of fruit is eaten the tailpiece of the snake is not popped off, so it gets 1 node longer
        # Increments score by 10 when fruit is eaten
        if p1_position[0] == fruit_position[0] and p1_position[1] == fruit_position[1]:
            p1_score += 10
            fruit_spawn = False
        else:
            p1_body.pop()  # Pops off the final piece to simulate the snake moving

        # Sets new random fruit position after its been eaten
        if not fruit_spawn:
            fruit_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]

        fruit_spawn = True
        game_window.fill(black)

        # Draws a pink rectangle at each position in the snakes body
        for pos in p1_body:
            pygame.draw.rect(game_window, pink, pygame.Rect(pos[0], pos[1], 10, 10))

        # Draws new fruit
        pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

        # Triggers game_over if the snake touches the walls

        if p1_position[0] < 0:  # left
            p1_position[0] = window_x - 10
        if p1_position[0] > window_x - 10:  # right
            p1_position[0] = 0
        if p1_position[1] < 0:  # top
            p1_position[1] = window_y - 10
        if p1_position[1] > window_y - 10:  # bottom
            p1_position[1] = 0

        # Triggers game_over if the snake touches its own body
        for block in p1_body[1:]:
            if p1_position[0] == block[0] and p1_position[1] == block[1]:
                game_over(game_window, window_x, window_y, p1_score)
                time.sleep(2)
                menus.sp_score_input_menu(game_window, p1_score)

        # Continuously display score
        show_score(game_window, p1_score)

        if spawn:
            menus.spawn_countdown(game_window, window_x, window_y)
            spawn = False

        # Refresh game window
        pygame.display.update()

        # Refresh rate
        fps.tick(snake_speed)
