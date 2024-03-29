class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["--", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "wR", "--", "wR", "--", "wp", "bR", "--"],
            ["--", "wp", "--", "--", "bR", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.move_functions = {'p': self.get_pawn_moves, 'R': self.get_rook_moves, 'N': self.get_knight_moves,
                               'B': self.get_bishop_moves, 'Q': self.get_queen_moves, 'K': self.get_king_moves}

        self.white_to_move = True
        self.moveLog = []

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.moveLog.append(move)
        self.white_to_move = not self.white_to_move

    def undo_move(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

    def get_valid_moves(self):
        return self.get_all_possible_moves()

    def get_all_possible_moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[r][c][1]
                    self.move_functions[piece](r, c, moves)
        return moves

    def get_pawn_moves(self, r, c, moves):
        if self.white_to_move:
            if self.board[r - 1][c] == "--":
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 < 7:
                if self.board[r - 1][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:  # black pawn moves
            if self.board[r + 1][c] == "--":
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 < 7:
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def get_rook_moves(self, r, c, moves):
        if self.white_to_move:
            a = 'w'
            b = 'b'
        else:
            a = 'b'
            b = 'w'
        for i in range(r + 1, 8):  # movement down on column
            if self.board[i][c] == "--":
                moves.append(Move((r, c), (i, c), self.board))
            if self.board[i][c][0] == a:
                moves.append(Move((r, c), (i - 1, c), self.board))
                break
            if self.board[i][c][0] == b:
                moves.append(Move((r, c), (i, c), self.board))
                break
        for i in range(r - 1, -1, -1):  # movement up on column
            if self.board[i][c] == "--":
                moves.append(Move((r, c), (i, c), self.board))
            if self.board[i][c][0] == a:
                moves.append(Move((r, c), (i + 1, c), self.board))
                break
            if self.board[i][c][0] == b:
                moves.append(Move((r, c), (i, c), self.board))
                break
        for i in range(c + 1, 8):  # movement right on row
            if self.board[r][i] == "--":
                moves.append(Move((r, c), (r, i), self.board))
            if self.board[r][i][0] == a:
                moves.append(Move((r, c), (r, i - 1), self.board))
                break
            if self.board[r][i][0] == b:
                moves.append(Move((r, c), (r, i), self.board))
                break

        for i in range(c - 1, -1, -1):  # movement left on row
            if self.board[r][i] == "--":
                moves.append(Move((r, c), (r, i), self.board))
            if self.board[r][i][0] == a:
                moves.append(Move((r, c), (r, i + 1), self.board))
                break
            if self.board[r][i][0] == b:
                moves.append(Move((r, c), (r, i), self.board))
                break

    def get_knight_moves(self, r, c, moves):
        knight_moves = [(r + 2, c + 1), (r + 2, c - 1), (r - 2, c + 1), (r - 2, c - 1),
                        (r + 1, c + 2), (r + 1, c - 2), (r - 1, c + 2), (r - 1, c - 2)]

        a = 'b' if self.white_to_move else 'w'

        for row, col in knight_moves:
            if 0 <= row < 8 and 0 <= col < 8:
                if self.board[row][col] == "--" or self.board[row][col][0] == a:
                    moves.append(Move((r, c), (row, col), self.board))

    def get_bishop_moves(self, r, c, moves):
        pass

    def get_queen_moves(self, r, c, moves):
        pass

    def get_king_moves(self, r, c, moves):
        pass


class Move:
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}

    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]
