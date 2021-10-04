from checkRows import check_rows
import random
from inputFile.readInputFile import read_game_state
from generateMoves.generateMoves import generate_moves


def determine_move(difficulty: str, worst_board: dict(dict(dict())), best_board: dict(dict(dict()))):
    """ Determines and returns the move to make given the specified difficulty

    difficulty -- string representing difficulty setting
    worst_board -- board representing the worst possible move
    best_board -- board representing the best possible move
    """
    if difficulty == 'easy':
        if random.random() < .9:
            return worst_board
        else:
            return best_board
    elif difficulty == 'medium':
        if random.random() < .5:
            return worst_board
        else:
            return best_board
    elif difficulty == 'hard':
        if random.random() < .1:
            return worst_board
        else:
            return best_board


def generate_move():
    """ Return the move to make given the board read by read_game_state """
    board = read_game_state()
    worst_board, best_board = find_best_move(board)
    move = determine_move(board['difficulty'], worst_board, best_board)
    return move



def minimax(board: dict(dict(dict())), depth: int, is_maximizing_player: bool, alpha: int, beta: int):
    """ Runs the minimax algorithm with alpha beta pruning to find the best possible move value
        given that the search tree has a input depth. returns the value of the move

        board -- the board representing current game state
        depth -- the recursive depth that the minimax algorithm goes down to
        is_maximizing_player -- representing the player currently making a move at a given recursion
        alpha -- alpha value for alpha/beta pruning
        beta -- beta value for alpha/beta pruning
    """
    depth_val = depth
    value, game_over = evaluate(board, is_maximizing_player)
    
    if not depth_val < 3:
        return value - depth_val

    if game_over:
        return value - depth_val

    else: 
        if is_maximizing_player:
            best_value = -1000
            for i, newBoard in enumerate(generate_moves(board, 'E')):
                move_value = minimax(newBoard, depth_val+1, not is_maximizing_player, alpha, beta)
                best_value = max(best_value, move_value)
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break

            return best_value
        else:
            best_value = 1000
            for i, newBoard in enumerate(generate_moves(board, 'P')):
                move_value = minimax(newBoard, depth_val+1, not is_maximizing_player, alpha, beta)
                best_value = min(best_value, move_value)
                beta = min(beta, best_value)
                if beta <= alpha:
                    break

            return best_value

def evaluate(board: dict(dict(dict())), is_maximizing_player: bool):
    """ The evaluate function used in the minimax implementation. looks for rows
        that are close to three in a row and returns a higher value for better
        game states

        board -- representing current game state
        is_maximizing_player -- representing the player currently making a move at a given recursion
    """
    two_in_a_row_max, three_in_a_row_max = check_rows('E', board)[0], check_rows('E', board)[1]
    two_in_a_row_min, three_in_a_row_min = check_rows('P', board)[0], check_rows('P', board)[1]
    # Spelet är oavgjort om båda har slut på drag eller om ingen kan göra nåt.
    if board['playerMovesLeft'] == 0 and board['engineMovesLeft'] == 0:
        return 0, True
    if len(generate_moves(board,'P')) == 0 and len(generate_moves(board,'E')) == 0:
        return 0, True
    if is_maximizing_player:
        # Någon har vunnit om den andra spelaren antingen har 0 på hand och färre än 3 på planen
        # eller inte kan göra ett drag.
        if three_in_a_row_max and board['placedPlayerPieces'] == 3 and board['onhandPlayerPieces'] == 0:
            return 100, True 
        if three_in_a_row_min and board['placedEnginePieces'] == 3 and board['onhandEnginePieces'] == 0:
            return -100, True 

        if three_in_a_row_max:
            return 20, False 
        if two_in_a_row_max:
            return 10, False


    elif not is_maximizing_player:
        # Någon har vunnit om den andra spelaren antingen har 0 på hand och färre än 3 på planen
        # eller inte kan göra ett drag.
        if three_in_a_row_max and board['placedPlayerPieces'] == 3 and board['onhandPlayerPieces'] == 0:
            return 100, True 
        if three_in_a_row_min and board['placedEnginePieces'] == 3 and board['onhandEnginePieces'] == 0:
            return -100, True 

        if three_in_a_row_min:
            return -20, False 
        if two_in_a_row_min:
            return -10, False

    return 0, False

def find_best_move(board: dict(dict(dict()))):
    """ Tries all the possible moves the player can make and returns the 
        ones with the best and worst minimax score

        board -- dictionary describing current board state
    """
    best_value = -1000
    best_move = None
    worst_value = 1000
    worst_move = None

    for move in generate_moves(board, 'E'):
        move_value = minimax(move, 0, False, best_value, worst_value)
        if move_value > best_value:
            best_value = move_value
            best_move = move 
        if move_value < worst_value:
            worst_value = move_value
            worst_move = move

    return worst_move, best_move