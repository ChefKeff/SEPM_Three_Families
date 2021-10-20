
from game_engine.changeCommParams import change_comm_params
from game_engine.minimax import generate_move
from game_engine.minimax import minimax
from game_engine.inputFile.readInputFile import read_game_state
import json

""" Given that there is an input file named "inputFile.json" formatted in the correct way in the same
    directory that this script is executed in an output file will be generated representing a new board
    state with one move made by the engine
"""

def generate_move_create_output(file_name:str="../game_platform_input_file.json"):
    """ Generates a move and writes the corresponding json object to a file
        named "outputFile.json"

        str -- name of the output file
    """
    board = read_game_state()
    tdiff = board['TPLAYER'].split('-')[0]
    fdiff = board['FPLAYER'].split('-')[0]
    
    if ((tdiff == 'easy' or tdiff == 'medium' or tdiff == 'hard') and (fdiff == 'easy' or fdiff == 'medium' or fdiff == 'hard')):
        value = minimax(board, 0, True, False, -1000, 1000)
        if value == 100:
            gamescore = 1
            gamedone = 1
            board['GAMESCORE'] = gamescore
            board['GAMEDONE'] = gamedone
        if value == -100:
            gamescore = -1
            gamedone = 1
            board['GAMESCORE'] = gamescore
            board['GAMEDONE'] = gamedone
        if value == 0:
            gamescore = 0
            gamedone = 1
            board['GAMESCORE'] = gamescore
            board['GAMEDONE'] = gamedone
        json_object = json.dumps(board)
        with open(file_name, 'w') as output_file:
            output_file.write(json_object)
    else:    
        move = generate_move()
        move = change_comm_params(move)
        json_object = json.dumps(move)
        with open(file_name, 'w') as output_file:
            output_file.write(json_object)
        

if __name__ == '__main__':
    print("Generating output file...")
    generate_move_create_output()
    print("Successfully generated output file")
