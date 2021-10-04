# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, './')


def get_phase(player: str, game_state):
    """
    Gets the phase of either the player or the engine. Returns it as a number.

    player - 'E' for engine 'P' for player
    game_state - board representing current game state
    """
    if player == 'P':
        if game_state['playerMovesLeft'] == 0:
            return 0
        if game_state['placedPlayerPieces'] < game_state['totalPiecesPerPlayer'] and game_state['onhandPlayerPieces'] > 0:
            return 1 
        if game_state['onhandPlayerPieces'] == 0 and game_state['placedPlayerPieces'] > 3:
            return 2
        if game_state['onhandPlayerPieces'] == 0 and game_state['placedPlayerPieces'] == 3:
            return 3
    elif player == 'E':
        if game_state['engineMovesLeft'] == 0:
            return 0
        if game_state['placedEnginePieces'] < game_state['totalPiecesPerPlayer'] and game_state['onhandEnginePieces'] > 0:
            return 1
        if game_state['onhandEnginePieces'] == 0 and game_state['placedEnginePieces'] > 3:
            return 2
        if game_state['onhandEnginePieces'] == 0 and game_state['placedEnginePieces'] == 3:
            return 3

