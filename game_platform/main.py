
'''
This is the main module running the game.

(C) 2021 Group G
'''

import sys
import json
import time
from tools import prompt, clear_screen, show_rules, boxed_output, validate_game_input
from game_class import Game
from communication_platform.Bin import Server, Client


def setup_player(game, color):
    clear_screen()
    
    while True:
        print('>Enter name for ' + color + ' player:\n')
        name = input()
        
        if len(name) < 2 or len(name) > 10:
            boxed_output('Enter a name between 2 and 10 characters.')
            continue

        if color == 'black' and game.white_player['ai_or_online']:
            game.setup_player(color, name, False, None)
            return

        while True:
            ai = input('Is this an AI? \n Yes(y)    No(n) \n')

            if ai.lower() == 'y' or ai.lower() == 'yes':
                game.set_local_ai()
                while True:
                    difficulty = input('Which difficulty \n Easy(e)    Medium(m)    Hard(h) \n')
                    if difficulty.lower() == 'e' or difficulty.lower() == 'm' or difficulty.lower() == 'h':
                        if difficulty.lower() == 'e':
                            difficulty = 'easy'
                        elif difficulty.lower() == 'm':
                            difficulty = 'medium'
                        elif difficulty.lower() == 'h':
                            difficulty = 'hard'
                        game.setup_player(color, name, True, difficulty)
                        return      
                    else:    
                        boxed_output('Please enter easy(e), medium(m) or hard(h).')
                        continue
                    
            else:
                game.set_current_player(color)
                game.setup_player(color, name, False, None)
                return
                    

def play_local(game):
    '''Starts game in local mode.'''
    print("Playing Locally")

    # Set up players
    setup_player(game, 'white')
    setup_player(game, 'black')

    # To JSON
    game.to_json()
    

def play_online(game):
    '''Starts game in online mode.'''
    print("Playing Online")

    prompt(
        'Do you want to host or join a game?:',
        ['Host', 'Join'],
        ['h', 'j'],
        [host_game, join_game],
        False,
        arguments=[game, game]
    )
    
def host_game(game):
    '''For hosting a game.'''
    
    game.stop_game()
    Server.host()
    
def get_key(val, my_dict):
    '''Get key by value.'''
    for key, value in my_dict.items():
         if val == value:
             return key
 
    return "key doesn't exist"

def join_game(game):
    '''For joining a game.'''
    name = str(input('Enter player name (without blankspaces): '))
    difficulty = None
    while True:
        ai = input('Is this an AI? \n Yes(y)    No(n) \n')
        if ai.lower() == 'y' or ai.lower() == 'yes':
            while True:
                difficulty = input('Which difficulty \n Easy(e)    Medium(m)   Hard(h) \n')
                if difficulty.lower() == 'e' or difficulty.lower() == 'm' or difficulty.lower() == 'h':
                    if difficulty.lower() == 'e':
                        difficulty = 'easy'
                    elif difficulty.lower() == 'm':
                        difficulty = 'medium'
                    elif difficulty.lower() == 'h':
                        difficulty = 'hard'
                    break_outer = True
                    break
                else:
                    boxed_output('Please enter easy(e), medium(m) or hard(h).')
                    continue
        elif ai.lower() == 'n' or ai.lower() == 'no':
            break
        if break_outer:
            break

    name = name.strip()
    if difficulty is not None:
        name = difficulty + "-" + name
    addr = '127.0.0.1'
    port = int(input('connect to port: '))

    client = Client.Client(addr, port, name)
    game.stop_game()
    game.set_client(client)

    # Says to game class to play online
    game.set_online()

    while True:
        tournament = {}
        try:
            with open('tournamentFile.json', 'r', encoding='utf-8') as file:
                tournament = json.load(file)
            print("whiling")
            if name in tournament['NEXTPLAYERS']:
                print("iffing")
                color = 'white' if tournament['NEXTPLAYERS'][name] == 'W' else 'black'
                opponent_color = 'black' if tournament['NEXTPLAYERS'][name] == 'W' else 'white'
                opponent_name = get_key(opponent_color[0].upper(), tournament['NEXTPLAYERS'])
                if difficulty is not None:
                    game.setup_player(color, name, True, difficulty, True)
                else:
                    game.setup_player(color, name, False, None, False)
                ai_diff = None
                if '-' in opponent_name:
                    ai_diff, ai_name = opponent_name.split('-')

                print(ai_diff)
                if ai_diff is not None:
                    game.setup_player(opponent_color, opponent_name, True,
                                      ai_diff.strip(), True)
                else:
                    game.setup_player(opponent_color, opponent_name, True, 'easy')
                game.set_current_player(color)
                print("in here doing stuff")
                # To json
                
                game.to_json()

                # Start game
                client.sendFile('../game_platform_input_file.json')
                game.start_game()
                return
        except Exception as e:
            print(e)
            print("found no tournamentFILE ")
        time.sleep(1)
        
        
    
    

def quit_game():
    '''Quits the game.'''
    sys.exit()

# ------------------------------ START SCREEN ------------------------------

def start_screen(game):
    '''Prints the starting screen and prompts user with options.'''
    clear_screen()
    prompt(
        'Welcome!, please select an alternative:',
        ['Start', 'Rules', 'Quit'],
        ['s', 'r', 'q'],
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
            arguments=[game, game]
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
