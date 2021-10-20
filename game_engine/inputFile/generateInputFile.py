import random

def create_input_file():
    """
    Create a game_board for testing our engine. The game_board will consist of a bunch of nodes
    and all the nodes that a node is connected to. 

    The output will be a .json-file, with a row describing the difficulty, followed by arrays of the nodes.
    The arrays will be written like
    "[nodex,nodey]" : {"reachableNodes":[[r1x,r1y],[r2x,r2y]], "marking":"P"}
    
    The .json-file also contains some rules in the beginning of the file, including
        - Difficulty
        - amount of player moves left
        - amount of engine moves left
        - amount of placed player pieces
        - amount of placed engine pieces
        - amount of pieces left on player hand
        - amount of pieces left on engine hand 
        - amount of total pieces per player allowed in game
    Where reachableNodes contain all the nodes that the current node is connected to, 
    and marking states wether the node is occupied by a player piece (P), engine piece (E) or is available (A)
    """

   
    row_length = 13                             # row_length - the length of a row of the (initially) quadratic game board
    player_moves_left = 193                     # amount of moves left for the player      
    engine_moves_left = 194                     # moves left for the engine
    placed_player_pieces = 0                    # the number of player pieces that have been placed on the board
    placed_engine_pieces = 0                    # the number of engine pieces that have been placed on the board   
    onhand_player_pieces = 0                    # the number of pieces the engine has on his/her hand
    onhand_engine_pieces = 1                    # the number of pieces the engine has on its hand
    available_player_pieces = 7                 # the number of available player pieces
    available_engine_pieces = 6                 # this dictates which phase of the game we're in, if it's available_player_pieces-1 -> phase 1 if ==available_player_pieces -> phase 2 if ==3 -> phase 3
    total_pieces_per_player = 7                 # total amount of pieces. Will be placed_pieces + onhand_pieces unless a pieces have been removed
    game_board_string = ''                      # the string to be created and sent to the .txt-file
    difficulty = 'medium'                       # the difficulty, to control the move that the engine does
    game_board = []                             # empty arr where the game board will be added
    node_arr = []                               # empty arr to be filled w all the nodes
    for col in range(row_length):               # create node_arr
        for row in range(row_length):
            node = [[col,row]]
            node_arr += node     

    for node in node_arr:                       # check all the reachable nodes from one node, since we loop from top to bottom, we do not need to check upwards
        reachable_nodes = []
        if [node[0]+1, node[1]] in node_arr:
            if random.random() < 0.25:
                if [node[0]+1, node[1]] not in reachable_nodes:
                    reachable_nodes += [[node[0]+1, node[1]]]
        if [node[0]+1,node[1]+1] in node_arr:
             if random.random() < 0.25:
                if [node[0]+1, node[1]+1] not in reachable_nodes:
                    reachable_nodes += [[node[0]+1, node[1]+1]]
        if [node[0],node[1]+1] in node_arr:
             if random.random() < 0.25:
                if [node[0], node[1]+1] not in reachable_nodes:
                    reachable_nodes += [[node[0], node[1]+1]]
        if [node[0]-1,node[1]+1] in node_arr:
             if random.random() < 0.25:
                if [node[0]-1, node[1]+1] not in reachable_nodes:
                    reachable_nodes += [[node[0]-1, node[1]+1]]
        new_node = [[node, reachable_nodes]]
        game_board += new_node
    
    for node in game_board: 
        if node[1] != []:
            for i in range(row_length*row_length):
                for rn in range(len(node[1])):
                    if game_board[i][0] == node[1][rn]:
                        if node[0] not in game_board[i][1]:
                            game_board[i][1] += [node[0]]
                           
    for i in range(row_length*row_length):    
        if game_board[i][1] != []:
            if type(game_board[i][1]) != int:
                if random.random() < 0.15:
                    if placed_player_pieces < available_player_pieces:  # places the player pieces randomly on the board     
                        new_node_w_player = [game_board[i], 1337]
                        game_board[i] = new_node_w_player
                        placed_player_pieces += 1
                if random.random() < 0.15:
                    if placed_engine_pieces < available_engine_pieces:  # places the engine pieces randomly on the board     
                        new_node_w_engine = [game_board[i], 420]
                        game_board[i] = new_node_w_engine
                        placed_engine_pieces += 1

    game_board_string += '{ "difficulty" : "' + difficulty + '" ,' + '\n' + '"playerMovesLeft": ' + str(player_moves_left) + ',\n "engineMovesLeft": ' + str(engine_moves_left) + ', \n"placedPlayerPieces": ' + str(placed_player_pieces) +', \n "placedEnginePieces": ' + str(placed_engine_pieces) + ',\n "onhandPlayerPieces": ' + str(onhand_player_pieces) + ',\n "onhandEnginePieces": ' + str(onhand_engine_pieces) + ', \n "totalPiecesPerPlayer":' + str(total_pieces_per_player) + ', \n "nodeInfo": {' + '\n'

    for i in range(row_length*row_length):                           # creates the string that is to be made into a .json 
        if i == row_length*row_length-1:                             # I'm just now realising there are many ways to do this more easily
            if game_board[i][1] == 1337:                             # but who cares haha, as long as it works, right?
                game_board_string += '"' + str(game_board[i][0][0]) + '": ' + '{"reachableNodes": ' + str(game_board[i][0][1]) + ', "marking": "P" } \n'   
            if game_board[i][1] == 420:
                game_board_string += '"' + str(game_board[i][0][0]) + '": ' + '{"reachableNodes": ' + str(game_board[i][0][1]) + ', "marking": "E" } \n'   
            elif type(game_board[i][1]) != int:
                game_board_string += '"' + str(game_board[i][0]) + '": ' + '{"reachableNodes": ' + str(game_board[i][1]) + ', "marking": "A" } \n' 
        else:
            if game_board[i][1] == 1337:
                game_board_string += '"' + str(game_board[i][0][0]) + '": ' + '{"reachableNodes": ' + str(game_board[i][0][1]) + ', "marking": "P" }, \n'     
            if game_board[i][1] == 420:
                game_board_string += '"' + str(game_board[i][0][0]) + '": ' + '{"reachableNodes": ' + str(game_board[i][0][1]) + ', "marking": "E" }, \n'   
            elif type(game_board[i][1]) != int:
                game_board_string += '"' + str(game_board[i][0]) + '": ' + '{"reachableNodes": ' + str(game_board[i][1]) + ', "marking": "A" }, \n' 
    game_board_string += '} }'
    game_boardFile = open('inputFileTest.json', 'w')     # sends stuff to the .json file :-)
    game_boardFile.write(game_board_string)


create_input_file() 
