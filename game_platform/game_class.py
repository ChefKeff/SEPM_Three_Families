'''
This module consists of the game class which contains
the methods controlling the game logic and order.

(C) 2021 Group G
'''
import sys
import time
sys.path.insert(0, '../')
import json
from game_engine.generateOutputFile import generate_move_create_output
from board_class import Board
from piece_class import Piece
from tools import (
    clear_screen,
    notification,
    boxed_output,
    board_design,
    show_rules,
    validate_game_input,
    check_input_int,
    print_ascii,
    suggest_placement
)


class Game:
    '''
    The Game class controls the logic of the game.
    '''

    def __init__(self, board_structure):
        # Set up game logic
        self.game_done = False
        self.game_score = 0
        self.game_running = False
        self.whose_turn = "white"
        self.stage2 = False
        self.turns = 0
        self.client = None
        self.local_ai = False

        self.white_player = {
            'name': 'White',
            'color': 'white',
            'color_single': 'W',
            'turns': 0,
            'placements': 0,
            'ai_or_online': False,
            'difficulty': None,
        }

        self.black_player = {
            'name': 'Black',
            'color': 'black',
            'color_single': 'B',
            'turns': 0,
            'placements': 0,
            'ai_or_online': False,
            'difficulty': None
        }

        # Online mode
        self.online = False
        self.current_player = None
        

        self.connections = board_structure['connections']

        # Set up rules
        self.max_turns = board_structure['max_turns']
        self.pieces_in_hand = board_structure['pieces_in_hand']

        # Set up board
        self.board = Board(
            board_structure['no_nodes'],
            board_structure['connections'],
            board_structure['possible_mills']
        )
        self.board_to_print = board_design('default')

    # ----------------------- TO JSON ------------------------

    def to_json(self):
        print('#-------------------------------------TO JSON')
        '''Creates a .json file with the game configurations'''
        if not self.white_player['ai_or_online'] and not self.black_player['ai_or_online']:
            return
            
        ai_player = None
        player = None
        if self.white_player['ai_or_online']:
            ai_player = self.white_player
            player = self.black_player
        elif self.black_player['ai_or_online']:
            ai_player = self.black_player
            player = self.white_player

        data = {}
        data['fileType'] = 'GAMEFILE'
        data['difficulty'] = ai_player['difficulty']
        data['playerMovesLeft'] = 100 # TODO: Placeholder, fix this
        data['engineMovesLeft'] = 100 # TODO: Placeholder, fix this

        # TODO: I took for granted white=player, black=ai
        w_count, b_count = self.check_pieces_count()
        
        data['maxTurns'] = self.max_turns # TODO: Should this also exist in game file ?
        data['GAMEDONE'] = 1 if self.game_done else 0
        # TODO: These I'm unsure of:
        data['TPLAYER'] = self.black_player['name'] if self.whose_turn == 'white' else self.white_player['name']
        data['FPLAYER'] = self.white_player['name'] if self.whose_turn == 'white' else self.white_player['name']
        data['TPCOLOUR'] = self.black_player['color_single'] if self.whose_turn == 'white' else self.white_player['color_single']
        data['FPCOLOUR'] = self.white_player['color_single'] if self.whose_turn == 'white' else self.white_player['color_single']
        data['GAMESCORE'] = self.game_score
        # TODO: Guess the following should work, I haven't tried
        data['playerMovesLeft'] = self.max_turns - player['turns']
        data['engineMovesLeft'] = self.max_turns - ai_player['turns']
        data['placedPlayerPieces'] = w_count
        data['placedEnginePieces'] = b_count #outputFile['placedEnginePieces']
        data['onhandPlayerPieces'] = self.pieces_in_hand - player['placements']
        data['onhandEnginePieces'] = self.pieces_in_hand -  ai_player['placements'] #outputFile['onhandEnginePieces'] if outputFile['onhandEnginePieces'] != 11 else 11
        data['totalPiecesPerPlayer'] = self.pieces_in_hand

        # Create a lexicon for the board in order to translate e.g. 10 -> [2, 0]
        list_of_coordinates = []
        for i in range(7):
            if i != 3: # Every row with 3 coordinates
                for j in range(3):
                    list_of_coordinates.append([i,j])
            else:
                for j in range(7): # The middle row with 7 coordinates
                    list_of_coordinates.append([i,j])

        # Translate each connection to [row, column] format 
        list_of_connections = []
        for (i, row) in enumerate(self.connections):
            innerList = []
            for (j, number) in enumerate(row):
                innerList.append(list_of_coordinates[int(number)-1])
            list_of_connections.append(innerList)

        # Append to json file
        data['nodeInfo'] = {}
        for (i, coordinate) in enumerate(list_of_coordinates):
            data['nodeInfo'][str(coordinate)] = {}
            data['nodeInfo'][str(coordinate)]['reachableNodes'] = list_of_connections[i]
            
            piece = self.board.find_piece_by_coords(i+1) # Not exactly sure why I need to add 1 here
            if piece is not None:
                if piece.color == 'white':
                    data['nodeInfo'][str(coordinate)]['marking'] = 'P' if self.black_player['ai_or_online'] else 'E'
                else:
                    data['nodeInfo'][str(coordinate)]['marking'] = 'E' if self.black_player['ai_or_online'] else 'P'
            else:
                data['nodeInfo'][str(coordinate)]['marking'] = 'A'

        with open('../game_platform_input_file.json', 'w') as outfile:
            json.dump(data, outfile)
        print('€€€€€€€€€€€€LEAVING TO JSON')

    # ----------------------------- FROM JSON ------------------------------
    def from_json(self, data=None):
        '''Updates game configuration/information from json/dictionary.'''
        if not self.white_player['ai_or_online'] and not self.black_player['ai_or_online']:
            return
        
        ai_player = None
        player = None
        if self.white_player['ai_or_online']:
            ai_player = self.white_player
            player = self.black_player
        elif self.black_player['ai_or_online']:
            ai_player = self.black_player
            player = self.white_player

        if data is None:
            with open('outputFile.json', 'r') as f:
                data = json.load(f)

        nodeList = self.board.node_list
        nodeInfo = data['nodeInfo']
        for (i, node) in enumerate(nodeInfo):
            if nodeInfo[node]['marking'] == 'P':
                if nodeList[i]['piece'] is None:
                    nodeList[i]['piece'] = Piece(player['color'])
                else:
                    nodeList[i]['piece'].color = player['color']
            elif nodeInfo[node]['marking']  == 'E': 
                if nodeList[i]['piece'] is None:
                    nodeList[i]['piece'] = Piece(ai_player['color'])
                else:
                    nodeList[i]['piece'].color = ai_player['color']
            else:
                nodeList[i]['piece'] = None
    
    # ----------------------------- START GAME ------------------------------
    def start_game(self):
        '''Starts the game.'''
        self.game_running = True

    # ----------------------------- TOGGLE ONLINE ----------------------------
    def set_online(self):
        '''Toggles the online mode attribute.'''
        self.toggle_online = True

    # ----------------------------- TOGGLE ONLINE ----------------------------
    def set_local_ai(self):
        '''Toggles the local ai attribute.'''
        self.local_ai = True

    # ----------------------------- SET CLIENT -------------------------------
    def set_client(self, client):
        '''Sets client for game.'''
        self.client = client
    # --------------------------SET CURRENT PLAYER----------------------------
    def set_current_player(self, color):
        '''Toggles the online mode attribute.'''
        self.current_player = self.white_player if color.lower() == 'white' else self.black_player

    # ------------------------------- STOP GAME ------------------------------
    def stop_game(self):
        '''Starts the game.'''
        self.game_running = False

    # ------------------------------ SETUP NAMES -----------------------------
    def setup_player(self, color, name, ai_or_online, difficulty):
        '''Starts the game.'''
        if color.lower() == 'white':
            self.white_player['name'] = name
            if ai_or_online:
                self.white_player['ai_or_online'] = True
                self.white_player['difficulty'] = difficulty
        elif color.lower() == 'black':
            self.black_player['name'] = name
            if ai_or_online:
                self.black_player['ai_or_online'] = True
                self.black_player['difficulty'] = difficulty

    # ----------------------------- PRINT BOARD ------------------------------
    def print_board(self):
        '''Prints the board.'''
        self.board.display_board(self.board_to_print)

    # ----------------------------- CHANGE TURN ------------------------------

    def change_turn(self, color):
        '''Change player turn and increments turns.'''
        self.turns += 1

        # In order to keep track of turns each player has made
        # TODO: Does this look valid? Hasn't tested yet.
        if color == 'white':
            self.black_player['turns'] += 1
        elif color == 'black':
            self.white_player['turns'] += 1

        self.whose_turn = color

    # ----------------------------- PIECE COUNT ------------------------------

    def check_pieces_count(self):
        '''Checks how many pieces each player has.'''
        node_list = self.board.node_list
        w_count = 0
        b_count = 0

        for node in node_list:
            if node['piece'] is not None:
                if node['piece'].color == "white":
                    w_count += 1
                elif node['piece'].color == "black":
                    b_count += 1

        return w_count, b_count

    # ----------------------------- INFORMATION OUTPUT ------------------------------

    def game_output(self, message, choices):
        '''
            Combines notification() with check_pieces_count() to output both.
            Also checks for quit, rules and changing board commands.
        '''

        w_count, b_count = self.check_pieces_count()
        answer = notification(
            message,
            choices,
            w_count,
            b_count,
            self.pieces_in_hand,
            self.turns
        )

        if answer == "rules":
            clear_screen()
            show_rules()
        elif answer == "quit":
            clear_screen()
            sys.exit()
        elif answer == 'cyberpunk':
            self.board_to_print = board_design('cyberpunk')
        elif answer == 'normal':
            self.board_to_print = board_design('default')
        else:
            return answer

    # ----------------------------- GAME LOGIC ------------------------------

    def check_draw(self):
        '''Checks for draw.'''
        node_list = self.board.node_list
        stage2 = self.stage2

        # If turns are greater than max turns then it becomes a tie
        if self.max_turns > 0 and self.turns > self.max_turns:
            return True

        if not stage2:
            for node in node_list:
                if node['piece'] is not None:
                    return False
        elif stage2:
            for node in node_list:
                piece = node['piece']

                if piece is not None and piece.color == self.whose_turn:
                    reachable_nodes = node['reachable_nodes']

                    for reachable_node in reachable_nodes:
                        if reachable_node['piece'] is None:
                            return False
        else:
            return True

    def check_draw_and_win(self):
        '''
        Check for win or draw and returns 2 for draw,
        0 for white win, 1 for black win, else -1.
        '''

        draw = self.check_draw()
        if draw:
            return 2

        w_count, b_count = self.check_pieces_count()

        if self.stage2:
            if w_count <= 2:
                return 1
            if b_count <= 2:
                return 0

        return -1

    def game_logics(self, coords):
        '''Function for collecting logic functions that need to be run every loop.'''
        
        self.to_json()
        self.checking_rows(coords)
        check_win = self.check_draw_and_win()


        if check_win == 0:
            self.game_done = True
            self.game_score = 1 # TODO: Should this be 1?
            clear_screen()
            print_ascii('white-victory.txt')
            boxed_output("Press <Enter> to exit game")
            sys.exit()
        elif check_win == 1:
            self.game_done = True
            self.game_score = -1 # TODO: Should this be -1?
            clear_screen()
            print_ascii('black-victory.txt')
            boxed_output("Press <Enter> to exit game")
            sys.exit()
        elif check_win == 2:
            self.game_done = True
            self.game_score = 2 # TODO: Should this be 2?
            clear_screen()
            print_ascii('draw.txt')
            boxed_output("Press <Enter> to exit game")
            sys.exit()

# ----------------------------- THREE IN A ROW  ------------------------------

    def check_valid_removal(self, node_to_remove):
        '''
        Checks whether attempted piece is in a 3-in-a-row
        formation or not, and if so, if that's valid.
        '''

        if self.board.check_for_row(node_to_remove):
            opponent_node_list = []
            for node in self.board.node_list:
                if node['piece'] is not None:
                    if self.whose_turn == "white" and node['piece'].color == "black":
                        opponent_node_list.append(node)
                    elif self.whose_turn == "black" and node['piece'].color == "white":
                        opponent_node_list.append(node)

            all_rows = True
            for node in opponent_node_list:
                if not self.board.check_for_row(node):
                    all_rows = False

            if not all_rows:
                return False

        return True

    def checking_rows(self, coords):
        '''Check whether a player has got 3 in a row with associated actions.'''
        _, node = self.board.find_node_and_index_by_coords(int(coords))

        if (self.whose_turn == 'black' and self.black_player['ai_or_online']) or (self.whose_turn == 'white' and self.white_player['ai_or_online']):
            return
        if self.board.check_for_row(node):
            clear_screen()
            self.print_board()
            piece = node['piece']

            removed_piece = False
            while not removed_piece:
                clear_screen()
                self.print_board()
                response = self.game_output(
                    '3 in a row! You get to remove a piece (' +
                    self.whose_turn+'):',
                    ["Enter piece to remove "]
                )

                if not validate_game_input(response):
                    continue

                _, node = self.board.find_node_and_index_by_coords(
                    int(float(response)))
                if not self.check_valid_removal(node):
                    clear_screen()
                    self.print_board()
                    self.game_output("Piece is in a 3-in-a-row!",
                                    ["Press <Enter> to continue"])
                    continue

                removed_piece = piece.remove_piece(response, self.board)
                if removed_piece:
                    self.to_json()
                    clear_screen()
                    self.print_board()

    # ----------------------------- PLACE PIECE PHASE ------------------------------

    def place_piece_aux(self, color):
        '''Aux function to place_pieces_phase'''
        self.change_turn(color)
        #hantera om det är en människa/spelare online's tur
        if not self.local_ai and ((self.whose_turn == 'white' and self.white_player['ai_or_online']) or (self.whose_turn == 'black' and self.black_player['ai_or_online'])):
            # Lyssna efter game file
            # Uppdatera game board
            listening = True
            while listening:
                with open('../game_platform_input_file.json', 'r', encoding='utf-8') as file:
                    game_state = json.load(file)
                    if self.current_player['name'] in game_state['TPLAYER']:
                        self.from_json(game_state)
                        return
                time.sleep(1)
                print('Listening for placement move')

            if self.whose_turn == 'white':
                self.white_player['placements'] += 1 #TODO: might have to change this
            else:
                self.black_player['placements'] += 1 #TODO: might have to change this

        #hantera om det är en lokal ai's tur
        if self.local_ai and ((self.whose_turn == "black" and self.black_player['ai_or_online']) or (self.whose_turn == "white" and self.white_player['ai_or_online'])):
            print('updating board')
            # Send board to game_engine
            generate_move_create_output()    
            # Update board
            self.from_json()

            if self.whose_turn == 'white':
                self.white_player['placements'] += 1 #TODO: might have to change this
            else:
                self.black_player['placements'] += 1 #TODO: might have to change this
        else:
            piece = Piece(color)

            # Check if placement successful, otherwise ask until placement successful
            placed = False
            while not placed:
                clear_screen()
                self.print_board()
                response = self.game_output(
                    "Enter node to place a piece ("+self.whose_turn + "): ",
                    [suggest_placement(self.board)]
                )

                if not validate_game_input(response):
                    continue

                placed = piece.place_piece(response, self.board)

                clear_screen()
                self.print_board()

            # Sending game state to server
            if self.online:
                self.client.sendFile('../game_platform_input_file.json')

            if color == "white":
                 self.white_player['placements'] += 1
            else:
                 self.black_player['placements'] += 1

            self.game_logics(response)

    def place_pieces_phase(self):
        '''
        Method for the place pieces phase which should keep going
        until everyone has placed 11 pieces each.
        '''
        while self.pieces_in_hand not in ( self.white_player['placements'],  self.black_player['placements']):
            # print board
            clear_screen()
            self.print_board()

            # place black and white piece
            self.place_piece_aux("white")
            clear_screen()
            self.print_board()
            self.place_piece_aux("black")

            # print board after placement
            clear_screen()
            self.print_board()

        self.change_turn("white")
        self.stage2 = True


    # ----------------------------- MOVE PIECE PHASE ------------------------------

    def move_pieces_phase(self):
        '''Method for the move pieces phase.'''
        while True:
            clear_screen()
            self.print_board()
            if self.whose_turn == 'black' and self.black_player['ai_or_online']:
                # Send board to game_engine
                generate_move_create_output()    
                # Update board
                self.from_json() 
            elif self.whose_turn == 'white' and self.white_player['ai_or_online']:
                # Send board to game_engine
                generate_move_create_output()    
                # Update board
                self.from_json() 
            else:
                piece_to_move_coords = self.game_output(
                    "Enter piece to MOVE ("+self.whose_turn + ")",
                    [suggest_placement(self.board)]
                )

                if not validate_game_input(piece_to_move_coords):
                    continue

                if not check_input_int(piece_to_move_coords):
                    boxed_output("Please enter valid input")
                    continue

                piece_to_move = self.board.find_piece_by_coords(
                    piece_to_move_coords
                )

                if piece_to_move is None or piece_to_move.color != self.whose_turn:
                    clear_screen()
                    self.print_board()
                    self.game_output(
                        "You can only move your own pieces!",
                        ["Press <Enter> to continue"]
                    )
                    continue

                clear_screen()
                self.print_board()

                chosen_coords = self.game_output(
                    "Enter node to PLACE piece ("+self.whose_turn + ")",
                    [suggest_placement(self.board)]
                )

                if not validate_game_input(chosen_coords):
                    continue

                if not check_input_int(chosen_coords):
                    boxed_output("Please enter valid input")
                    continue

                _, chosen_node = self.board.find_node_and_index_by_coords(
                    chosen_coords
                )

                if chosen_node is None or chosen_node['piece'] is not None:
                    clear_screen()
                    self.print_board()
                    self.game_output(
                        "You can only move to empty node!",
                        ["Press <Enter> to continue"]
                    )
                    continue

                w_count, b_count = self.check_pieces_count()

                pieces_left = w_count if self.whose_turn == "white" else b_count

                if not piece_to_move.move_piece(
                    piece_to_move_coords,
                    chosen_coords,
                    self.board,
                    pieces_left
                ):
                    continue


            self.game_logics(chosen_coords)

            # Change player turn
            if self.whose_turn == "white":
                self.change_turn("black")
            else:
                self.change_turn("white")

    # ----------------------------- TESTING FUNCTIONS ------------------------------

    def place_pieces_auto(self):
        '''Places all pieces automatically.'''
        # NOTE: range(1, 23) might be troublesome if number of pieces changes
        for i in range(1, 23):
            piece_w = Piece(color="white")
            piece_b = Piece(color="black")

            if i % 2 != 0:
                piece_w.place_piece(i, self.board)
            else:
                piece_b.place_piece(i, self.board)

        self.print_board()
        self.stage2 = True

    def place_pieces_draw(self):
        '''Places pieces in a way to trigger a draw.'''
        for i in range(1, 12):
            piece_w = Piece(color="black")
            piece_w.place_piece(i, self.board)

        for i in range(12, 23):
            piece_b = Piece(color="white")
            piece_b.place_piece(i, self.board)

        self.print_board()
        self.stage2 = True
