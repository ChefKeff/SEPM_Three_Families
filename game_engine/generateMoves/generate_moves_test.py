import generateMoves
import unittest
import test_cases_moves
import pprint

pp = pprint.PrettyPrinter(indent=4)

class TestGenerateMovesMethods(unittest.TestCase):
    def test_remove_pieces(self):
        test_board, possible_moves = test_cases_moves.remove_pieces()
        find_possible_moves = generateMoves.generate_remove_piece_moves(test_board, 'E')
        self.assertCountEqual(possible_moves, find_possible_moves)
        
    def test_place_pieces(self):
        test_board, possible_moves = test_cases_moves.place_pieces()
        find_possible_moves = generateMoves.generate_place_piece_moves(test_board, 'E')
        self.assertCountEqual(possible_moves, find_possible_moves)

    def test_move_pieces(self):
        test_board, possible_moves = test_cases_moves.move_pieces()
        find_possible_moves = generateMoves.generate_move_piece_moves(test_board, 'E')
        self.assertCountEqual(possible_moves, find_possible_moves)
    
    def test_move_pieces_anywhere(self):
        test_board, possible_moves = test_cases_moves.move_pieces_anywhere()
        find_possible_moves = generateMoves.generate_move_piece_anywhere_moves(test_board, 'E')
        self.assertCountEqual(possible_moves, find_possible_moves)

if __name__ == '__main__':
    unittest.main()
