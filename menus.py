import pygame
import pygame_menu
import one_player_snake
import two_player_snake
from datetime import date
from tinydb import TinyDB

dark_blue = pygame.Color(2, 15, 199)
dark_pink = pygame.Color(199, 2, 143)

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

    def launch_main_menu():
        main_menu(screen, window_x, window_y)

    scoredb = TinyDB("scores.json")
    mp_table = scoredb.table("multiplayer")

    #i = {'name': 'none', 'score': '0', 'date': '0000-00-00'}
    sp_first = {'name': 'none', 'score': '0', 'date': '0000-00-00'}
    sp_second = {'name': 'none', 'score': '0', 'date': '0000-00-00'}
    sp_third = {'name': 'none', 'score': '0', 'date': '0000-00-00'}
    mp_first = {'name': 'none', 'score': '0', 'date': '0000-00-00'}
    mp_second = {'name': 'none', 'score': '0', 'date': '0000-00-00'}
    mp_third = {'name': 'none', 'score': '0', 'date': '0000-00-00'}

    for i in scoredb:
        if int(i['score']) >= int(sp_first['score']):
            sp_third = sp_second
            sp_second = sp_first
            sp_first = i
        elif int(i['score']) >= int(sp_second['score']):
            sp_third = sp_second
            sp_second = i
        elif int(i['score']) >= int(sp_third['score']):
            sp_third = i

    for i in mp_table:
        if int(i['score']) >= int(mp_first['score']):
            mp_third = mp_second
            mp_second = mp_first
            mp_first = i
        elif int(i['score']) >= int(mp_second['score']):
            mp_third = mp_second
            mp_second = i
        elif int(i['score']) >= int(mp_third['score']):
            mp_third = i

    sp_high_scores = ('1. ' + str(sp_first['score']) + ' - ' + sp_first["name"] + " " + sp_first["date"] + "\n"
                   + "2. " + str(sp_second["score"]) + " - " + sp_second["name"] + " " + sp_second["date"] + "\n"
                   + "3. " + str(sp_third["score"]) + " - " + sp_third["name"] + " " + sp_third["date"]
                   )
    mp_high_scores = ('1. ' + str(mp_first['score']) + ' - ' + mp_first["name"] + " " + mp_first["date"] + "\n"
                      + "2. " + str(mp_second["score"]) + " - " + mp_second["name"] + " " + mp_second["date"] + "\n"
                      + "3. " + str(mp_third["score"]) + " - " + mp_third["name"] + " " + mp_third["date"]
                      )

    menu = pygame_menu.Menu('High Scores', 400, 480, theme=pygame_menu.themes.THEME_SOLARIZED)
    menu.add.label("Single Player", max_char=-1, font_size=30)
    menu.add.label(sp_high_scores, max_char=-1, font_size=20)
    menu.add.label("Multiplayer", max_char=-1, font_size=30)
    menu.add.label(mp_high_scores, max_char=-1, font_size=20)
    menu.add.button('Back', launch_main_menu)
    menu.mainloop(screen)

def sp_score_input_menu(screen, window_x, window_y, p1_score):

    def add_name(in_name):
        
        nonlocal p1_score
        nonlocal screen
        nonlocal window_x
        nonlocal window_y
        
        scoredb = TinyDB("scores.json")

        name = in_name
        today = str(date.today())
        scoredb.insert({'name': name, 'score': p1_score, 'date': today})
        main_menu(screen, window_x, window_y)

    menu = pygame_menu.Menu('New Score', 300, 200, theme=pygame_menu.themes.THEME_SOLARIZED)
    menu.add.label('Score: ' + str(p1_score), max_char=-1, font_size=20)
    menu.add.text_input('Name: ', default='XXX', maxchar = 3, onreturn = add_name)
    menu.add.label('Press enter when done', max_char=-1, font_size=20)
    menu.mainloop(screen)


def mp_score_input_menu(screen, window_x, window_y, p1_score, p2_score):

    def add_first_name(in_name):
        nonlocal p1_score
        nonlocal screen
        nonlocal window_x
        nonlocal window_y

        scoredb = TinyDB("scores.json")
        mp_table = scoredb.table("multiplayer")

        name = in_name
        today = str(date.today())
        mp_table.insert({'name': name, 'score': p1_score, 'date': today})

        menu = pygame_menu.Menu('New Score', 300, 200, theme=pygame_menu.themes.THEME_SOLARIZED)
        menu.add.label('Score: ' + str(p2_score), font_color = dark_blue, max_char=-1, font_size=20)
        menu.add.text_input('Player 2: ', default='XXX', maxchar=3, onreturn=add_second_name)
        menu.add.label('Press enter when done', max_char=-1, font_size=20)
        menu.mainloop(screen)

    def add_second_name(in_name):
        nonlocal p2_score
        nonlocal screen
        nonlocal window_x
        nonlocal window_y

        scoredb = TinyDB("scores.json")
        mp_table = scoredb.table("multiplayer")

        name = in_name
        today = str(date.today())
        mp_table.insert({'name': name, 'score': p2_score, 'date': today})
        main_menu(screen, window_x, window_y)

    menu = pygame_menu.Menu('New Score', 300, 200, theme=pygame_menu.themes.THEME_SOLARIZED)
    menu.add.label('Score: ' + str(p1_score), font_color = dark_pink, max_char=-1, font_size=20)
    menu.add.text_input('Player 1: ', default='XXX', maxchar=3, onreturn=add_first_name)
    menu.add.label('Press enter when done', max_char=-1, font_size=20)
    menu.mainloop(screen)