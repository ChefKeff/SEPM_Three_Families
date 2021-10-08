'''
This is the main module running the game.

(C) 2021 Group G
'''

import sys
import time
import json
from tools import prompt, clear_screen, show_rules, boxed_output
from game_class import Game


def setup_names(game):
    '''Setup the names for the players'''
    white_player_name = ''
    black_player_name = ''

    # White Player
    while True:
        print('> Enter name for white player:')
        white_player_name = input()
        if len(white_player_name) < 2 or len(white_player_name) > 10:
            boxed_output('Please enter a name between 2 and 10 characters!')
            continue

        game.set_player_name('white', white_player_name)
        print('> Name successfully set')
        break

    clear_screen()

    # Black Player
    while True:
        print('> Enter name for black player:')
        black_player_name = input()
        if len(black_player_name) < 2 or len(black_player_name) > 10:
            boxed_output('Please enter a name between 2 and 10 characters!')
            continue
        
        if game.white_player['name'].lower() == black_player_name.lower():
            boxed_output('Both players cannot have the same name!')
            continue

        game.set_player_name('black', black_player_name)
        print('> Name successfully set')
        time.sleep(2)
        break



def play_local(game):
    '''Starts game in local mode.'''
    print("Playing Locally")    

    # Ask if user wants to play agains AI or not and difficulty
    show_ai_options(game)

    # Ask names for the two players
    setup_names(game)
    

def play_online():
    '''Starts game in online mode.'''
    print("Playing Online")


def quit_game():
    '''Quits the game.'''
    sys.exit()


# ------------------------------ GAME OPTIONS MENU ------------------------------

def turn_on_ai(game):
    '''Turns the AI on.'''
    game.toggle_ai(1)

def turn_off_ai(game):
    '''Turns the AI off.'''
    game.toggle_ai(0)

def set_ai_easy(game):
    '''Sets the difficulty of the AI to easy.'''
    game.set_ai_difficulty('easy')

def set_ai_medium(game):
    '''Sets the difficulty of the AI to medium.'''
    game.set_ai_difficulty('medium')

def set_ai_hard(game):
    '''Sets the difficulty of the AI to hard.'''
    game.set_ai_difficulty('hard')

def show_ai_options(game):
    '''Shows AI options.'''
    clear_screen()

    # Ask whether to play against an AI or not
    prompt(
        'Who do you want to play against?',
        ['Other Player', 'AI'],
        ['p', 'a'],
        [turn_off_ai, turn_on_ai],
        False,
        arguments=[game, game]
    )

    if game.play_with_ai:
        prompt(
            'AI settings (current setting is '+game.ai_difficulty+'):',
            ['Easy', 'Medium', 'Hard'],
            ['e', 'm', 'h'],
            [set_ai_easy, set_ai_medium, set_ai_hard],
            False,
            arguments=[game, game, game]
        )
            
# ------------------------------ START SCREEN ------------------------------

def start_screen(game):
    '''Prints the starting screen and prompts user with options.'''
    clear_screen()
    prompt(
        'Welcome!, please select an alternative:',
        ['Start', 'Rules', 'Quit'],
        ['s', 'r', 'o', 'p', 'q'],
        [game.start_game, show_rules, quit_game],
        False,
        arguments=[None, None, None]
    )
    clear_screen()
    if game.game_running:
        prompt(
            'Choose an option: ',
            ["Local", "Online"],
            ['l', 'o'],
            [play_local, play_online],
            False,
            arguments=[game, None]
        )


def get_board_structure(filename):
    '''Fetch board structure from a .json-file.'''
    # Read JSON file containing the board structure
    with open(filename, 'r', encoding='utf-8') as board_file:
        data = board_file.read()
    return json.loads(data)


def main():
    '''The main function which acts as the starting point of the game.'''

    # Get the board structure from file
    board_structure = get_board_structure('board.json')

    # Initiate the game with the board_structure
    game = Game(board_structure)

    while True:
        # Show start screen (Start, Rules, Quit)
        start_screen(game)

        while game.game_running:
            # Stage 1
            game.place_pieces_phase()

            # Stage 2
            game.move_pieces_phase()


if __name__ == "__main__":
    main()
