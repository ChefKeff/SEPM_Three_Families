from game_engine.minimax import evaluate


def change_comm_params(move):
    """
    A function that actually changes the parameters from the COMM-platform
    uses. Quite nice :-)
    """
    (gamescore, gamedone) = check_board_state(move, True)
    t_player_ai = f_player_ai = False
    for diff in ('easy', 'hard', 'medium'):
        if diff in move['TPLAYER']:
            t_player_ai = True
        if diff in move['FPLAYER']:
            f_player_ai = True
    if not (t_player_ai and f_player_ai):
        current_t_player = move['TPLAYER']
        current_t_col = move['TPCOLOUR']
        move['TPLAYER'] = move['FPLAYER']
        move['FPLAYER'] = current_t_player
        move['TPCOLOUR'] = move['FPCOLOUR']
        move['FPCOLOUR'] = current_t_col

    move['GAMESCORE'] = gamescore
    move['GAMEDONE'] = gamedone
        
    return move

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
