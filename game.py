from board import Board
from utils import notation_to_index, index_to_notation


class Game:
    def __init__(self, board=None):
        print(f"Initializing Game with board: {board}")
        self.board = board if board else Board()
        self.current_player = 'white'

    def switch_player(self):
        self.current_player = 'black' if self.current_player == 'white' else 'white'

    def opponent_color(self):
        return 'black' if self.current_player == 'white' else 'white'

    def is_game_over(self):
        """
        Check for checkmate or stalemate.
        """
        if self.board.is_in_check(self.current_player):
            possible_moves = self.board.get_all_possible_moves(self.current_player)
            if not possible_moves:
                print(f"Checkmate! {self.opponent_color()} wins!")
                return True
        else:
            possible_moves = self.board.get_all_possible_moves(self.current_player)
            if not possible_moves:
                print("Stalemate!")
                return True
        return False

    def play_turn(self):
        """
        Handle a single turn in the game.
        """
        valid_move = False
        while not valid_move:
            self.board.display()
            print(f"{self.current_player}'s turn")
            start_notation = input("Enter the position of the piece to move (e.g., 'e2'): ").strip()
            if start_notation.lower() == 'quit':
                print("Game ended by player.")
                exit()
            start_pos = notation_to_index(start_notation)
            if start_pos:
                piece = self.board.get_piece_at(start_pos)
                if piece and piece.color == self.current_player:
                    # Get possible moves for the piece
                    possible_moves = piece.get_possible_moves(start_pos, self.board)
                    # Filter out moves that would leave the king in check
                    legal_moves = []
                    for end_pos in possible_moves:
                        # Simulate the move
                        captured_piece = self.board.get_piece_at(end_pos)
                        self.board.set_piece_at(end_pos, piece)
                        self.board.set_piece_at(start_pos, None)
                        in_check = self.board.is_in_check(self.current_player)
                        # Undo the move
                        self.board.set_piece_at(start_pos, piece)
                        self.board.set_piece_at(end_pos, captured_piece)
                        if not in_check:
                            legal_moves.append(end_pos)
                    if not legal_moves:
                        print("No legal moves available for this piece. Please choose another piece.")
                        continue
                    # Convert legal moves to algebraic notation
                    move_notations = [index_to_notation(row, col) for (row, col) in legal_moves]
                    print(f"Possible moves: {', '.join(move_notations)}")
                    end_notation = input("Enter the position to move to (e.g., 'e4'): ").strip()
                    if end_notation.lower() == 'quit':
                        print("Game ended by player.")
                        exit()
                    end_pos = notation_to_index(end_notation)
                    if end_pos and end_pos in legal_moves:
                        if self.board.move_piece(start_pos, end_pos):
                            valid_move = True
                        else:
                            print("Invalid move. Try again.")
                    else:
                        print("Invalid move. Please choose one of the suggested moves.")
                else:
                    print("No valid piece at that position. Try again.")
            else:
                print("Invalid notation. Use format like 'e2'.")
        self.switch_player()



    def play(self):
        """
        Start the game loop.
        """
        while not self.is_game_over():
            self.play_turn()
        print("Game over!")
