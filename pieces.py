# pieces.py

class Piece:
    def __init__(self, color):
        self.color = color  # 'white' or 'black'
        self.symbol = ' '   # Will be set in subclasses
        self.has_moved = False  # Track if the piece has moved (for special moves)

    def get_possible_moves(self, position, board):
        """
        Calculate all possible moves for this piece.
        Should be overridden by subclasses.
        """
        raise NotImplementedError

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'P' if color == 'white' else 'p'

    def get_possible_moves(self, position, board):
        moves = []
        row, col = position
        direction = -1 if self.color == 'white' else 1

        # One square forward
        forward_pos = (row + direction, col)
        if board.is_empty(forward_pos):
            moves.append(forward_pos)
            # Two squares forward from starting position
            if not self.has_moved:
                two_forward_pos = (row + 2 * direction, col)
                if board.is_empty(two_forward_pos):
                    moves.append(two_forward_pos)

        # Captures
        for dc in [-1, 1]:
            new_col = col + dc
            if 0 <= new_col < 8:
                capture_pos = (row + direction, new_col)
                if 0 <= capture_pos[0] < 8:
                    target_piece = board.get_piece_at(capture_pos)
                    if target_piece and target_piece.color != self.color:
                        moves.append(capture_pos)
                    else:
                        # En passant capture
                        # Check if last move was a pawn moving two squares to adjacent file
                        # En passant capture
                        if board.last_move:
                            last_piece, last_start, last_end = board.last_move
                            if isinstance(last_piece, Pawn) and last_piece.color != self.color:
                                if abs(last_end[0] - last_start[0]) == 2:
                                    if last_end[0] == row and last_end[1] == new_col:
                                        en_passant_pos = (row + direction, new_col)
                                        moves.append(en_passant_pos)

        return moves

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'N' if color == 'white' else 'n'

    def get_possible_moves(self, position, board):
        moves = []
        row, col = position
        offsets = [
            (-2, -1), (-2, 1),
            (-1, -2), (-1, 2),
            (1, -2),  (1, 2),
            (2, -1),  (2, 1)
        ]
        for dr, dc in offsets:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_pos = (new_row, new_col)
                if board.is_empty(target_pos) or board.is_enemy_piece(target_pos, self.color):
                    moves.append(target_pos)
        return moves

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'B' if color == 'white' else 'b'

    def get_possible_moves(self, position, board):
        return self._get_linear_moves(position, board, [(-1, -1), (-1, 1), (1, -1), (1, 1)])

    def _get_linear_moves(self, position, board, directions):
        moves = []
        row, col = position
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target_pos = (new_row, new_col)
                if board.is_empty(target_pos):
                    moves.append(target_pos)
                elif board.is_enemy_piece(target_pos, self.color):
                    moves.append(target_pos)
                    break
                else:  # Own piece blocks the path
                    break
                new_row += dr
                new_col += dc
        return moves

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'R' if color == 'white' else 'r'

    def get_possible_moves(self, position, board):
        return self._get_linear_moves(position, board, [(-1, 0), (1, 0), (0, -1), (0, 1)])

    def _get_linear_moves(self, position, board, directions):
        # Same as in Bishop
        moves = []
        row, col = position
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target_pos = (new_row, new_col)
                if board.is_empty(target_pos):
                    moves.append(target_pos)
                elif board.is_enemy_piece(target_pos, self.color):
                    moves.append(target_pos)
                    break
                else:
                    break
                new_row += dr
                new_col += dc
        return moves

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'Q' if color == 'white' else 'q'

    def get_possible_moves(self, position, board):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1),
                      (-1, 0), (1, 0), (0, -1), (0, 1)]
        return self._get_linear_moves(position, board, directions)

    def _get_linear_moves(self, position, board, directions):
        # Same method as in Bishop and Rook
        moves = []
        row, col = position
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target_pos = (new_row, new_col)
                if board.is_empty(target_pos):
                    moves.append(target_pos)
                elif board.is_enemy_piece(target_pos, self.color):
                    moves.append(target_pos)
                    break
                else:
                    break
                new_row += dr
                new_col += dc
        return moves

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'K' if color == 'white' else 'k'

    def get_possible_moves(self, position, board):
        moves = []
        row, col = position
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),         (0, 1),
                      (1, -1),  (1, 0),  (1, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_pos = (new_row, new_col)
                if not board.is_ally_piece(target_pos, self.color):
                    moves.append(target_pos)

        # Castling
        if not self.has_moved and not board.is_in_check(self.color):
            # Kingside castling
            moves.extend(self._get_castling_moves(position, board, kingside=True))
            # Queenside castling
            moves.extend(self._get_castling_moves(position, board, kingside=False))
        return moves

    def _get_castling_moves(self, position, board, kingside):
        moves = []
        row, col = position
        if kingside:
            rook_col = 7
            step = 1
        else:
            rook_col = 0
            step = -1
        rook = board.get_piece_at((row, rook_col))
        if isinstance(rook, Rook) and not rook.has_moved:
            # Check squares between king and rook
            for offset in range(step, step * 3, step):
                check_col = col + offset
                if not board.is_empty((row, check_col)):
                    break
                if board.is_square_attacked((row, check_col), self.color):
                    break
            else:
                # All squares are clear and not under attack
                moves.append((row, col + step * 2))
        return moves
