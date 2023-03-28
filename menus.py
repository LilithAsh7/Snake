import pygame
import pygame_menu
import one_player_snake
import two_player_snake
from datetime import date
from tinydb import TinyDB
import time


# Creates main menu
# with single player, multiplayer, high score, and quit buttons.
def main_menu():
    main_window_x = 500
    main_window_y = 480

    pygame.init()
    game_window = pygame.display.set_mode(
        (main_window_x, main_window_y), pygame.NOFRAME)

    # These three functions are triggered on the corresponding button presses
    # Launches single player snake game
    def single_player():
        one_player_snake.one_player_snake(
            game_window, main_window_x, main_window_y)

    # Launches 2 player snake game with bigger window
    def multiplayer():
        mp_window_x = 720
        mp_window_y = 480
        new_game_window = pygame.display.set_mode(
            (mp_window_x, mp_window_y), pygame.NOFRAME)
        two_player_snake.two_player_snake(
            new_game_window, mp_window_x, mp_window_y)

    # Launches the high score menu
    def launch_high_score_menu():
        high_score_menu(game_window)

    # Creates menu, populates it with buttons, and draws it on game_window
    menu = pygame_menu.Menu(
        'Snek', 400, 300, theme=pygame_menu.themes.THEME_SOLARIZED)
    menu.add.button('One player', single_player)
    menu.add.button('Two Player', multiplayer)
    menu.add.button('High Scores', launch_high_score_menu)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(game_window)


# Gets top 3 high scores for single player and multiplayer
def get_high_scores():
    # Sets the database to scores.json
    score_database = TinyDB("scores.json")

    # The default table is _default which is for single player scores.
    # This line sets mp_table as the multiplayer table.
    mp_table = score_database.table("multiplayer")

    # Initializing variables for high score comparison
    sp_first = {'name': 'none', 'score': '0', 'date': '0000-00-00'}
    sp_second = {'name': 'none', 'score': '0', 'date': '0000-00-00'}
    sp_third = {'name': 'none', 'score': '0', 'date': '0000-00-00'}
    mp_first = {'name': 'none', 'score': '0', 'date': '0000-00-00'}
    mp_second = {'name': 'none', 'score': '0', 'date': '0000-00-00'}
    mp_third = {'name': 'none', 'score': '0', 'date': '0000-00-00'}

    # Bubble sorts to set first second and third high scores
    # Bubble sort for single player scores
    for i in score_database:
        if int(i['score']) >= int(sp_first['score']):
            sp_third = sp_second
            sp_second = sp_first
            sp_first = i
        elif int(i['score']) >= int(sp_second['score']):
            sp_third = sp_second
            sp_second = i
        elif int(i['score']) >= int(sp_third['score']):
            sp_third = i

    # Bubble sort for multiplayer scores
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

    # Inserts the strings returned by format_high_scores into all_high_scores
    all_high_scores = []
    all_high_scores.insert(
        0, format_high_scores(sp_first, sp_second, sp_third))
    all_high_scores.insert(
        1, format_high_scores(mp_first, mp_second, mp_third))

    return all_high_scores


# Formats and returns high scores for display on the high score menu
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
def high_score_menu(game_window):
    # Gets formatted high scores
    high_scores = get_high_scores()

    # Creates and displays high score menu
    menu = pygame_menu.Menu(
        'High Scores', 400, 480, theme=pygame_menu.themes.THEME_SOLARIZED)
    menu.add.label("Single Player", max_char=-1, font_size=30)
    menu.add.label(high_scores[0], max_char=-1, font_size=20)
    menu.add.label("Multiplayer", max_char=-1, font_size=30)
    menu.add.label(high_scores[1], max_char=-1, font_size=20)
    menu.add.button('Back', main_menu)
    menu.mainloop(game_window)


# Creates single player score input menu and adds score to database
def sp_score_input_menu(game_window, p1_score):
    # Adds players input name and score to database
    def add_name(in_name):
        # Defines database file
        score_database = TinyDB("scores.json")

        # User input from text_input button on score_input_menu
        name = in_name

        # Gets todays date
        today = str(date.today())

        # Inserts name, score, and date into database
        score_database.insert(
            {'name': name, 'score': p1_score, 'date': today})

        main_menu()

    # Creates single player score input menu
    menu = pygame_menu.Menu(
        'New Score', 300, 200, theme=pygame_menu.themes.THEME_SOLARIZED)
    menu.add.label('Score: ' + str(p1_score), max_char=-1, font_size=20)
    # The text input of this button is passed to add_name as in_name
    menu.add.text_input(
        'Name: ', default='XXX', maxchar=3, onreturn=add_name)
    menu.add.label('Press enter when done', max_char=-1, font_size=20)
    menu.mainloop(game_window)


# Displays 2 multiplayer high score input menus one at a time
# The first displayed window is for player 1
# The second displayed window is for player 2
def mp_score_input_menu(game_window, p1_score, p2_score):
    dark_pink = pygame.Color(199, 2, 143)

    # Adds player 1's score and creates menu for player 2's input
    def add_first_name(in_name):
        # Color to be used for second players input
        dark_blue = pygame.Color(2, 15, 199)

        # Defines database file and multiplayer table
        score_database = TinyDB("scores.json")
        mp_table = score_database.table("multiplayer")

        # User input from text_input button on score input menu
        name = in_name

        # Gets todays date
        today = str(date.today())

        # Inserts player 1's name, score, and the date into database
        mp_table.insert({'name': name, 'score': p1_score, 'date': today})

        # Creates and displays new menu for player 2's score input
        new_menu = pygame_menu.Menu(
            'New Score', 300, 200,
            theme=pygame_menu.themes.THEME_SOLARIZED)
        new_menu.add.label(
            'Score: ' + str(p2_score),
            font_color=dark_blue, max_char=-1, font_size=20)
        # The text input of this button is passed to add_second_name as in_name
        new_menu.add.text_input(
            'Player 2: ', default='XXX',
            maxchar=3, onreturn=add_second_name)
        new_menu.add.label(
            'Press enter when done', max_char=-1, font_size=20)
        new_menu.mainloop(game_window)

    # Adds players 2's input name and goes back to main menu
    def add_second_name(in_name):
        # Defines database file and multiplayer table
        score_database = TinyDB("scores.json")
        mp_table = score_database.table("multiplayer")

        # User input from text_input button on score input menu
        name = in_name

        # Gets today's date
        today = str(date.today())

        # Inserts player 2's name, score, and the date into database
        mp_table.insert({'name': name, 'score': p2_score, 'date': today})
        # Goes back to main menu
        main_menu()

    # Creates and displays first multiplayer score input menu
    menu = pygame_menu.Menu(
        'New Score', 300, 200, theme=pygame_menu.themes.THEME_SOLARIZED)
    menu.add.label(
        'Score: ' + str(p1_score),
        font_color=dark_pink, max_char=-1, font_size=20)
    menu.add.text_input(
        'Player 1: ', default='XXX', maxchar=3, onreturn=add_first_name)
    menu.add.label('Press enter when done', max_char=-1, font_size=20)
    menu.mainloop(game_window)


# Displays "Get set" then "Go!" before starting the game
# Gives the players 2 seconds to get ready
def spawn_countdown(game_window, window_x, window_y):
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)
    set_go = "Get set"
    main_font = pygame.font.SysFont('times new roman', 50)
    
    # Renders words from set_go and draws them in the game window
    ready_surface = main_font.render(set_go, True, red)
    ready_rect = ready_surface.get_rect()
    ready_rect.midtop = (window_x / 2, window_y / 4)
    game_window.blit(ready_surface, ready_rect)
    pygame.display.flip()
    
    # Delays code by 1 second, erases previous words and sets set_go to "Go!"
    time.sleep(1)
    game_window.fill(pygame.Color("black"), ready_rect)
    set_go = "Go!"

    # Renders words from set_go and draws them in the game window
    ready_surface = main_font.render(set_go, True, green)
    ready_rect = ready_surface.get_rect()
    ready_rect.midtop = (window_x / 2, window_y / 4)
    game_window.blit(ready_surface, ready_rect)
    pygame.display.flip()
    
    # Delays code one more time before continuing
    time.sleep(1)
