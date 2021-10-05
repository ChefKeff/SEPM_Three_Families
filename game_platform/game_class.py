'''
This module consists of the game class which contains
the methods controlling the game logic and order.

(C) 2021 Group G
'''

import sys
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
    # Set up game logic
    whose_turn = "white"
    stage2 = False
    w_placements = 0
    b_placements = 0
    turns = 0

    def __init__(self, board_structure):
        # Set up game logic
        self.game_running = False
        self.whose_turn = "white"
        self.stage2 = False
        self.w_placements = 0
        self.b_placements = 0
        self.turns = 0

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

    # ----------------------------- START GAME ------------------------------
    def start_game(self):
        '''Starts the game.'''
        self.game_running = True

    # ----------------------------- PRINT BOARD ------------------------------
    def print_board(self):
        '''Prints the board.'''
        self.board.display_board(self.board_to_print)

    # ----------------------------- CHANGE TURN ------------------------------

    def change_turn(self, color):
        '''Change player turn and increments turns.'''
        self.turns += 1
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

        self.checking_rows(coords)
        check_win = self.check_draw_and_win()

        if check_win == 0:
            clear_screen()
            print_ascii('white-victory.txt')
            boxed_output("Press <Enter> to exit game")
            sys.exit()
        elif check_win == 1:
            clear_screen()
            print_ascii('black-victory.txt')
            boxed_output("Press <Enter> to exit game")
            sys.exit()
        elif check_win == 2:
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
                    clear_screen()
                    self.print_board()

    # ----------------------------- PLACE PIECE PHASE ------------------------------

    def place_piece_aux(self, color):
        '''Aux function to place_pieces_phase'''
        self.change_turn(color)
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

        if color == "white":
            self.w_placements += 1
        else:
            self.b_placements += 1

        self.game_logics(response)

    def place_pieces_phase(self):
        '''
        Method for the place pieces phase which should keep going
        until everyone has placed 11 pieces each.
        '''
        while self.pieces_in_hand not in (self.w_placements, self.b_placements):
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