# utils.py

def notation_to_index(notation):
    """
    Convert algebraic notation to zero-based row and column indices.
    """
    columns = 'abcdefgh'
    rows = '87654321'
    if len(notation) == 2:
        col = columns.find(notation[0])
        row = rows.find(notation[1])
        if 0 <= col < 8 and 0 <= row < 8:
            return row, col
    return None

def index_to_notation(row, col):
    """
    Convert zero-based row and column indices to algebraic notation.
    """
    columns = 'abcdefgh'
    rows = '87654321'
    if 0 <= col < 8 and 0 <= row < 8:
        return f"{columns[col]}{rows[row]}"
    return None
