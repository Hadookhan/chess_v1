
board = [
    ["r","n","b","q","k","b","n","r"],
    ["p","p","p","p","p","p","p","p"],
    [".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".","."],
    ["P","P","P","P","P","P","P","P"],
    ["R","N","B","Q","K","B","N","R"]
]

class Node:
    def __init__(self, val, move, next=None, prev=None):
        self.val = val
        self.move = move
        self.next = next
        self.prev = prev

class Chess:

    pos_convert = {
        'a' : 0,
        'b' : 1,
        'c' : 2,
        'd' : 3,
        'e' : 4,
        'f' : 5,
        'g' : 6,
        'h' : 7
    }

    def __init__(self, board=board, white_to_move=True):
        self.board = board
        self.history = [self.copy_board()]
        self.head, self.tail = Node(-1, -1), Node(-1, -1)
        self.head.next, self.tail.prev = self.tail, self.head
        self.move_validators = {
            "p": self.__valid_pawn,
            "n": self.__valid_knight,
            "r": self.__valid_rook_bishop_queen,
            "b": self.__valid_rook_bishop_queen,
            "q": self.__valid_rook_bishop_queen,
            "k": self.__valid_king
        }
        self.white_to_move = white_to_move
        self.en_passant_target = "-"

    def copy_board(self) -> list[list[str]]:
        return [row[:] for row in self.board]

    def __conv_move(self, pos) -> tuple:
        if len(pos) != 2 or pos[0].lower() not in self.pos_convert or not pos[1].isdigit():
            raise ValueError(f"Invalid position format: {pos}")
        col = self.pos_convert[pos[0].lower()]
        row = 8 - int(pos[1])
        return row, col

    def move(self, pos1, pos2) -> None:
        r1, c1 = self.__conv_move(pos1)
        r2, c2 = self.__conv_move(pos2)

        piece = self.board[r1][c1]
        if self.is_valid(pos1, pos2):
            self.board[r1][c1] = "."
            self.board[r2][c2] = piece
            self.history.append(self.copy_board())

            self.white_to_move = not self.white_to_move
        else:
            print("\nINVALID MOVE\n")

    def __update_move(self, val, move):
        new_move = Node(val, move)
        prev = self.tail.prev
        prev.next = self.tail.prev = new_move
        new_move.next, new_move.prev = self.tail, prev

    def is_valid(self, pos1, pos2) -> bool:
        r1, c1 = self.__conv_move(pos1)
        r2, c2 = self.__conv_move(pos2)
        piece = self.board[r1][c1]
        target = self.board[r2][c2]

        validator = self.move_validators.get(piece.lower())
        if validator:
            return validator(pos1, pos2, piece, target, r1, c1, r2, c2) if validator != self.__valid_rook_bishop_queen else validator(pos1, pos2, piece, target)

        return False
        
    def __has_moved(self, square) -> bool:
        for move in self.get_moves():
            if move[0] == square:  # piece moved from this square
                return True
        return False
    
    def __valid_pawn(self, pos1, pos2, piece, target, r1, c1, r2, c2) -> bool:
        direction = -1 if piece.isupper() else 1  # standard 1-step move
        start_row = 6 if piece.isupper() else 1

        # Single forward move
        if c1 == c2 and target == ".":
            if r2 == r1 + direction:
                return self.__move_or_capture(pos1, pos2, piece, target)
            # Double forward from starting row
            if r1 == start_row and r2 == r1 + 2 * direction and self.board[r1 + direction][c1] == ".":
                return self.__move_or_capture(pos1, pos2, piece, target)

        # Diagonal capture
        if abs(c1 - c2) == 1 and r2 == r1 + direction and target != "." and target.islower() != piece.islower():
            return self.__move_or_capture(pos1, pos2, piece, target)
        return False
    
    def to_algebraic(self, row, col) -> str:
        files = list(self.pos_convert.keys())
        return f"{files[col]}{8 - row}"
    
    def __valid_knight(self, pos1, pos2, piece, target, r1, c1, r2, c2) -> bool:
        knight_moves = [
                (2, 1), (1, 2), (-1, 2), (-2, 1),
                (-2, -1), (-1, -2), (1, -2), (2, -1)
            ]
        for dr, dc in knight_moves:
            if (r1 + dr == r2 and c1 + dc == c2) and self.__is_blocked(piece, target) == False:
                return self.__move_or_capture(pos1, pos2, piece, target)
        return False
        
    def __valid_rook_bishop_queen(self, pos1, pos2, piece, target) -> bool:
        if self.__is_blocked(piece, target) or self.__path_is_clear(piece, pos1, pos2) == False:
                return False
            
        return self.__move_or_capture(pos1, pos2, piece, target)
    
    def __valid_king(self, pos1, pos2, piece, target, r1, c1, r2, c2) -> bool:
        king_moves = [
            (1,0), (0,1), (1,1), (1,-1),
            (-1,0), (0,-1), (-1,-1), (-1,1)
        ]

        for dr, dc in king_moves:
            if self.__short_castle(pos1, pos2, piece, target):
                return self.__move_or_capture(pos1, pos2, piece, target, castle_s=True)
            elif self.__long_castle(pos1, pos2, piece, target):
                return self.__move_or_capture(pos1, pos2, piece, target, castle_l=True)
            elif (r1 + dr == r2 and c1 + dc == c2) and self.__is_blocked(piece, target) == False:
                return self.__move_or_capture(pos1, pos2, piece, target)
        return False

    def __is_blocked(self, piece, target) -> bool:
        if (piece.isupper() and target.isupper()) or (piece.islower() and target.islower()):
            return True

        return False
    
    def __path_is_clear(self, piece, pos1, pos2) -> bool:
        r1, c1 = self.__conv_move(pos1)
        r2, c2 = self.__conv_move(pos2)

        if piece.lower() == "r":
            # Horizontal movement
            if r1 == r2:
                step = 1 if c2 > c1 else -1
                for col in range(c1 + step, c2, step):
                    if self.board[r1][col] != ".":
                        return False
                return True

            # Vertical movement
            elif c1 == c2:
                step = 1 if r2 > r1 else -1
                for row in range(r1 + step, r2, step):
                    if self.board[row][c1] != ".":
                        return False
                return True
            return False
        
        if piece.lower() == "b":
            if abs(r1 - r2) != abs(c1 - c2):
                return False
            
            row_step = 1 if r2 > r1 else -1
            col_step = 1 if c2 > c1 else -1
            row, col = r1 + row_step, c1 + col_step

            while row != r2 and col != c2:
                if self.board[row][col] != ".":
                    return False
                row += row_step
                col += col_step
            return True

        if piece.lower() == "q":
            if r1==r2 or c1==c2:
                return self.__path_is_clear("r",pos1,pos2)
            elif abs(r1 - r2) == abs(c1 - c2):
                return self.__path_is_clear("b", pos1, pos2)
            else:
                return False
            
        if piece.lower() == "k":
            if r1==r2:
                step = 1 if c2 > c1 else -1
                for col in range(c1 + step, c2, step):
                    if self.board[r1][col] != ".":
                        return False
                return True
        return False
    
    def __can_castle(self, square: str) -> bool:
        return not self.__has_moved(square)
    
    def __short_castle(self, pos1, pos2, piece, target):
        if piece.lower() != "k" or target != ".":
            return False

        if piece.isupper():  # White
            if pos1 != "e1" or pos2 != "g1":
                return False
            if not self.__can_castle("e1") or not self.__can_castle("h1"):
                return False
            if not self.__path_is_clear(piece, pos1, pos2):
                return False
            # NOTE: Add king safety checks here
            self.board[7][7] = "."
            self.board[7][5] = "R"
            return True

        else:  # Black
            if pos1 != "e8" or pos2 != "g8":
                return False
            if not self.__can_castle("e8") or not self.__can_castle("h8"):
                return False
            if not self.__path_is_clear(piece, pos1, pos2):
                return False
            self.board[0][7] = "."
            self.board[0][5] = "r"
            return True
        
    def __long_castle(self, pos1, pos2, piece, target):
        if piece.lower() != "k" or target != ".":
            return False

        if piece.isupper():  # White
            if pos1 != "e1" or pos2 != "c1":
                return False
            if not self.__can_castle("e1") or not self.__can_castle("a1"):
                return False
            if not self.__path_is_clear(piece, pos1, pos2):
                return False
            # NOTE: Add king safety checks here
            self.board[7][0] = "."
            self.board[7][3] = "R"
            return True

        else:  # Black
            if pos1 != "e8" or pos2 != "c8":
                return False
            if not self.__can_castle("e8") or not self.__can_castle("a8"):
                return False
            if not self.__path_is_clear(piece, pos1, pos2):
                return False
            self.board[0][0] = "."
            self.board[0][3] = "r"
            return True

    
    def __move_or_capture(self, pos1, pos2, piece, target, castle_s=False, castle_l=False) -> bool:
        r1, c1 = self.__conv_move(pos1)
        r2, c2 = self.__conv_move(pos2)
        square = self.to_algebraic(r1, c1)

        if target == ".":
            if piece.lower() == "p":
                print(target)
                self.__update_move((pos1, pos2), pos2)
                return True
            if castle_s:
                print("\nMove: O-O")
                self.__update_move((pos1, pos2), "O-O")
                return True
            if castle_l:
                print("\nMove: O-O-O")
                self.__update_move((pos1, pos2), "O-O-O")
                return True
            print(f"\nMove: {piece.upper()}{pos1[0]}{pos2}")
            self.__update_move((pos1, pos2), f"{piece.upper()}{pos1[0]}{pos2}")
            return True
        elif (target.islower() != piece.islower()):
            if piece.lower() == "p":
                print(f"{square}x{pos2}")
                self.__update_move((pos1, pos2), f"{square}x{pos2}") if self.board[r2][c2][0].lower() == "p" else self.__update_move((pos1, pos2), f"{square}x{target.upper()}{pos2[0]}")
                return True
            print(f"\nMove: {piece.upper()}{pos1[0]}x{pos2}")
            self.__update_move((pos1, pos2), f"{piece.upper()}{pos1[0]}x{pos2}")
            return True
        return False
    
    def undo(self) -> None:
        if len(self.history) > 1:
            prev_move = self.history.pop()  # remove current
            self.board = prev_move

        if self.tail.prev != self.head:
            self.tail.prev = self.tail.prev.prev
            self.tail.prev.next = self.tail

    def show_board(self) -> None:
        print("  a b c d e f g h")
        print(" +----------------")
        for i, row in enumerate(self.board):
            rank = 8 - i  # Chess ranks go from 8 to 1
            row_str = f"{rank}|{' '.join(row)}"
            print(row_str)
        print()

    def show_moves(self) -> None:
        cur = self.head.next
        n = 1
        queue = []

        while cur != self.tail:
            queue.append(cur.move)
            cur = cur.next
        
        for i in range(1, len(queue), 2):
            print(f"{n} | {queue[i-1]} {queue[i]}")
            n+=1
    
    def get_moves(self) -> list:
        cur = self.head.next
        queue = []

        while cur != self.tail:
            queue.append(list(cur.val))
            cur = cur.next
        
        return queue
    
    def __get_castling_rights(self) -> str:
        rights = ""

        # Check white
        if not self.__has_moved("e1"):
            if not self.__has_moved("h1"):
                rights += "K"
            if not self.__has_moved("a1"):
                rights += "Q"

        # Check black
        if not self.__has_moved("e8"):
            if not self.__has_moved("h8"):
                rights += "k"
            if not self.__has_moved("a8"):
                rights += "q"

        return rights if rights else "-"


    def to_fen(self) -> str:
        fen_rows = []

        for row in self.board:
            fen_row = ""
            empty_count = 0
            for square in row:
                if square == ".":
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen_row += str(empty_count)
                        empty_count = 0
                    fen_row += square
            if empty_count > 0:
                fen_row += str(empty_count)
            fen_rows.append(fen_row)

        piece_placement = "/".join(fen_rows)
        side_to_move = "w"  if self.white_to_move else "b"
        castling_rights = self.__get_castling_rights()
        en_passant = self.en_passant_target
        halfmove_clock = "0"
        fullmove_number = "1"

        return f"{piece_placement} {side_to_move} {castling_rights} {en_passant} {halfmove_clock} {fullmove_number}"

    def custom_board_to_fen(self, board, white_to_move=True):
        white_to_move = self.white_to_move
        fen_rows = []
        for row in board:
            empty = 0
            fen_row = ""
            for piece in row:
                if piece == ".":
                    empty += 1
                else:
                    if empty > 0:
                        fen_row += str(empty)
                        empty = 0
                    fen_row += piece
            if empty > 0:
                fen_row += str(empty)
            fen_rows.append(fen_row)
        board_part = "/".join(fen_rows)
        turn_part = "w" if white_to_move else "b"
        return f"{board_part} {turn_part} - - 0 1"

