from minimax import evaluate


def change_comm_params(move):
    current_t_player = move['TPLAYER']
    current_t_col = move['TPCOLOUR']
    move['TPLAYER'] = move['FPLAYER']
    move['FPLAYER'] = current_t_player
    move['TPCOLOUR'] = move['FPCOLOUR']
    move['FPCOLOUR'] = current_t_col

    print(evaluate(move, True))
    (score, win_loss) = evaluate(move, True)
    if score == 0 and win_loss:             # If it's a tie
        move['GAMEDONE'] = 1
        move['GAMESCORE'] = 0
    elif score > 0 and win_loss:            # if the engine won!
        move['GAMEDONE'] = 1
        move['GAMESCORE'] = 1
    elif score < 0 and not win_loss:        # if the player won :(
        move['GAMEDONE'] = 1
        move['GAMESCORE'] = -1
    else:                                   # if the game is not yet done
        move['GAMEDONE'] = 0
        move['GAMESCORE'] = 0
    
    return move