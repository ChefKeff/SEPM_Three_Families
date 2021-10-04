'''
This module specifies the board of the game.

(C) 2021 Group G
'''


class Board():
    '''
    The Board class specifies the board of the game.
    '''

    empty_pieces = []
    white_pieces = []
    black_pieces = []

    def __init__(self, number_of_nodes, nodes_to_connect, possible_wins):
        self.number_of_nodes = number_of_nodes
        self.possible_wins = possible_wins
        self.node_list = []

        self.create_node_list(number_of_nodes)
        self.connect_nodes(nodes_to_connect)
        self.create_characters(number_of_nodes)

    # ------------------------ INITIALIZATION FUNCTIONS --------------------------

    def create_node_list(self, num_of_nodes):
        '''Method for creating the node list.'''
        for i in range(num_of_nodes):
            self.node_list.append({
                "coords": i+1,
                "piece": None,
                "reachable_nodes": []
            })

    def connect_nodes(self, nodes_to_connect):
        '''Method for connecting nodes in node_list.'''
        for (i, connecting_nodes) in enumerate(nodes_to_connect):
            for connecting_node in connecting_nodes:
                self.node_list[i]['reachable_nodes'].append(
                    self.node_list[connecting_node-1]
                )

    def create_empty_characters(self, num_of_nodes):
        '''Create the empty characters.'''
        for i in range(1, num_of_nodes + 1):
            if i < 10:
                self.empty_pieces.append('0' + str(i))
            else:
                self.empty_pieces.append(str(i))

    def create_piece_characters(self):
        '''Create the piece characters.'''
        for (i, _) in enumerate(self.empty_pieces):
            self.white_pieces.append(
                '\x1b[1;30;47m' + self.empty_pieces[i] + '\x1b[0m'
            )
            self.black_pieces.append(
                '\x1b[5;37;41m' + self.empty_pieces[i] + '\x1b[0m'
            )

    def create_characters(self, num_of_nodes):
        '''Create all characters for board.'''
        self.create_empty_characters(num_of_nodes)
        self.create_piece_characters()

    # ---------------------------- FIND NODES/PIECES -----------------------------

    def find_node_and_index_by_coords(self, coords):
        '''Method for finding a node and its index by coordinate.'''
        coords = int(coords)

        for i, node in enumerate(self.node_list):
            if node['coords'] == coords:
                return i, node
        return None, None

    def find_piece_by_coords(self, coords):
        '''Method for finding a piece by its coordinates.'''
        coords = int(coords)

        for node in self.node_list:
            if node['coords'] == coords:
                return node['piece']
        return None

    # ----------------------------- THREE IN A ROW ------------------------------

    def check_for_row(self, node):
        '''Method for checking if a node is creating a mill (3 in a row).'''
        if node['piece'] is not None:
            player = node['piece'].color

            for row in self.possible_wins:
                if node['coords'] in row:
                    flag = True
                    for number in row:
                        _, found_node = self.find_node_and_index_by_coords(
                            number
                        )
                        if found_node['piece'] is None or found_node['piece'].color != player:
                            flag = False

                    if flag:
                        return True

        return False

    # ----------------------------- PRINT BOARD  ------------------------------

    def display_board(self, current_board):
        '''Method for displaying the board.'''
        list_to_display = []
        for i, node in enumerate(self.node_list):
            piece = node['piece']
            if piece is None:
                list_to_display.append(self.empty_pieces[i])
            elif piece.color == "white":
                list_to_display.append(self.white_pieces[i])
            else:
                list_to_display.append(self.black_pieces[i])

        print(current_board % tuple(list_to_display))
