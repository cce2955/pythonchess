# board.py

from pieces import Pawn, Knight, Bishop, Rook, Queen, King

class Board:
    def __init__(self):
        self.grid = self.initialize_board()
        self.last_move = None  # Keep track of the last move for en passant

    def initialize_board(self):
        grid = [[None for _ in range(8)] for _ in range(8)]
        # Place pawns
        for i in range(8):
            grid[1][i] = Pawn('black')
            grid[6][i] = Pawn('white')
        # Place other pieces
        # Black pieces
        grid[0][0] = Rook('black')
        grid[0][7] = Rook('black')
        grid[0][1] = Knight('black')
        grid[0][6] = Knight('black')
        grid[0][2] = Bishop('black')
        grid[0][5] = Bishop('black')
        grid[0][3] = Queen('black')
        grid[0][4] = King('black')
        # White pieces
        grid[7][0] = Rook('white')
        grid[7][7] = Rook('white')
        grid[7][1] = Knight('white')
        grid[7][6] = Knight('white')
        grid[7][2] = Bishop('white')
        grid[7][5] = Bishop('white')
        grid[7][3] = Queen('white')
        grid[7][4] = King('white')
        return grid

    def move_piece(self, start_pos, end_pos):
        """
        Move a piece from start_pos to end_pos, assuming the move is valid.
        """
        piece = self.get_piece_at(start_pos)
        if piece:
            captured_piece = self.get_piece_at(end_pos)
            self.set_piece_at(end_pos, piece)
            self.set_piece_at(start_pos, None)
            # Handle pawn promotion
            if isinstance(piece, Pawn):
                promotion_row = 0 if piece.color == 'white' else 7
                if end_pos[0] == promotion_row:
                    self.promote_pawn(end_pos, piece.color)
            # Update has_moved status
            piece.has_moved = True
            if isinstance(piece, King) and abs(start_pos[1] - end_pos[1]) == 2:
                # Handle castling
                self._castle_rook(piece.color, start_pos, end_pos)
            # Handle en passant capture
            if isinstance(piece, Pawn) and captured_piece is None:
                if start_pos[1] != end_pos[1]:
                    # Capturing en passant
                    capture_row = start_pos[0]
                    captured_pawn_pos = (capture_row, end_pos[1])
                    self.set_piece_at(captured_pawn_pos, None)

            self.last_move = (piece, start_pos, end_pos)
            return True
        else:
            print("No piece at the starting position.")
            return False


    def _castle_rook(self, color, king_start, king_end):
        row = king_start[0]
        if king_end[1] == 6:  # Kingside
            rook_start = (row, 7)
            rook_end = (row, 5)
        elif king_end[1] == 2:  # Queenside
            rook_start = (row, 0)
            rook_end = (row, 3)
        rook = self.get_piece_at(rook_start)
        self.set_piece_at(rook_end, rook)
        self.set_piece_at(rook_start, None)
        rook.has_moved = True

    def promote_pawn(self, position, color):
        while True:
            choice = input("Promote pawn to (Q, R, B, N): ").upper()
            if choice in ['Q', 'R', 'B', 'N']:
                if choice == 'Q':
                    self.set_piece_at(position, Queen(color))
                elif choice == 'R':
                    self.set_piece_at(position, Rook(color))
                elif choice == 'B':
                    self.set_piece_at(position, Bishop(color))
                elif choice == 'N':
                    self.set_piece_at(position, Knight(color))
                break
            else:
                print("Invalid choice. Please choose Q, R, B, or N.")

    def get_piece_at(self, position):
        row, col = position
        if 0 <= row < 8 and 0 <= col < 8:
            return self.grid[row][col]
        return None

    def set_piece_at(self, position, piece):
        row, col = position
        if 0 <= row < 8 and 0 <= col < 8:
            self.grid[row][col] = piece

    def is_empty(self, position):
        return self.get_piece_at(position) is None

    def is_enemy_piece(self, position, color):
        piece = self.get_piece_at(position)
        return piece is not None and piece.color != color

    def is_ally_piece(self, position, color):
        piece = self.get_piece_at(position)
        return piece is not None and piece.color == color

    def is_square_attacked(self, position, color):
        """
        Determine if a square is attacked by any enemy pieces.
        """
        for row in range(8):
            for col in range(8):
                piece = self.get_piece_at((row, col))
                if piece and piece.color != color:
                    # Skip enemy king to prevent infinite recursion
                    if isinstance(piece, King):
                        continue
                    if position in piece.get_possible_moves((row, col), self):
                        return True
        # Check for enemy king separately
        return self.is_adjacent_enemy_king(position, color)
    def is_adjacent_enemy_king(self, position, color):
        """
        Check if the enemy king is adjacent to the given position.
        """
        row, col = position
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    piece = self.get_piece_at((new_row, new_col))
                    if isinstance(piece, King) and piece.color != color:
                        return True
        return False

    def is_in_check(self, color):
        """
        Check if the king of the given color is under attack.
        """
        king_pos = self.find_king(color)
        return self.is_square_attacked(king_pos, color)

    def find_king(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.get_piece_at((row, col))
                if isinstance(piece, King) and piece.color == color:
                    return (row, col)
        return None

    def get_all_possible_moves(self, color):
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.get_piece_at((row, col))
                if piece and piece.color == color:
                    piece_moves = piece.get_possible_moves((row, col), self)
                    for move in piece_moves:
                        # Simulate the move
                        captured_piece = self.get_piece_at(move)
                        self.set_piece_at(move, piece)
                        self.set_piece_at((row, col), None)
                        if not self.is_in_check(color):
                            moves.append(((row, col), move))
                        # Undo the move
                        self.set_piece_at((row, col), piece)
                        self.set_piece_at(move, captured_piece)
        return moves

    def display(self):
        """
        Display the board in the console with colors.
        """
        print("  a b c d e f g h")
        for row_idx, row in enumerate(self.grid):
            print(8 - row_idx, end=' ')
            for col_idx, cell in enumerate(row):
                if cell:
                    symbol = cell.symbol
                    if cell.color == 'white':
                        symbol = f'\033[97m{symbol}\033[0m'  # White pieces
                    else:
                        symbol = f'\033[94m{symbol}\033[0m'  # Black pieces
                else:
                    # Use different background for squares
                    if (row_idx + col_idx) % 2 == 0:
                        symbol = '\033[47m \033[0m'  # Light square
                    else:
                        symbol = '\033[40m \033[0m'  # Dark square
                print(symbol, end=' ')
            print(8 - row_idx)
        print("  a b c d e f g h")
