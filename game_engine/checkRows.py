import json
from game_engine.inputFile.readInputFile import read_game_state
from copy import deepcopy
from itertools import groupby

def check_rows(marking: str, board: dict(dict(dict()))):
    """ Returns a list containing two booleans that are true if 
    two in a row and three in a row is found on the board

    marking -- 'E' or 'P' for player or engine
    board -- board representing current game state
    """
    two_in_a_row = False
    three_in_a_row = False
    threes = []
    for node in board['nodeInfo']:
        # check all the nodes with two or more neighbors
        if len(board['nodeInfo'][node]['reachableNodes']) >= 2 and board['nodeInfo'][node]['marking'] == marking:
            r_nodes = board['nodeInfo'][node]['reachableNodes']
            x_counter = y_counter = 0
            x_reachable = []  
            y_reachable = []
            for r_node in r_nodes:
                if type(node) != list:      # if the node happens not to be a list, make it a list
                    node = json.loads(node)      
                if r_node[0] == node[0] and board['nodeInfo'][str(r_node)]['marking'] == marking:
                    x_counter += 1
                    if x_counter == 1:
                        x_reachable = r_node
                        two_in_a_row = True
                    if x_counter == 2:
                        if marking == 'E' and [r_node, x_reachable, node] not in threes:
                            threes += [[r_node, x_reachable, node]]
                        else:
                            three_in_a_row = True
                elif r_node[1] == node[1] and board['nodeInfo'][str(r_node)]['marking'] == marking:
                    y_counter += 1
                    if y_counter == 1:
                        y_reachable = r_node
                        two_in_a_row = True
                    if y_counter == 2:
                        if marking == 'E' and [r_node, y_reachable, node] not in threes:
                            threes += [[r_node, y_reachable, node]]
                        else:
                            three_in_a_row = True
                            
    if marking == 'E':
        for three in threes:
            if three not in board['engineThrees']:
                three_in_a_row = True
                break
        board['engineThrees'] = threes


    #board['engineThrees'] = threes
    #if three_in_a_row:    
        #print("\nthrees: ")
        #print(threes)
        #print("\nboard: ")
        #print(board['engineThrees'])
    #print(board['engineThrees'])
            
    return [two_in_a_row, three_in_a_row]