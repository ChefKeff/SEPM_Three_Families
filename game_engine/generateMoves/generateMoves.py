import sys
import os
import pprint

pp = pprint.PrettyPrinter(indent=4)
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
  
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
  
# adding the parent directory to 
# the sys.path.
sys.path.append(parent)

from inputFile.readInputFile import read_game_state
from getPhase import get_phase
from checkRows import check_rows

from copy import deepcopy

def generate_place_piece_moves(board: dict(dict(dict())), turn: str):
    """ Generates all the possible "place piece on board" moves. Returns
        list containing the game states representing those moves.
        
        board -- dictionary describing current board state
        turn -- player we are creating moves for player name
    """
    boards = []
    for node, node_info in board['nodeInfo'].items():
        if node_info['marking'] == 'A':
            #make move on board add board to list
            new_board = deepcopy(board)

            new_board['nodeInfo'][str(node)]['marking'] = turn
            if turn == board['FPLAYER']:
                new_board['placedEnginePieces'] += 1
                new_board['onhandEnginePieces'] -= 1
                new_board['engineMovesLeft'] -= 1 
            elif turn == board['TPLAYER']:
                new_board['placedPlayerPieces'] += 1
                new_board['onhandPlayerPieces'] -= 1
                new_board['playerMovesLeft'] -= 1 

            if check_rows(turn, new_board)[1]:
                new_boards = generate_remove_piece_moves(new_board, turn)
                for new_b in new_boards:
                    boards.append(new_b)
            else:
                boards.append(new_board)
    
    return boards

def generate_move_piece_moves(board: dict(dict(dict())), turn: str):
    """ Generates all the possible "move piece a single step" moves. Returns
        list containing the game states representing those moves.
    
        board -- dictionary describing current board state
        turn -- player we are creating moves for ('P' or 'E')
    """
    boards = []
    for node, node_info in board['nodeInfo'].items():
        if node_info['marking'] == turn:
            for reachable_node in node_info['reachableNodes']:
                if board['nodeInfo'][str(reachable_node)]['marking'] == 'A':
                    new_board = deepcopy(board)
                    
                    # swap places between the other available node and
                    # the currently occupied node
                    new_board['nodeInfo'][str(reachable_node)]['marking'] = turn
                    new_board['nodeInfo'][str(node)]['marking'] = 'A'
                    if turn == board['FPLAYER']:
                        new_board['engineMovesLeft'] -= 1 
                    else:
                        new_board['playerMovesLeft'] -= 1 

                    if check_rows(turn, new_board)[1]:
                        new_boards = generate_remove_piece_moves(new_board, turn)
                        for new_b in new_boards:
                            boards.append(new_b)
                    else:
                        boards.append(new_board)

    return boards

def generate_move_piece_anywhere_moves(board: dict(dict(dict())), turn: str):
    """ Generates all the possible "move piece anywhere" moves. Returns
        list containing the game states representing those moves.

        board -- dictionary describing current board state
        turn -- player we are creating moves for ('P' or 'E')
    """
    boards = []
    for node, node_info in board['nodeInfo'].items():
        if node_info['marking'] == turn:
            for other_node, other_node_info in board['nodeInfo'].items():
                if other_node != node:
                    if other_node_info['marking'] == 'A':
                        new_board = deepcopy(board)
                        
                        # swap places between the other available node and
                        # the currently occupied node
                        new_board['nodeInfo'][str(other_node)]['marking'] = turn
                        new_board['nodeInfo'][str(node)]['marking'] = 'A'
                        if turn == board['FPLAYER']:
                            new_board['engineMovesLeft'] -= 1
                        elif turn == board['TPLAYER']:
                            new_board['playerMovesLeft'] -= 1 

                        if check_rows(turn, new_board)[1]:
                            new_boards = generate_remove_piece_moves(new_board, turn)
                            for new_b in new_boards:
                                boards.append(new_b)
                        else:
                            boards.append(new_board)
    return boards

def generate_remove_piece_moves(board: dict(dict(dict())), turn: str):
    """ Generates all the possible "remove piece" moves. Returns
        list containing the game states representing those moves.

        board -- dictionary describing current board state
        turn -- player we are creating moves for ('P' or 'E')
    """
    boards = []
    opponent = {board['TPLAYER']:board['FPLAYER'], board['FPLAYER']:board['TPLAYER']}
    for node, node_info in board['nodeInfo'].items():
        if node_info['marking'] == opponent[turn]:
            new_board = deepcopy(board)

            # remove indicated by making the piece available
            new_board['nodeInfo'][str(node)]['marking'] = 'A'
            if turn == board['FPLAYER']:
                new_board['placedPlayerPieces'] -= 1
            elif turn == board['TPLAYER']:
                new_board['placedEnginePieces'] -= 1
            boards.append(new_board)
    return boards

def generate_moves(board: dict(dict(dict())), turn: str):
    """ Generates all the possible moves. Returns
        list containing the game states representing those moves.

        board -- dictionary describing current board state
        turn -- player we are creating moves for ('P' or 'E')
    """
    
    phase = get_phase(turn, board)
    moves = []
    if phase == 0:
        moves = []
    elif phase == 1:
        moves = generate_place_piece_moves(board, turn)
    elif phase == 2:
        moves = generate_move_piece_moves(board, turn)
    elif phase == 3:
        moves = generate_move_piece_anywhere_moves(board, turn)

    return moves