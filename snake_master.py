import pygame
import time #Used for timed delays
import random

snake_speed = 10

#Size of the window
window_x = 720
window_y = 480

#Defining colors that will be used later
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

pygame.init()   #Initializing the game window
screen = pygame.display.set_mode((window_x, window_y))  #Creating the game window using the x and y window sizes from earlier
pygame.display.set_caption('Snake game')                #Setting the title of the window

fps = pygame.time.Clock()   #Defines the intended frames per second

snake_position = [100, 50]  #Sets the initial position of the snake
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]  #Sets the positions of the nodes that make the snakes body

#Sets a random fruit position within the window range and sets fruit_spawn to TRUE, meaning that a fruit is on the board
fruit_position = [random.randrange(1, (window_x//10)) * 10, random.randrange(1, (window_y//10)) * 10]
fruit_spawn = True

#Sets the initial direction that the snake is moving to "RIGHT"
direction = 'RIGHT'     #direction is the current direction of the snake

                        #change_to is used to check whether the snake can move from the current direction to the next direction
change_to = direction   #for example, if the snake is moving up it can't immediately switch to moving down
                        #so if direction = "UP" and change_to = "DOWN" then nothing will happen 

score = 0   #Set initial score to zero

#This function shows the score in the top left of the screen
def show_score(choice, color, font, size):
    
    #Create font
    score_font = pygame.font.SysFont(font, size)

    #Create surface variable to be passed to .blit
    score_surface = score_font.render('Score : ' + str(score), True, color)

    #Create rectangle variable to define shape of text box for the score
    score_rect = score_surface.get_rect()

    #Use blit to draw the scoreboard onto the current screen
    screen.blit(score_surface, score_rect)

def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)

    game_over_surface = my_font.render('Your score is : ' + str(score), True, red)

    game_over_rect = game_over_surface.get_rect()

    game_over_rect.midtop = (window_x/2, window_y/4)

    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    time.sleep(2)

    pygame.quit
    quit()

while True:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        fruit_spawn = False
    else:
        snake_body.pop()

    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x//10)) * 10, random.randrange(1, (window_y//10)) * 10]

    fruit_spawn = True
    screen.fill(black)

    for pos in snake_body:
        pygame.draw.rect(screen, green, pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(screen, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    if snake_position[0] < 0 or snake_position[0] > window_x-10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y-10:
        game_over()

    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    show_score(1, white, 'times new roman', 20)

    pygame.display.update()

    fps.tick(snake_speed)
