import json

def read_game_state():
    """
    Reads the .json-file containing the game state.
    """
    game_json = open('../game_platform_input_file.json')
    #print("game json", game_json)
    game_data = json.load(game_json)
    game_struct = {}
    node_info = {}
    #print("game data", game_data)
    print("tplayer:", game_data['TPLAYER'], "tcolor:", game_data['TPCOLOUR'])
    print("fplayer:", game_data['FPLAYER'], "fcolor:", game_data['FPCOLOUR'])
    game_struct = {
        'fileType': game_data['fileType'],
        'GAMEDONE': game_data['GAMEDONE'],
        'TPLAYER': game_data['TPLAYER'],
        'FPLAYER': game_data['FPLAYER'],
        'TPCOLOUR': game_data['TPCOLOUR'],
        'FPCOLOUR': game_data['FPCOLOUR'],
        'GAMESCORE': game_data['GAMESCORE'],
        'difficulty': game_data['difficulty'],
        'firstMoveDone': game_data['firstMoveDone'],
        'playerMovesLeft': game_data['playerMovesLeft'],
        'engineMovesLeft': game_data['engineMovesLeft'],
        'placedPlayerPieces': game_data['placedPlayerPieces'],
        'placedEnginePieces': game_data['placedEnginePieces'],
        'onhandPlayerPieces': game_data['onhandPlayerPieces'],
        'onhandEnginePieces': game_data['onhandEnginePieces'],
        'totalPiecesPerPlayer': game_data['totalPiecesPerPlayer'],
        'engineThrees': game_data['engineThrees']
    }
    for node in game_data['nodeInfo']:
        if game_data['nodeInfo'][node]['reachableNodes'] != []:
            node_info[node] = game_data['nodeInfo'][node]
    game_struct['nodeInfo'] = node_info
    return game_struct

read_game_state()
