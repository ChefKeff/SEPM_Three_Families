'''
This module specifies the game pieces.

(C) 2021 Group G
'''

from tools import boxed_output, check_input_int


class Piece:
    '''
    The Piece class represent the nodes of the board that are
    owned by a player.
    '''

    def __init__(self, color):
        self.color = color

    # ----------------------------- PLACE ------------------------------

    def place_piece(self, coords, board):
        '''Method for placing a piece a specific coordinate on the board.'''

        if not check_input_int(coords):
            boxed_output("Please enter valid input")
            return False

        coords = int(coords)

        i, node = board.find_node_and_index_by_coords(coords)
        if node is None:
            boxed_output("Invalid coordinate")
            return False

        if node['piece'] is not None:
            boxed_output("Space is already occupied!")
            return False

        board.node_list[i]['piece'] = self
        return True

    # ----------------------------- REMOVE ------------------------------

    def remove_piece(self, coords, board):
        '''Method for removing a piece from a specific coordinate on the board.'''
        if not check_input_int(coords):
            boxed_output("Please enter valid input")
            return False

        coords = int(coords)

        i, node = board.find_node_and_index_by_coords(coords)
        if node is None:
            boxed_output("Invalid coordinate")
            return False

        if node['piece'] is None:
            boxed_output("Space is empty!")
            return False

        if node['piece'].color == self.color:
            boxed_output(
                "You can only remove the opponent's pieces!")
            return False

        board.node_list[i]['piece'] = None

        return True

    # ----------------------------- MOVE ------------------------------
    def move_piece(self, curr_coords, new_coords, board, pieces_left):
        '''
        Method for moving a piece from a specific coordinate
        to another coordinate on the board.
        '''
        curr_coords_int = check_input_int(curr_coords)
        new_coords_int = check_input_int(new_coords)

        if not curr_coords_int or not new_coords_int:
            boxed_output("Please enter valid input")
            return False

        curr_coords = int(curr_coords)
        new_coords = int(new_coords)

        i_curr, curr_node = board.find_node_and_index_by_coords(
            curr_coords
        )

        if curr_node is None:
            boxed_output("Invalid coordinate")
            return False

        if curr_node['piece'] is None:
            boxed_output("Space is empty!")
            return False

        i_new, new_node = board.find_node_and_index_by_coords(
            new_coords
        )

        if new_node is None:
            boxed_output("Invalid coordinate!")
            return False

        if pieces_left > 3:
            reachable_nodes = curr_node['reachable_nodes']
            node_reachable = False
            for node in reachable_nodes:
                if new_node['coords'] == node['coords']:
                    node_reachable = True

            if not node_reachable:
                boxed_output("Node not reachable")
                return False

        if new_node['piece'] is not None:
            boxed_output("Space is already occupied!")
            return False

        board.node_list[i_curr]['piece'] = None
        board.node_list[i_new]['piece'] = self

        return True
