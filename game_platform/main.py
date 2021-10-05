'''
This is the main module running the game.

(C) 2021 Group G
'''

import sys
import json
from tools import prompt, clear_screen, show_rules
from game_class import Game


def play_local():
    '''Starts game in local mode.'''
    print("Playing Locally")


def play_online():
    '''Starts game in online mode.'''
    print("Playing Online")


def quit_game():
    '''Quits the game.'''
    sys.exit()


def set_ai_easy(game):
    '''Sets the difficulty of the AI to easy.'''
    game.set_ai_difficulty('easy')

def set_ai_medium(game):
    '''Sets the difficulty of the AI to medium.'''
    game.set_ai_difficulty('medium')

def set_ai_hard(game):
    '''Sets the difficulty of the AI to hard.'''
    game.set_ai_difficulty('hard')

def go_back():
    '''Makes user go back from ai difficulty (really fast fix).'''
    return

def show_options(game):
    clear_screen()
    prompt(
        'AI difficilty (current setting is '+game.ai_difficulty+'):',
        ['Easy', 'Medium', 'Hard', 'Back'],
        ['e', 'm', 'h', 'b'],
        [set_ai_easy, set_ai_medium, set_ai_hard, go_back],
        False,
        arguments=[game, game, game, None]
    )


def start_screen(game):
    '''Prints the starting screen and prompts user with options.'''
    clear_screen()
    prompt(
        'Welcome!, please select an alternative:',
        ['Start', 'Rules', 'Options', 'Quit'],
        ['s', 'r', 'o', 'q'],
        [game.start_game, show_rules, show_options, quit_game],
        False,
        arguments=[None, None, game, None]
    )
    clear_screen()
    if game.game_running:
        prompt(
            'Choose an option: ',
            ["Local", "Online"],
            ['l', 'o'],
            [play_local, play_online],
            False
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
