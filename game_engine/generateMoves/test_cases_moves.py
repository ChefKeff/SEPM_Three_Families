def remove_pieces():
    """
        returns a test board and its corresponding possible next
        states given a remove move

    """
    test_board = {
        'placedPlayerPieces': 4,
        'placedEnginePieces': 0,
        'onhandPlayerPieces': 3,
        'onhandEnginePieces': 7,
        "totalPiecesPerPlayer": 7,
        "playerMovesLeft": 1,
        "engineMovesLeft": 2,
        'nodeInfo': {
            '[0, 0]': {'reachableNodes': [], 'marking': 'A'},
            '[1, 0]': {'reachableNodes': [[2,0], [1,1]], 'marking': 'P'},
            '[2, 0]': {'reachableNodes': [[1,0]], 'marking': 'A'},
            '[0, 1]': {'reachableNodes': [], 'marking': 'A'},
            '[1, 1]': {'reachableNodes': [[1,0],[1,2]], 'marking': 'P'},
            '[2, 1]': {'reachableNodes': [], 'marking': 'A'},
            '[0, 2]': {'reachableNodes': [[1,2]], 'marking': 'P'},
            '[1, 2]': {'reachableNodes': [[0,2]], 'marking': 'P'},
            '[2, 2]': {'reachableNodes': [], 'marking': 'A'},
        }
    }

    next_states = [
        {
            'placedPlayerPieces': 3,
            'placedEnginePieces': 0,
            'onhandPlayerPieces': 3,
            'onhandEnginePieces': 7,
            "totalPiecesPerPlayer": 7,
            "playerMovesLeft": 1,
            "engineMovesLeft": 1,
            'nodeInfo': {
                '[0, 0]': {'reachableNodes': [], 'marking': 'A'},
                '[1, 0]': {'reachableNodes': [[2,0], [1,1]], 'marking': 'P'},
                '[2, 0]': {'reachableNodes': [[1,0]], 'marking': 'A'},
                '[0, 1]': {'reachableNodes': [], 'marking': 'A'},
                '[1, 1]': {'reachableNodes': [[1,0],[1,2]], 'marking': 'A'},
                '[2, 1]': {'reachableNodes': [], 'marking': 'A'},
                '[0, 2]': {'reachableNodes': [[1,2]], 'marking': 'P'},
                '[1, 2]': {'reachableNodes': [[0,2]], 'marking': 'P'},
                '[2, 2]': {'reachableNodes': [], 'marking': 'A'},
            }
        },
        {
            'placedPlayerPieces': 3,
            'placedEnginePieces': 0,
            'onhandPlayerPieces': 3,
            'onhandEnginePieces': 7,
            "totalPiecesPerPlayer": 7,
            "playerMovesLeft": 1,
            "engineMovesLeft": 1,
            'nodeInfo': {
                '[0, 0]': {'reachableNodes': [], 'marking': 'A'},
                '[1, 0]': {'reachableNodes': [[2,0], [1,1]], 'marking': 'P'},
                '[2, 0]': {'reachableNodes': [[1,0]], 'marking': 'A'},
                '[0, 1]': {'reachableNodes': [], 'marking': 'A'},
                '[1, 1]': {'reachableNodes': [[1,0],[1,2]], 'marking': 'P'},
                '[2, 1]': {'reachableNodes': [], 'marking': 'A'},
                '[0, 2]': {'reachableNodes': [[1,2]], 'marking': 'A'},
                '[1, 2]': {'reachableNodes': [[0,2]], 'marking': 'P'},
                '[2, 2]': {'reachableNodes': [], 'marking': 'A'},
            }
        },
        {
            'placedPlayerPieces': 3,
            'placedEnginePieces': 0,
            'onhandPlayerPieces': 3,
            'onhandEnginePieces': 7,
            "totalPiecesPerPlayer": 7,
            "playerMovesLeft": 1,
            "engineMovesLeft": 1,
            'nodeInfo': {
            '[0, 0]': {'reachableNodes': [], 'marking': 'A'},
            '[1, 0]': {'reachableNodes': [[2,0], [1,1]], 'marking': 'P'},
            '[2, 0]': {'reachableNodes': [[1,0]], 'marking': 'A'},
            '[0, 1]': {'reachableNodes': [], 'marking': 'A'},
            '[1, 1]': {'reachableNodes': [[1,0],[1,2]], 'marking': 'P'},
            '[2, 1]': {'reachableNodes': [], 'marking': 'A'},
            '[0, 2]': {'reachableNodes': [[1,2]], 'marking': 'P'},
            '[1, 2]': {'reachableNodes': [[0,2]], 'marking': 'A'},
            '[2, 2]': {'reachableNodes': [], 'marking': 'A'},
            }
        },
        {
            'placedPlayerPieces': 3,
            'placedEnginePieces': 0,
            'onhandPlayerPieces': 3,
            'onhandEnginePieces': 7,
            "totalPiecesPerPlayer": 7,
            "playerMovesLeft": 1,
            "engineMovesLeft": 1,
            'nodeInfo': {
            '[0, 0]': {'reachableNodes': [], 'marking': 'A'},
            '[1, 0]': {'reachableNodes': [[2,0], [1,1]], 'marking': 'A'},
            '[2, 0]': {'reachableNodes': [[1,0]], 'marking': 'A'},
            '[0, 1]': {'reachableNodes': [], 'marking': 'A'},
            '[1, 1]': {'reachableNodes': [[1,0],[1,2]], 'marking': 'P'},
            '[2, 1]': {'reachableNodes': [], 'marking': 'A'},
            '[0, 2]': {'reachableNodes': [[1,2]], 'marking': 'P'},
            '[1, 2]': {'reachableNodes': [[0,2]], 'marking': 'P'},
            '[2, 2]': {'reachableNodes': [], 'marking': 'A'},
            },
        },
    ]
    return test_board, next_states


def place_pieces():
    """
        returns a test board and its corresponding possible next
        states given a place move

    """
    test_board = {
        'placedPlayerPieces': 0,
        'placedEnginePieces': 0,
        'onhandPlayerPieces': 7,
        'onhandEnginePieces': 7,
        "totalPiecesPerPlayer": 7,
        "playerMovesLeft": 1,
        "engineMovesLeft": 2,
        'nodeInfo': {
            '[1, 0]': {'reachableNodes': [[2,0], [1,1]], 'marking': 'A'},
            '[2, 0]': {'reachableNodes': [[1,0]], 'marking': 'A'},
            '[1, 1]': {'reachableNodes': [[1,0],[1,2]], 'marking': 'A'},
            '[0, 2]': {'reachableNodes': [[1,2]], 'marking': 'A'},
            '[1, 2]': {'reachableNodes': [[0,2]], 'marking': 'A'},
        }
    }

    next_states = [
        {
            'placedPlayerPieces': 0,
            'placedEnginePieces': 1,
            'onhandPlayerPieces': 7,
            'onhandEnginePieces': 6,
            "totalPiecesPerPlayer": 7,
            "playerMovesLeft": 1,
            "engineMovesLeft": 1,
            'nodeInfo': {
                '[1, 0]': {'reachableNodes': [[2,0], [1,1]], 'marking': 'E'},
                '[2, 0]': {'reachableNodes': [[1,0]], 'marking': 'A'},
                '[1, 1]': {'reachableNodes': [[1,0],[1,2]], 'marking': 'A'},
                '[0, 2]': {'reachableNodes': [[1,2]], 'marking': 'A'},
                '[1, 2]': {'reachableNodes': [[0,2]], 'marking': 'A'},
            }
        },
        {
            'placedPlayerPieces': 0,
            'placedEnginePieces': 1,
            'onhandPlayerPieces': 7,
            'onhandEnginePieces': 6,
            "totalPiecesPerPlayer": 7,
            "playerMovesLeft": 1,
            "engineMovesLeft": 1,
            'nodeInfo': {
            '[1, 0]': {'reachableNodes': [[2,0], [1,1]], 'marking': 'A'},
            '[2, 0]': {'reachableNodes': [[1,0]], 'marking': 'E'},        
            '[1, 1]': {'reachableNodes': [[1,0],[1,2]], 'marking': 'A'},
            '[0, 2]': {'reachableNodes': [[1,2]], 'marking': 'A'},
            '[1, 2]': {'reachableNodes': [[0,2]], 'marking': 'A'},
            }
        },
        {   'placedPlayerPieces': 0,
            'placedEnginePieces': 1,
            'onhandPlayerPieces': 7,
            'onhandEnginePieces': 6,
            "totalPiecesPerPlayer": 7,
            "playerMovesLeft": 1,
            "engineMovesLeft": 1,
            'nodeInfo': {
            '[1, 0]': {'reachableNodes': [[2,0], [1,1]], 'marking': 'A'},
            '[2, 0]': {'reachableNodes': [[1,0]], 'marking': 'A'},
            '[1, 1]': {'reachableNodes': [[1,0],[1,2]], 'marking': 'E'},
            '[0, 2]': {'reachableNodes': [[1,2]], 'marking': 'A'},
            '[1, 2]': {'reachableNodes': [[0,2]], 'marking': 'A'},
            }
        },
        {
            'placedPlayerPieces': 0,
            'placedEnginePieces': 1,
            'onhandPlayerPieces': 7,
            'onhandEnginePieces': 6,
            "totalPiecesPerPlayer": 7,
            "playerMovesLeft": 1,
            "engineMovesLeft": 1,
            'nodeInfo': {
            '[1, 0]': {'reachableNodes': [[2,0], [1,1]], 'marking': 'A'},
            '[2, 0]': {'reachableNodes': [[1,0]], 'marking': 'A'},
            '[1, 1]': {'reachableNodes': [[1,0],[1,2]], 'marking': 'A'},
            '[0, 2]': {'reachableNodes': [[1,2]], 'marking': 'E'},
            '[1, 2]': {'reachableNodes': [[0,2]], 'marking': 'A'},
            }
        },
        {
            'placedPlayerPieces': 0,
            'placedEnginePieces': 1,
            'onhandPlayerPieces': 7,
            'onhandEnginePieces': 6,
            "totalPiecesPerPlayer": 7,
            "playerMovesLeft": 1,
            "engineMovesLeft": 1,
            'nodeInfo': {
            '[1, 0]': {'reachableNodes': [[2,0], [1,1]], 'marking': 'A'},
            '[2, 0]': {'reachableNodes': [[1,0]], 'marking': 'A'},
            '[1, 1]': {'reachableNodes': [[1,0],[1,2]], 'marking': 'A'},
            '[0, 2]': {'reachableNodes': [[1,2]], 'marking': 'A'},
            '[1, 2]': {'reachableNodes': [[0,2]], 'marking': 'E'},
            }
        },
    ]
    return test_board, next_states


def move_pieces():
    """
        returns a test board and its corresponding possible next
        states given a move piece move

    """
    test_board = {
        'placedPlayerPieces': 1,
        'placedEnginePieces': 2,
        'onhandPlayerPieces': 6,
        'onhandEnginePieces': 5,
        "totalPiecesPerPlayer": 7,
        "playerMovesLeft": 1,
        "engineMovesLeft": 2,
        'nodeInfo': {
            '[1, 0]': {'reachableNodes': [[2,0], [1,1]], 'marking': 'E'},
            '[2, 0]': {'reachableNodes': [[1,0]], 'marking': 'A'},
            '[1, 1]': {'reachableNodes': [[1,0],[1,2]], 'marking': 'P'},
            '[0, 2]': {'reachableNodes': [[1,2]], 'marking': 'A'},
            '[1, 2]': {'reachableNodes': [[0,2], [2,1]], 'marking': 'E'},
            '[2, 1]': {'reachableNodes': [[1,2]], 'marking': 'A'},
        }
    }

    next_states = [
       {
        'placedPlayerPieces': 1,
        'placedEnginePieces': 2,
        'onhandPlayerPieces': 6,
        'onhandEnginePieces': 5,
        "totalPiecesPerPlayer": 7,
        "playerMovesLeft": 1,
        "engineMovesLeft": 1,
        'nodeInfo': {
            '[1, 0]': {'reachableNodes': [[2,0], [1,1]], 'marking': 'A'},
            '[2, 0]': {'reachableNodes': [[1,0]], 'marking': 'E'},
            '[1, 1]': {'reachableNodes': [[1,0],[1,2]], 'marking': 'P'},
            '[0, 2]': {'reachableNodes': [[1,2]], 'marking': 'A'},
            '[1, 2]': {'reachableNodes': [[0,2], [2,1]], 'marking': 'E'},
            '[2, 1]': {'reachableNodes': [[1,2]], 'marking': 'A'},
        }
        },
        {
        'placedPlayerPieces': 1,
        'placedEnginePieces': 2,
        'onhandPlayerPieces': 6,
        'onhandEnginePieces': 5,
        "totalPiecesPerPlayer": 7,
        "playerMovesLeft": 1,
        "engineMovesLeft": 1,
        'nodeInfo': {
        '[1, 0]': {'reachableNodes': [[2,0], [1,1]], 'marking': 'E'},
        '[2, 0]': {'reachableNodes': [[1,0]], 'marking': 'A'},
        '[1, 1]': {'reachableNodes': [[1,0],[1,2]], 'marking': 'P'},
        '[0, 2]': {'reachableNodes': [[1,2]], 'marking': 'A'},
        '[1, 2]': {'reachableNodes': [[0,2], [2,1]], 'marking': 'A'},
        '[2, 1]': {'reachableNodes': [[1,2]], 'marking': 'E'},
        }
        },
        {
        'placedPlayerPieces': 1,
        'placedEnginePieces': 2,
        'onhandPlayerPieces': 6,
        'onhandEnginePieces': 5,
        "totalPiecesPerPlayer": 7,
        "playerMovesLeft": 1,
        "engineMovesLeft": 1,
        'nodeInfo': {
        '[1, 0]': {'reachableNodes': [[2,0], [1,1]], 'marking': 'E'},
        '[2, 0]': {'reachableNodes': [[1,0]], 'marking': 'A'},
        '[1, 1]': {'reachableNodes': [[1,0],[1,2]], 'marking': 'P'},
        '[0, 2]': {'reachableNodes': [[1,2]], 'marking': 'E'},
        '[1, 2]': {'reachableNodes': [[0,2], [2,1]], 'marking': 'A'},
        '[2, 1]': {'reachableNodes': [[1,2]], 'marking': 'A'},
        }
        },
    ]
    return test_board, next_states

def move_pieces_anywhere():
    """
        returns a test board and its corresponding possible next
        states given a move piece anywhere move

    """
    test_board = {
        'placedPlayerPieces': 1,
        'placedEnginePieces': 2,
        'onhandPlayerPieces': 6,
        'onhandEnginePieces': 5,
        "totalPiecesPerPlayer": 7,
        "playerMovesLeft": 1,
        "engineMovesLeft": 2,
        'nodeInfo': {
            '[1, 0]': {'reachableNodes': [[2,0], [1,1]], 'marking': 'E'},
            '[2, 0]': {'reachableNodes': [[1,0]], 'marking': 'A'},
            '[1, 1]': {'reachableNodes': [[1,0],[1,2]], 'marking': 'P'},
            '[0, 2]': {'reachableNodes': [[1,2]], 'marking': 'A'},
            '[1, 2]': {'reachableNodes': [[0,2], [2,1]], 'marking': 'E'},
            '[2, 1]': {'reachableNodes': [[1,2]], 'marking': 'A'},
        }
    }

    next_states = [
       {
           'placedPlayerPieces': 1,
        'placedEnginePieces': 2,
        'onhandPlayerPieces': 6,
        'onhandEnginePieces': 5,
        "totalPiecesPerPlayer": 7,
        "playerMovesLeft": 1,
        "engineMovesLeft": 1,
        'nodeInfo': {
            '[1, 0]': {'reachableNodes': [[2,0], [1,1]], 'marking': 'A'},
            '[2, 0]': {'reachableNodes': [[1,0]], 'marking': 'E'},
            '[1, 1]': {'reachableNodes': [[1,0],[1,2]], 'marking': 'P'},
            '[0, 2]': {'reachableNodes': [[1,2]], 'marking': 'A'},
            '[1, 2]': {'reachableNodes': [[0,2], [2,1]], 'marking': 'E'},
            '[2, 1]': {'reachableNodes': [[1,2]], 'marking': 'A'},
        }
        },
        {
            'placedPlayerPieces': 1,
        'placedEnginePieces': 2,
        'onhandPlayerPieces': 6,
        'onhandEnginePieces': 5,
        "totalPiecesPerPlayer": 7,
        "playerMovesLeft": 1,
        "engineMovesLeft": 1,
        'nodeInfo': {
        '[1, 0]': {'reachableNodes': [[2,0], [1,1]], 'marking': 'E'},
        '[2, 0]': {'reachableNodes': [[1,0]], 'marking': 'A'},
        '[1, 1]': {'reachableNodes': [[1,0],[1,2]], 'marking': 'P'},
        '[0, 2]': {'reachableNodes': [[1,2]], 'marking': 'A'},
        '[1, 2]': {'reachableNodes': [[0,2], [2,1]], 'marking': 'A'},
        '[2, 1]': {'reachableNodes': [[1,2]], 'marking': 'E'},
        }
        },
        {
            'placedPlayerPieces': 1,
        'placedEnginePieces': 2,
        'onhandPlayerPieces': 6,
        'onhandEnginePieces': 5,
        "totalPiecesPerPlayer": 7,
        "playerMovesLeft": 1,
        "engineMovesLeft": 1,
        'nodeInfo': {
        '[1, 0]': {'reachableNodes': [[2,0], [1,1]], 'marking': 'E'},
        '[2, 0]': {'reachableNodes': [[1,0]], 'marking': 'A'},
        '[1, 1]': {'reachableNodes': [[1,0],[1,2]], 'marking': 'P'},
        '[0, 2]': {'reachableNodes': [[1,2]], 'marking': 'E'},
        '[1, 2]': {'reachableNodes': [[0,2], [2,1]], 'marking': 'A'},
        '[2, 1]': {'reachableNodes': [[1,2]], 'marking': 'A'},
        }
        },
        {
            'placedPlayerPieces': 1,
        'placedEnginePieces': 2,
        'onhandPlayerPieces': 6,
        'onhandEnginePieces': 5,
        "totalPiecesPerPlayer": 7,
        "playerMovesLeft": 1,
        "engineMovesLeft": 1,
        'nodeInfo': {
        '[1, 0]': {'reachableNodes': [[2,0], [1,1]], 'marking': 'A'},
        '[2, 0]': {'reachableNodes': [[1,0]], 'marking': 'A'},
        '[1, 1]': {'reachableNodes': [[1,0],[1,2]], 'marking': 'P'},
        '[0, 2]': {'reachableNodes': [[1,2]], 'marking': 'A'},
        '[1, 2]': {'reachableNodes': [[0,2], [2,1]], 'marking': 'E'},
        '[2, 1]': {'reachableNodes': [[1,2]], 'marking': 'E'},
        }
        },
        {
            'placedPlayerPieces': 1,
        'placedEnginePieces': 2,
        'onhandPlayerPieces': 6,
        'onhandEnginePieces': 5,
        "totalPiecesPerPlayer": 7,
        "playerMovesLeft": 1,
        "engineMovesLeft": 1,
        'nodeInfo': {
        '[1, 0]': {'reachableNodes': [[2,0], [1,1]], 'marking': 'A'},
        '[2, 0]': {'reachableNodes': [[1,0]], 'marking': 'A'},
        '[1, 1]': {'reachableNodes': [[1,0],[1,2]], 'marking': 'P'},
        '[0, 2]': {'reachableNodes': [[1,2]], 'marking': 'E'},
        '[1, 2]': {'reachableNodes': [[0,2], [2,1]], 'marking': 'E'},
        '[2, 1]': {'reachableNodes': [[1,2]], 'marking': 'A'},
        }
        },
        {
            'placedPlayerPieces': 1,
        'placedEnginePieces': 2,
        'onhandPlayerPieces': 6,
        'onhandEnginePieces': 5,
        "totalPiecesPerPlayer": 7,
        "playerMovesLeft": 1,
        "engineMovesLeft": 1,
        'nodeInfo': {
        '[1, 0]': {'reachableNodes': [[2,0], [1,1]], 'marking': 'E'},
        '[2, 0]': {'reachableNodes': [[1,0]], 'marking': 'E'},
        '[1, 1]': {'reachableNodes': [[1,0],[1,2]], 'marking': 'P'},
        '[0, 2]': {'reachableNodes': [[1,2]], 'marking': 'A'},
        '[1, 2]': {'reachableNodes': [[0,2], [2,1]], 'marking': 'A'},
        '[2, 1]': {'reachableNodes': [[1,2]], 'marking': 'A'},
        }
        }
    ]
    return test_board, next_states