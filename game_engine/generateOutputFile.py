
from game_engine.changeCommParams import change_comm_params
from game_engine.minimax import generate_move
import json

""" Given that there is an input file named "inputFile.json" formatted in the correct way in the same
    directory that this script is executed in an output file will be generated representing a new board
    state with one move made by the engine
"""

def generate_move_create_output(file_name:str="outputFile.json"):
    """ Generates a move and writes the corresponding json object to a file
        named "outputFile.json"

        str -- name of the output file
    """
    move = generate_move()
    print('gen output :-)')
    print(move['engineThrees'])
    move = change_comm_params(move)
    json_object = json.dumps(move, indent = 1)
    with open(file_name, 'w') as output_file:
        output_file.write(json_object)
    

if __name__ == '__main__':
    print("Generating output file...")
    generate_move_create_output()
    print("Successfully generated output file")