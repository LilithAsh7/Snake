import pygame
import pygame_menu
import one_player_snake
import two_player_snake
from datetime import date
from tinydb import TinyDB


def main_menu():
    main_window_x = 500
    main_window_y = 480

    pygame.init()
    screen = pygame.display.set_mode(
        (main_window_x, main_window_y), pygame.NOFRAME)

    def single_player():
        one_player_snake.onep_snake(screen, main_window_x, main_window_y)

    def multiplayer():
        mp_window_x = 720
        mp_window_y = 480
        new_screen = pygame.display.set_mode(
            (mp_window_x, mp_window_y), pygame.NOFRAME)
        two_player_snake.twop_snake(new_screen, mp_window_x, mp_window_y)

    def launch_high_score_menu():
        high_score_menu(screen)

    menu = pygame_menu.Menu(
        'Snek', 400, 300, theme=pygame_menu.themes.THEME_SOLARIZED)
    menu.add.button('One player', single_player)
    menu.add.button('Two Player', multiplayer)
    menu.add.button('High Scores', launch_high_score_menu)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)


# Gets top 3 high scores for single player and multiplayer
def get_high_scores():
    scoredb = TinyDB("scores.json")
    mp_table = scoredb.table("multiplayer")

    sp_first = {'name': 'none', 'score': '0', 'date': '0000-00-00'}
    sp_second = {'name': 'none', 'score': '0', 'date': '0000-00-00'}
    sp_third = {'name': 'none', 'score': '0', 'date': '0000-00-00'}
    mp_first = {'name': 'none', 'score': '0', 'date': '0000-00-00'}
    mp_second = {'name': 'none', 'score': '0', 'date': '0000-00-00'}
    mp_third = {'name': 'none', 'score': '0', 'date': '0000-00-00'}

    all_high_scores = []

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

    sp_high_scores = format_high_scores(sp_first, sp_second, sp_third)
    mp_high_scores = format_high_scores(mp_first, mp_second, mp_third)

    all_high_scores.insert(0, sp_high_scores)
    all_high_scores.insert(1, mp_high_scores)

    return all_high_scores


# Formats high scores for display on the high score menu
def format_high_scores(first, second, third):
    high_scores = ('1. ' + str(first['score']) + ' - '
                   + first["name"] + " " + first["date"] + "\n"
                   + "2. " + str(second["score"]) + " - "
                   + second["name"] + " " + second["date"] + "\n"
                   + "3. " + str(third["score"]) + " - "
                   + third["name"] + " " + third["date"]
                   )

    return high_scores


# Displays high score menu
def high_score_menu(screen):
    high_scores = get_high_scores()

    menu = pygame_menu.Menu(
        'High Scores', 400, 480, theme=pygame_menu.themes.THEME_SOLARIZED)
    menu.add.label("Single Player", max_char=-1, font_size=30)
    menu.add.label(high_scores[0], max_char=-1, font_size=20)
    menu.add.label("Multiplayer", max_char=-1, font_size=30)
    menu.add.label(high_scores[1], max_char=-1, font_size=20)
    menu.add.button('Back', main_menu)
    menu.mainloop(screen)


def sp_score_input_menu(screen, p1_score):
    def add_name(in_name):

        scoredb = TinyDB("scores.json")

        name = in_name
        today = str(date.today())
        scoredb.insert({'name': name, 'score': p1_score, 'date': today})
        main_menu()

    menu = pygame_menu.Menu(
        'New Score', 300, 200, theme=pygame_menu.themes.THEME_SOLARIZED)
    menu.add.label('Score: ' + str(p1_score), max_char=-1, font_size=20)
    menu.add.text_input(
        'Name: ', default='XXX', maxchar=3, onreturn=add_name)
    menu.add.label('Press enter when done', max_char=-1, font_size=20)
    menu.mainloop(screen)

#Displays high score input menu
def mp_score_input_menu(screen, p1_score, p2_score):

    #Adds player 1's name
    def add_first_name(in_name):
        dark_blue = pygame.Color(2, 15, 199)

        scoredb = TinyDB("scores.json")
        mp_table = scoredb.table("multiplayer")

        name = in_name
        today = str(date.today())
        mp_table.insert({'name': name, 'score': p1_score, 'date': today})

        new_menu = pygame_menu.Menu(
            'New Score', 300, 200,
            theme=pygame_menu.themes.THEME_SOLARIZED)
        new_menu.add.label(
            'Score: ' + str(p2_score),
            font_color=dark_blue, max_char=-1, font_size=20)
        new_menu.add.text_input(
            'Player 2: ', default='XXX',
            maxchar=3, onreturn=add_second_name)
        new_menu.add.label(
            'Press enter when done', max_char=-1, font_size=20)
        new_menu.mainloop(screen)

    #Adds players 2's name
    def add_second_name(in_name):

        scoredb = TinyDB("scores.json")
        mp_table = scoredb.table("multiplayer")

        name = in_name
        today = str(date.today())
        mp_table.insert({'name': name, 'score': p2_score, 'date': today})
        main_menu()

    dark_pink = pygame.Color(199, 2, 143)
    menu = pygame_menu.Menu(
        'New Score', 300, 200, theme=pygame_menu.themes.THEME_SOLARIZED)
    menu.add.label(
        'Score: ' + str(p1_score),
        font_color=dark_pink, max_char=-1, font_size=20)
    menu.add.text_input(
        'Player 1: ', default='XXX', maxchar=3, onreturn=add_first_name)
    menu.add.label('Press enter when done', max_char=-1, font_size=20)
    menu.mainloop(screen)
