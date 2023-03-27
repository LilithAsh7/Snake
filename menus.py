import pygame
import pygame_menu
import one_player_snake
import two_player_snake
from datetime import date
from tinydb import TinyDB

def main_menu(screen, window_x, window_y):
    def single_player():
        one_player_snake.onep_snake(screen, window_x, window_y)

    def multiplayer():
        two_player_snake.twop_snake(screen, window_x, window_y)

    def launch_high_score_menu():
        high_score_menu(screen, window_x, window_y)

    menu_surface = pygame.Surface((400, 300))

    menu = pygame_menu.Menu('Snek', 400, 300, theme=pygame_menu.themes.THEME_SOLARIZED)
    menu.add.button('One player', single_player)
    menu.add.button('Two Player', multiplayer)
    menu.add.button('High Scores', launch_high_score_menu)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)

def high_score_menu(screen, window_x, window_y):
#def high_score_menu(screen, window_x, window_y):

    def launch_main_menu():
        main_menu(screen, window_x, window_y)

    scoredb = TinyDB("scores.json")

    #i = {'name': 'none', 'score': '0', 'date': '0000-00-00'}
    first = {'name': 'none', 'score': '0', 'date': '0000-00-00'}
    second = {'name': 'none', 'score': '0', 'date': '0000-00-00'}
    third = {'name': 'none', 'score': '0', 'date': '0000-00-00'}

    for i in scoredb:
        if int(i['score']) >= int(first['score']):
            third = second
            second = first
            first = i
        elif int(i['score']) >= int(second['score']):
            third = second
            second = i
        elif int(i['score']) >= int(third['score']):
            third = i

    high_scores = ('1. ' + str(first['score']) + ' - ' + first["name"] + " " + first["date"] + "\n"
                   + "2. " + str(second["score"]) + " - " + second["name"] + " " + second["date"] + "\n"
                   + "3. " + str(third["score"]) + " - " + third["name"] + " " + third["date"]
                   )

    menu = pygame_menu.Menu('High Scores', 400, 300, theme=pygame_menu.themes.THEME_SOLARIZED)
    menu.add.label(high_scores, max_char=-1, font_size=20)
    menu.add.button('Back', launch_main_menu)
    menu.mainloop(screen)

def score_input_menu(screen, window_x, window_y, score):

    #in_score = score

    def add_name(in_name):


        nonlocal score
        nonlocal screen
        nonlocal window_x
        nonlocal window_y
        
        scoredb = TinyDB("scores.json")

        name = in_name
        today = str(date.today())
        scoredb.insert({'name': name, 'score': score, 'date': today})

        main_menu(screen, window_x, window_y)

    menu = pygame_menu.Menu('New Score', 300, 200, theme=pygame_menu.themes.THEME_SOLARIZED)
    menu.add.text_input('Name: ', default='XXX', maxchar = 3, onreturn = add_name)
    menu.add.label('Press enter when done', max_char=-1, font_size=20)
    menu.mainloop(screen)
