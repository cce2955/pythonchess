import unittest
from unittest.mock import patch
from io import StringIO
from pieces import Pawn, Knight, Bishop, Rook, Queen, King
from board import Board
from game import Game
from utils import notation_to_index, index_to_notation


class TestUtils(unittest.TestCase):
    def test_notation_to_index(self):
        self.assertEqual(notation_to_index('a8'), (0, 0))
        self.assertEqual(notation_to_index('h1'), (7, 7))
        self.assertEqual(notation_to_index('e4'), (4, 4))
        self.assertIsNone(notation_to_index('i9'))
        self.assertIsNone(notation_to_index('a0'))
        self.assertIsNone(notation_to_index(''))

    def test_index_to_notation(self):
        self.assertEqual(index_to_notation(0, 0), 'a8')
        self.assertEqual(index_to_notation(7, 7), 'h1')
        self.assertEqual(index_to_notation(4, 4), 'e4')
        self.assertIsNone(index_to_notation(-1, 0))
        self.assertIsNone(index_to_notation(8, 8))


class TestPieces(unittest.TestCase):
    def setUp(self):
        # Initialize an empty board for each test
        self.board = Board()
        self.board.grid = [[None for _ in range(8)] for _ in range(8)]  # Empty board
        self.board.set_piece_at(notation_to_index('e1'), King('white'))
        self.board.set_piece_at(notation_to_index('e8'), King('black'))

    def test_pawn_moves(self):
        pawn = Pawn('white')
        self.board.set_piece_at((6, 4), pawn)
        moves = pawn.get_possible_moves((6, 4), self.board)
        expected_moves = [(5, 4), (4, 4)]
        self.assertCountEqual(moves, expected_moves)

    def test_pawn_capture(self):
        pawn = Pawn('white')
        self.board.set_piece_at((6, 4), pawn)
        enemy_pawn1 = Pawn('black')
        enemy_pawn2 = Pawn('black')
        self.board.set_piece_at((5, 3), enemy_pawn1)
        self.board.set_piece_at((5, 5), enemy_pawn2)
        moves = pawn.get_possible_moves((6, 4), self.board)
        expected_moves = [(5, 4), (4, 4), (5, 3), (5, 5)]
        self.assertCountEqual(moves, expected_moves)

    def test_knight_moves(self):
        knight = Knight('white')
        self.board.set_piece_at((4, 4), knight)
        moves = knight.get_possible_moves((4, 4), self.board)
        expected_moves = [
            (2, 3), (2, 5), (3, 2), (3, 6),
            (5, 2), (5, 6), (6, 3), (6, 5)
        ]
        self.assertCountEqual(moves, expected_moves)

    def test_bishop_moves(self):
        bishop = Bishop('white')
        self.board.set_piece_at((4, 4), bishop)
        # Place blocking pieces
        self.board.set_piece_at((2, 2), Pawn('white'))  # Ally
        self.board.set_piece_at((6, 6), Pawn('black'))  # Enemy
        moves = bishop.get_possible_moves((4, 4), self.board)
        expected_moves = [
            (3, 3),
            # (2, 2) blocked by ally
            (5, 5), (6, 6),  # Can capture enemy
            (3, 5), (2, 6), (1, 7),
            (5, 3), (6, 2), (7, 1)
        ]
        self.assertCountEqual(moves, expected_moves)

    def test_rook_moves(self):
        rook = Rook('white')
        self.board.set_piece_at((4, 4), rook)
        self.board.set_piece_at((4, 7), Pawn('white'))  # Ally
        self.board.set_piece_at((1, 4), Pawn('black'))  # Enemy
        moves = rook.get_possible_moves((4, 4), self.board)
        expected_moves = [
            # Horizontal moves
            (4, 5), (4, 6),
            # (4, 7) blocked by ally
            (4, 3), (4, 2), (4, 1), (4, 0),
            # Vertical moves
            (3, 4), (2, 4), (1, 4),  # Can capture enemy at (1, 4)
            # (0, 4) blocked after capturing enemy
            (5, 4), (6, 4)
            # Removed (7, 4)
        ]
        self.assertCountEqual(moves, expected_moves)


    def test_queen_moves(self):
        queen = Queen('white')
        self.board.set_piece_at((4, 4), queen)
        self.board.set_piece_at((2, 4), Pawn('white'))  # Ally
        self.board.set_piece_at((4, 6), Pawn('black'))  # Enemy
        moves = queen.get_possible_moves((4, 4), self.board)
        expected_moves = [
            # Horizontal
            (4, 5), (4, 6),  # Can capture enemy at (4, 6)
            (4, 3), (4, 2), (4, 1), (4, 0),
            # Vertical
            (5, 4), (6, 4),
            (3, 4),
            # (2, 4) blocked by ally
            # Diagonals
            (5, 5), (6, 6), (7, 7),
            (5, 3), (6, 2), (7, 1),
            (3, 3), (2, 2), (1, 1), (0, 0),
            (3, 5), (2, 6), (1, 7)
        ]
        self.assertCountEqual(moves, expected_moves)


    def test_king_moves(self):
        king = King('white')
        self.board.set_piece_at((7, 4), king)
        self.board.set_piece_at((7, 5), Rook('black'))  # Enemy
        self.board.set_piece_at((6, 4), Pawn('white'))  # Ally
        moves = king.get_possible_moves((7, 4), self.board)
        expected_moves = [
            (6, 3), (7, 3), (6, 5), (7, 5)
            # Cannot move to (6, 4) blocked by ally
            # Cannot move to (6, 4) as it's occupied by an ally
        ]
        self.assertCountEqual(moves, expected_moves)

    def test_king_castling(self):
        # Setup for castling
        king = King('white')
        rook_kingside = Rook('white')
        rook_queenside = Rook('white')
        self.board.set_piece_at((7, 4), king)
        self.board.set_piece_at((7, 7), rook_kingside)
        self.board.set_piece_at((7, 0), rook_queenside)
        # Clear squares between king and rooks
        self.board.set_piece_at((7, 5), None)
        self.board.set_piece_at((7, 6), None)
        self.board.set_piece_at((7, 3), None)
        self.board.set_piece_at((7, 2), None)
        moves = king.get_possible_moves((7, 4), self.board)
        expected_moves = [
            # Normal king moves (excluding moves into check)
            (6, 3), (6, 4), (6, 5), (7, 3), (7, 5),
            # Castling moves
            (7, 2),  # Queenside castling
            (7, 6)   # Kingside castling
        ]
        self.assertCountEqual(moves, expected_moves)

    def test_pawn_promotion(self):
        pawn = Pawn('white')
        self.board.set_piece_at((1, 0), pawn)
        with patch('builtins.input', return_value='Q'):
            self.board.move_piece((1, 0), (0, 0))  # Move to 'a1' for promotion
        promoted_piece = self.board.get_piece_at((0, 0))
        self.assertIsInstance(promoted_piece, Queen)

    def test_en_passant(self):
        # Setup for en passant
        white_pawn = Pawn('white')
        black_pawn = Pawn('black')
        self.board.set_piece_at((3, 4), white_pawn)  # White pawn at e5 (3,4)
        self.board.set_piece_at((1, 5), black_pawn)  # Black pawn at f7 (1,5)
        white_pawn.has_moved = True  # Manually set has_moved to True
        
        # Black pawn moves two squares forward to f5 (3,5)
        self.board.last_move = None
        self.board.move_piece((1, 5), (3, 5))
        
        # Now white pawn can capture en passant at f6 (2,5)
        moves = white_pawn.get_possible_moves((3, 4), self.board)
        expected_moves = [(2, 4), (2, 5)]  # e5-e6 and en passant to f6
        self.assertCountEqual(moves, expected_moves)


class TestBoard(unittest.TestCase):
    def test_initial_board_setup(self):
        board = Board()
        # Test that the correct pieces are in their starting positions
        self.assertIsInstance(board.get_piece_at((0, 0)), Rook)
        self.assertIsInstance(board.get_piece_at((7, 4)), King)
        self.assertIsInstance(board.get_piece_at((1, 0)), Pawn)
        self.assertIsNone(board.get_piece_at((4, 4)))

    def test_move_piece(self):
        board = Board()
        pawn = board.get_piece_at((6, 4))
        self.assertTrue(board.move_piece((6, 4), (4, 4)))  # Pawn moves two squares
        self.assertEqual(board.get_piece_at((4, 4)), pawn)
        self.assertIsNone(board.get_piece_at((6, 4)))
        self.assertTrue(pawn.has_moved)

    def test_castling(self):
        board = Board()
        # Clear spaces between king and rook
        board.set_piece_at((7, 5), None)
        board.set_piece_at((7, 6), None)
        king = board.get_piece_at((7, 4))
        rook = board.get_piece_at((7, 7))
        self.assertTrue(board.move_piece((7, 4), (7, 6)))  # Kingside castling
        self.assertIs(board.get_piece_at((7, 6)), king)
        self.assertIs(board.get_piece_at((7, 5)), rook)
        self.assertIsNone(board.get_piece_at((7, 4)))
        self.assertIsNone(board.get_piece_at((7, 7)))
        self.assertTrue(king.has_moved)
        self.assertTrue(rook.has_moved)

    def test_en_passant_capture(self):
        board = Board()
        # Set up the pawns
        white_pawn = Pawn('white')
        black_pawn = Pawn('black')
        board.set_piece_at((3, 3), white_pawn)
        board.set_piece_at((1, 4), black_pawn)
        board.move_piece((1, 4), (3, 4))  # Black pawn moves two squares
        # Now white pawn can capture en passant
        self.assertTrue(board.move_piece((3, 3), (2, 4)))
        self.assertIs(board.get_piece_at((2, 4)), white_pawn)
        self.assertIsNone(board.get_piece_at((3, 3)))
        self.assertIsNone(board.get_piece_at((3, 4)))  # Captured pawn removed


class TestGame(unittest.TestCase):
    def test_checkmate(self):
        game = Game()
        # Perform moves to reach Fool's Mate position
        # 1. f3 e5
        game.board.move_piece((6, 5), (5, 5))  # White pawn f2-f3
        game.current_player = 'black'
        game.board.move_piece((1, 4), (3, 4))  # Black pawn e7-e5
        game.current_player = 'white'
        # 2. g4 Qh4#
        game.board.move_piece((6, 6), (4, 6))  # White pawn g2-g4
        game.current_player = 'black'
        game.board.move_piece((0, 3), (4, 7))  # Black queen d8-h4 (Qh4#)
        game.current_player = 'white'
        # Now check if the game detects checkmate
        self.assertTrue(game.is_game_over())

    def test_stalemate(self):
        game = Game()
        # Clear the board
        game.board.grid = [[None for _ in range(8)] for _ in range(8)]
        # Place the white king at h1 (7, 7)
        white_king = King('white')
        game.board.set_piece_at((7, 7), white_king)
        # Place the black king at f2 (6, 5)
        black_king = King('black')
        game.board.set_piece_at((6, 5), black_king)
        # Place the black queen at g2 (6, 6)
        black_queen = Queen('black')
        game.board.set_piece_at((6, 6), black_queen)
        game.current_player = 'white'
        # Now white has no legal moves but is not in check
        self.assertTrue(game.is_game_over())


class TestPawnPromotion(unittest.TestCase):
    def setUp(self):
        # Initialize an empty board for each test
        self.board = Board()
        self.board.grid = [[None for _ in range(8)] for _ in range(8)]  # Empty board

        # Place the White King at e1
        self.board.set_piece_at(notation_to_index('e1'), King('white'))

        # Place the Black King at e8
        self.board.set_piece_at(notation_to_index('e8'), King('black'))

    def test_pawn_promotion(self):
        pawn = Pawn('white')
        self.board.set_piece_at((1, 0), pawn)  # Place pawn at 'a2'
        with patch('builtins.input', return_value='Q'):
            self.board.move_piece((1, 0), (0, 0))  # Move to 'a1' for promotion
        promoted_piece = self.board.get_piece_at((0, 0))
        self.assertIsInstance(promoted_piece, Queen)

    @patch('builtins.input', side_effect=['e2', 'e4', ''])
    @patch('sys.stdout', new_callable=StringIO)
    def test_move_preview_valid_move(self, mock_stdout, mock_input):
        # Setup the board with a White Pawn at 'e2'
        self.board.set_piece_at(notation_to_index('e2'), Pawn('white'))
        game = Game(board=self.board)
        game.current_player = 'white'
        game.play_turn()
        output = mock_stdout.getvalue()
        self.assertIn("Possible moves: e3, e4", output)
        moved_piece = game.board.get_piece_at(notation_to_index('e4'))
        self.assertIsNotNone(moved_piece)
        self.assertIsInstance(moved_piece, Pawn)
        self.assertEqual(moved_piece.color, 'white')

    @patch('builtins.input', side_effect=['a2', 'a3', 'a2', 'a3', 'a2', 'a3'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_move_preview_no_legal_moves(self, mock_stdout, mock_input):
        # Setup the board with a White Pawn at 'a2' blocked by another White Pawn at 'a3'
        self.board.set_piece_at(notation_to_index('a2'), Pawn('white'))
        self.board.set_piece_at(notation_to_index('a3'), Pawn('white'))  # Blocking pawn
        game = Game(board=self.board)
        game.current_player = 'white'
        game.play_turn()
        output = mock_stdout.getvalue()
        self.assertIn("No legal moves available for this piece", output)



    
    @patch('builtins.input', side_effect=['e2', 'e5', 'e2', 'e4', 'e2', 'e5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_move_preview_invalid_move(self, mock_stdout, mock_input):
        # Setup the board with a White Pawn at 'e2'
        self.board.set_piece_at(notation_to_index('e2'), Pawn('white'))
        game = Game(board=self.board)
        game.current_player = 'white'
        game.play_turn()
        output = mock_stdout.getvalue()
        self.assertIn("Invalid move. Please choose one of the suggested moves.", output)



    @patch('builtins.input', side_effect=['e7', 'e1', 'e2', 'e3', 'e2', 'e4'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_move_preview_opponent_piece(self, mock_stdout, mock_input):
        # Setup the board with a White Pawn at 'e2' and a Black Pawn at 'e7'
        self.board.set_piece_at(notation_to_index('e2'), Pawn('white'))
        self.board.set_piece_at(notation_to_index('e7'), Pawn('black'))
        self.board.set_piece_at(notation_to_index('e1'), King('white'))
        self.board.set_piece_at(notation_to_index('e8'), King('black'))
        game = Game(board=self.board)
        game.current_player = 'white'
        game.play_turn()
        output = mock_stdout.getvalue()
        self.assertIn("No valid piece at that position. Try again.", output)



if __name__ == '__main__':
    unittest.main()
