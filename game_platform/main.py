'''
This is the main module running the game.

(C) 2021 Group G
'''

import sys
import json
from tools import prompt, clear_screen, show_rules, print_ascii
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

def go_back():
    '''Makes user go back from ai difficulty (really fast fix).'''
    return

def show_ai_options(game):
    '''Shows AI options.'''
    clear_screen()

    if not game.play_with_ai:
        prompt(
            'AI mode is not active. Do you want to turn it on?',
            ['Yes', 'No', 'Back'],
            ['y', 'n', 'b'],
            [turn_on_ai, go_back, go_back],
            False,
            arguments=[game, None, None]
        )
    
    if game.play_with_ai:
        prompt(
            'AI settings (current setting is '+game.ai_difficulty+'):',
            ['Easy', 'Medium', 'Hard', 'Turn Off', 'Back'],
            ['e', 'm', 'h', 'o', 'b'],
            [set_ai_easy, set_ai_medium, set_ai_hard, turn_off_ai, go_back],
            False,
            arguments=[game, game, game, game, None]
        )


def set_players(game):
    clear_screen()
    print_ascii('logo.txt')
    '''Sets the name of the players of the game.'''
    num_of_players = 10 # TODO: Fix this
    players = []
    for i in range(num_of_players):
        while True:
            print('Enter name of player '+str(i+1)+':')
            name = input()
            
            if len(name) < 3 or len(name) > 10:
                print('> Name of player must be between 3 and 10 characters in length!')
                continue
            players.append(name)
            break

    game.set_players(players)
            
# ------------------------------ START SCREEN ------------------------------

def start_screen(game):
    '''Prints the starting screen and prompts user with options.'''
    clear_screen()
    prompt(
        'Welcome!, please select an alternative:',
        ['Start', 'Rules', 'AI', 'Players', 'Quit'],
        ['s', 'r', 'o', 'p', 'q'],
        [game.start_game, show_rules, show_ai_options, set_players, quit_game],
        False,
        arguments=[None, None, game, game, None]
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
