import json
from game_engine.inputFile.readInputFile import read_game_state
from copy import deepcopy

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
            for i in range(len(board['nodeInfo'][node]['reachableNodes'])-1):
                if type(node) != list:      # if the node happens not to be a list, make it a list
                    node = json.loads(node)      
                if r_nodes[i][0] == node[0]:   # gets rows in the x-axis
                    counter = 0
                    reachable = []  
                    for r_node in r_nodes:
                        if r_node[0] == node[0] and board['nodeInfo'][str(r_node)]['marking'] == marking:
                            counter += 1
                        if counter == 1:
                            reachable = r_node
                            two_in_a_row = True
                        if counter == 2:
                            threes += [[r_node, reachable, node]] 
                if r_nodes[i][1] == node[1]:   # gets rows in the y-axis
                    counter = 0
                    reachable = []  
                    for r_node in r_nodes:
                        if r_node[1] == node[1] and board['nodeInfo'][str(r_node)]['marking'] == marking:
                            counter += 1
                        if counter == 1:
                            reachable = r_node
                            two_in_a_row = True
                        if counter == 2:
                            threes += [[r_node, reachable, node]]
    
    if len(board['engineThrees']) == 0 and len(threes) > 0:
        three_in_a_row = True
    else:
        for three in threes:
            if three not in board['engineThrees']:
                three_in_a_row = True

    if three_in_a_row:    
        print("\nthrees: ")
        print(threes)
        print("\nboard: ")
        print(board['engineThrees'])
    board['engineThrees'] = deepcopy(threes)
            
    return [two_in_a_row, three_in_a_row]