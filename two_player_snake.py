import pygame
import random
import menus
import time


# This function shows the score in the top left of the game window
def show_score(game_window, p1_score, p2_score):
    blue = pygame.Color(112, 241, 255)
    pink = pygame.Color(250, 147, 241)
    p1_color = pink
    p2_color = blue

    # Create font
    score_font = pygame.font.SysFont('times new roman', 20)

    # Create surface variables to be passed to .blit
    p1_score_surface = score_font.render(
        'P1 Score : ' + str(p1_score), True, p1_color)
    p2_score_surface = score_font.render(
        'P2 Score : ' + str(p2_score), True, p2_color)

    # Create rectangle variable to define shape of text box for the score
    score_rect = p1_score_surface.get_rect()

    # Use blit to draw the scoreboard onto the current game window
    game_window.blit(p1_score_surface, score_rect)
    game_window.blit(p2_score_surface, (0, 20))


# Checks winner and returns formatting info for game_over_message
def get_game_over_message(p1_score, p2_score, winner):
    blue = pygame.Color(112, 241, 255)
    pink = pygame.Color(250, 147, 241)
    white = pygame.Color(255, 255, 255)
    p1_color = pink
    p2_color = blue

    message_info = {}

    if winner == 1:
        message_info["color"] = p1_color
        message_info["message"] = "Player 1 wins!"
    elif winner == 2:
        message_info["color"] = p2_color
        message_info["message"] = "Player 2 wins!"
    else:
        message_info["color"] = white
        message_info["message"] = "Draw"

    message_info["p1_score"] = p1_score
    message_info["p2_score"] = p2_score

    return message_info


# This function displays the game over game message
def game_over_message(game_window, window_x, window_y, message_info):
    blue = pygame.Color(112, 241, 255)
    pink = pygame.Color(250, 147, 241)
    p1_color = pink
    p2_color = blue

    main_font = pygame.font.SysFont('times new roman', 50)
    sub_font = pygame.font.SysFont('times new roman', 20)

    # Create surface variables to be passed to .blit
    game_over_surface = main_font.render(
        message_info["message"], True, message_info["color"])
    p1_score_surface = sub_font.render(
        "Player 1: " + str(message_info["p1_score"]), True, p1_color)
    p2_score_surface = sub_font.render(
        "Player 2: " + str(message_info["p2_score"]), True, p2_color)

    # Gets locations of each surface
    game_over_rect = game_over_surface.get_rect()
    game_over_rect2 = p1_score_surface.get_rect()
    game_over_rect3 = p2_score_surface.get_rect()

    # Sets the position of each surface relative to a middle top position
    game_over_rect.midtop = (window_x / 2, window_y / 4)
    game_over_rect2.midtop = (window_x / 2, (window_y / 4) + 50)
    game_over_rect3.midtop = (window_x / 2, (window_y / 4) + 75)

    # Draw the surfaces in the window
    game_window.blit(game_over_surface, game_over_rect)
    game_window.blit(p1_score_surface, game_over_rect2)
    game_window.blit(p2_score_surface, game_over_rect3)
    pygame.display.flip()


# Draws snakes and fruit and handles movement as well as fruit eating mechanic
def two_player_snake(game_window, window_x, window_y):
    black = pygame.Color(0, 0, 0)
    blue = pygame.Color(112, 241, 255)
    pink = pygame.Color(250, 147, 241)
    white = pygame.Color(255, 255, 255)
    p1_color = pink
    p2_color = blue

    snake_speed = 13
    fps = pygame.time.Clock()

    # Sets the initial position of each snake
    # and the positions of the nodes that make the snakes body
    p1_position = [100, 50]
    p1_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    p2_position = [620, 50]
    p2_body = [[620, 50], [630, 50], [640, 50], [650, 50]]

    # Sets fruit spawn location
    fruit_position = [random.randrange(1, (window_x // 10))
                      * 10, random.randrange(1, (window_y // 10)) * 10]
    fruit_spawn = True
    spawn = True

    # Sets the initial direction that the snake is moving
    p1_direction = 'RIGHT'
    p2_direction = 'LEFT'

    # change_to is used to check whether if the snake's move is valid
    p1_change_to = p1_direction
    p2_change_to = p2_direction

    p1_score = 0
    p2_score = 0

    # Main infinite loop of the game
    while True:

        # Changes "change_to" based on keyboard input
        # or starts game_over_message on pressing escape
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
                if event.key == pygame.K_w:
                    p2_change_to = 'UP'
                if event.key == pygame.K_s:
                    p2_change_to = 'DOWN'
                if event.key == pygame.K_a:
                    p2_change_to = 'LEFT'
                if event.key == pygame.K_d:
                    p2_change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    if p1_score > p2_score:
                        message_info = get_game_over_message(
                            p1_score, p2_score, 1)
                        game_over_message(
                            game_window, window_x, window_y, message_info)
                        time.sleep(2)
                        menus.mp_score_input_menu(
                            game_window, message_info["p1_score"],
                            message_info["p2_score"])
                    elif p1_score < p2_score:
                        message_info = get_game_over_message(
                            p1_score, p2_score, 2)
                        game_over_message(
                            game_window, window_x, window_y, message_info)
                        time.sleep(2)
                        menus.mp_score_input_menu(
                            game_window, message_info["p1_score"],
                            message_info["p2_score"])
                    else:
                        message_info = get_game_over_message(
                            p1_score, p2_score, 3)
                        game_over_message(
                            game_window, window_x, window_y, message_info)
                        time.sleep(2)
                        menus.mp_score_input_menu(game_window,
                                                  message_info["p1_score"],
                                                  message_info["p2_score"])

        # Compares change_to with direction to make sure move is valid
        # then changes direction to change_to
        if p1_change_to == 'UP' and p1_direction != 'DOWN':
            p1_direction = 'UP'
        if p1_change_to == 'DOWN' and p1_direction != 'UP':
            p1_direction = 'DOWN'
        if p1_change_to == 'LEFT' and p1_direction != 'RIGHT':
            p1_direction = 'LEFT'
        if p1_change_to == 'RIGHT' and p1_direction != 'LEFT':
            p1_direction = 'RIGHT'
        if p2_change_to == 'UP' and p2_direction != 'DOWN':
            p2_direction = 'UP'
        if p2_change_to == 'DOWN' and p2_direction != 'UP':
            p2_direction = 'DOWN'
        if p2_change_to == 'LEFT' and p2_direction != 'RIGHT':
            p2_direction = 'LEFT'
        if p2_change_to == 'RIGHT' and p2_direction != 'LEFT':
            p2_direction = 'RIGHT'

        # Moves snake based on direction
        if p1_direction == 'UP':
            p1_position[1] -= 10
        if p1_direction == 'DOWN':
            p1_position[1] += 10
        if p1_direction == 'LEFT':
            p1_position[0] -= 10
        if p1_direction == 'RIGHT':
            p1_position[0] += 10
        if p2_direction == 'UP':
            p2_position[1] -= 10
        if p2_direction == 'DOWN':
            p2_position[1] += 10
        if p2_direction == 'LEFT':
            p2_position[0] -= 10
        if p2_direction == 'RIGHT':
            p2_position[0] += 10

        # Grows snake body
        p1_body.insert(0, list(p1_position))
        p2_body.insert(0, list(p2_position))

        # Grows snake by 1 if fruit is eaten and increments score by 10
        if p1_position[0] == fruit_position[0] and (
                p1_position[1] == fruit_position[1]):
            p1_score += 10
            fruit_spawn = False
            p2_body.pop()
        elif p2_position[0] == fruit_position[0] and (
                p2_position[1] == fruit_position[1]):
            p2_score += 10
            fruit_spawn = False
            p1_body.pop()
        # Pops off end of snake tail to simulate movement
        else:
            p1_body.pop()
            p2_body.pop()

        # Sets new random fruit position after its been eaten
        if not fruit_spawn:
            fruit_position = [random.randrange(1, (window_x // 10))
                              * 10, random.randrange(1, (window_y // 10)) * 10]

        fruit_spawn = True
        game_window.fill(black)

        # Draws a pink rectangle at each position in the snakes body
        for pos in p1_body:
            pygame.draw.rect(
                game_window, p1_color, pygame.Rect(pos[0], pos[1], 10, 10))
        for pos in p2_body:
            pygame.draw.rect(
                game_window, p2_color, pygame.Rect(pos[0], pos[1], 10, 10))

        # Draws new fruit
        pygame.draw.rect(game_window, white, pygame.Rect(
            fruit_position[0], fruit_position[1], 10, 10))

        # Wraps snake around if they touch a wall
        if p1_position[0] < 0:
            p1_position[0] = window_x - 10
        if p1_position[0] > window_x - 10:
            p1_position[0] = -10
        if p1_position[1] < 0:
            p1_position[1] = window_y - 10
        if p1_position[1] > window_y - 10:
            p1_position[1] = -10
        if p2_position[0] < 0:
            p2_position[0] = window_x - 10
        if p2_position[0] > window_x - 10:
            p2_position[0] = -10
        if p2_position[1] < 0:  # top
            p2_position[1] = window_y - 10
        if p2_position[1] > window_y - 10:
            p2_position[1] = -10

        # Draw conditions
        if (p1_position[0] == p2_position[0]
                              and p1_position[1] == p2_position[1]):
            message_info = get_game_over_message(p1_score, p2_score, 3)
            game_over_message(game_window, window_x, window_y, message_info)
            time.sleep(2)
            menus.mp_score_input_menu(game_window,
                                      message_info["p1_score"],
                                      message_info["p2_score"])

        # Triggers game_over on certain conditions
        for block in p1_body[1:]:
            # If player 1 touches their own body
            if p1_position[0] == block[0] and p1_position[1] == block[1]:
                message_info = get_game_over_message(p1_score, p2_score, 2)
                game_over_message(game_window,
                                  window_x,
                                  window_y, message_info)
                time.sleep(2)
                menus.mp_score_input_menu(game_window,
                                          message_info["p1_score"],
                                          message_info["p2_score"])
            # If player 2 touches player 1's body
            if p2_position[0] == block[0] and p2_position[1] == block[1]:
                message_info = get_game_over_message(p1_score, p2_score, 1)
                game_over_message(game_window,
                                  window_x,
                                  window_y, message_info)
                time.sleep(2)
                menus.mp_score_input_menu(game_window,
                                          message_info["p1_score"],
                                          message_info["p2_score"])
        for block in p2_body[1:]:
            # If player 2 touches their own body
            if p2_position[0] == block[0] and p2_position[1] == block[1]:
                message_info = get_game_over_message(p1_score, p2_score, 1)
                game_over_message(game_window,
                                  window_x,
                                  window_y, message_info)
                time.sleep(2)
                menus.mp_score_input_menu(game_window,
                                          message_info["p1_score"],
                                          message_info["p2_score"])
            # If player 1 touches player 2's body
            if p1_position[0] == block[0] and p1_position[1] == block[1]:
                message_info = get_game_over_message(p1_score, p2_score, 2)
                game_over_message(game_window,
                                  window_x,
                                  window_y, message_info)
                time.sleep(2)
                menus.mp_score_input_menu(game_window,
                                          message_info["p1_score"],
                                          message_info["p2_score"])

        # Continuously display score
        show_score(game_window, p1_score, p2_score)

        # Refresh game window
        pygame.display.update()

        # Runs "get set, go!" code on initial spawn
        if spawn:
            menus.spawn_countdown(game_window, window_x, window_y)
            spawn = False

        # Refresh rate
        fps.tick(snake_speed)
