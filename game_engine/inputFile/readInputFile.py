import json

def read_game_state():
    """
    Reads the .json-file containing the game state.
    """
    game_json = open('inputFile.json')
    game_data = json.load(game_json)
    game_struct = {}
    node_info = {}
    
    game_struct = {
        'difficulty': game_data['difficulty'],
        'playerMovesLeft': game_data['playerMovesLeft'],
        'engineMovesLeft': game_data['engineMovesLeft'],
        'placedPlayerPieces': game_data['placedPlayerPieces'],
        'placedEnginePieces': game_data['placedEnginePieces'],
        'onhandPlayerPieces': game_data['onhandPlayerPieces'],
        'onhandEnginePieces': game_data['onhandPlayerPieces'],
        'totalPiecesPerPlayer': game_data['totalPiecesPerPlayer']
    }

    for node in game_data['nodeInfo']:
        if game_data['nodeInfo'][node]['reachableNodes'] != []:
            node_info[node] = game_data['nodeInfo'][node]
    
    game_struct['nodeInfo'] = node_info

    return game_struct
