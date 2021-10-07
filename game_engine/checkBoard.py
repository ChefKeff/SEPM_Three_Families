from minimax import evaluate

def check_board_state(board: dict(dict(dict())), is_maximizing_player: bool):
"""
Evaluates the board and determines whether the board is a winning or losing board
and changes the gamescore and gamedone parameters.

"""

    value, game_over = evaluate(board, is_maximizing_player)
    
    if game_over:
        if value > 0:
            gamescore = 1
            gamedone = 1
        if value < 0:
            gamescore = -1
            gamedone = 1
    elif not game_over:
        gamescore = 0
        gamedone = 0

    return gamescore, gamedone