
board = [
    ["r","n","b","k","q","b","n","r"],
    ["p","p","p","p","p","p","p","p"],
    [".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".","."],
    ["P","P","P","P","P","P","P","P"],
    ["R","N","B","K","Q","B","N","R"]
]

class Node:
    def __init__(self, val, move, board, next=None, prev=None):
        self.val = val
        self.move = move
        self.board = board
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
        self.head, self.tail = Node(-1, -1, self.copy_board()), Node(-1, -1, [[]])
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

    def move(self, pos1, pos2) -> bool:
        r1, c1 = self.__conv_move(pos1)
        r2, c2 = self.__conv_move(pos2)
        if self.board[r1][c1].isupper() != self.white_to_move:
            print(f"\nINVALID MOVE: {'Whites move' if self.white_to_move else 'Blacks move'}\n")
            return False

        piece = self.board[r1][c1]
        if self.is_valid(pos1, pos2):
            self.white_to_move = not self.white_to_move
            #print(self.__in_check(self.white_to_move))
            self.board[r1][c1] = "."
            self.board[r2][c2] = piece
            print(f"{'Whites Turn' if self.white_to_move else 'Blacks Turn'}")
            return True
        else:
            print("\nINVALID MOVE\n")
            return False

    def __update_move(self, val, move, board):
        new_move = Node(val, move, board)
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
            if pos1 != "d1" or pos2 != "b1":
                return False
            if not self.__can_castle("d1") or not self.__can_castle("a1"):
                return False
            if not self.__path_is_clear(piece, pos1, pos2):
                return False
            # NOTE: Add king safety checks here
            self.board[7][0] = "."
            self.board[7][2] = "R"
            return True

        else:  # Black
            if pos1 != "d8" or pos2 != "b8":
                return False
            if not self.__can_castle("d8") or not self.__can_castle("a8"):
                return False
            if not self.__path_is_clear(piece, pos1, pos2):
                return False
            self.board[0][0] = "."
            self.board[0][2] = "r"
            return True
        
    def __long_castle(self, pos1, pos2, piece, target):
        if piece.lower() != "k" or target != ".":
            return False

        if piece.isupper():  # White
            if pos1 != "d1" or pos2 != "f1":
                return False
            if not self.__can_castle("d1") or not self.__can_castle("h1"):
                return False
            if not self.__path_is_clear(piece, pos1, pos2):
                return False
            # NOTE: Add king safety checks here
            self.board[7][7] = "."
            self.board[7][4] = "R"
            return True

        else:  # Black
            if pos1 != "d8" or pos2 != "f8":
                return False
            if not self.__can_castle("d8") or not self.__can_castle("h8"):
                return False
            if not self.__path_is_clear(piece, pos1, pos2):
                return False
            self.board[0][7] = "."
            self.board[0][4] = "r"
            return True

    def __find_king(self, white=True) -> tuple:
        king = 'K' if white else 'k'
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == king:
                    return row, col
        return None
                
    def __is_square_attacked(self, row, col, attacker_is_white: bool) -> bool:
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece.lower() == ".":
                     continue
                if (piece.isupper() and attacker_is_white) or (piece.islower() and not attacker_is_white):
                    from_pos = self.to_algebraic(r, c)
                    to_pos = self.to_algebraic(row, col)
                    if self.is_valid(from_pos, to_pos):
                        return True
        return False

    def __in_check(self, white: bool) -> bool:
        king_pos = self.__find_king(white)
        if not king_pos:
            return False
        row, col = king_pos
        return self.__is_square_attacked(row, col, not white)

    
    def __move_or_capture(self, pos1, pos2, piece, target, castle_s=False, castle_l=False) -> bool:
        r1, c1 = self.__conv_move(pos1)
        r2, c2 = self.__conv_move(pos2)
        print(r2, c2)
        square = self.to_algebraic(r1, c1)

        if self.__in_check(self.white_to_move):
            print("Check!")

        if target == ".":
            if piece.lower() == "p":
                if self.__pawn_promote(piece, r2, c2):
                    print(f"{square}={self.board[r2][c2].upper()}")
                    self.__update_move((pos1, pos2), f"{square}={self.board[r2][c2].upper()}", self.copy_board())
                else:
                    print(target)
                    self.__update_move((pos1, pos2), pos2, self.copy_board())
                return True
            if castle_s:
                print("\nMove: O-O")
                self.__update_move((pos1, pos2), "O-O", self.copy_board())
                return True
            if castle_l:
                print("\nMove: O-O-O")
                self.__update_move((pos1, pos2), "O-O-O", self.copy_board())
                return True
            print(f"\nMove: {piece.upper()}{pos1[0]}{pos2}")
            self.__update_move((pos1, pos2), f"{piece.upper()}{pos1[0]}{pos2}", self.copy_board())
            return True
        elif (target.islower() != piece.islower()):
            if piece.lower() == "p":
                if self.__pawn_promote(piece, r2, c2):
                    print(f"{square}x{pos2}={self.board[r2][c2].upper()}")
                    self.__update_move((pos1, pos2), f"{square}x{pos2}={self.board[r2][c2].upper()}", self.copy_board())
                else:
                    print(f"{square}x{pos2}")
                    self.__update_move((pos1, pos2), f"{square}x{pos2}", self.copy_board()) if self.board[r2][c2][0].lower() == "p" else self.__update_move((pos1, pos2), f"{square}x{target.upper()}{pos2[0]}", self.copy_board())
                return True
            print(f"\nMove: {piece.upper()}{pos1[0]}x{pos2}")
            self.__update_move((pos1, pos2), f"{piece.upper()}{pos1[0]}x{pos2}", self.copy_board())
            return True
        return False
    
    def undo(self) -> None:

        if self.tail.prev != self.head:
            self.board = self.tail.prev.board
            self.tail.prev = self.tail.prev.prev
            self.tail.prev.next = self.tail
            self.white_to_move = not self.white_to_move

    def show_board(self) -> None:
        print("  a b c d e f g h")
        print(" +----------------")
        for i, row in enumerate(self.board):
            rank = 8 - i  # Chess ranks go from 8 to 1
            row_str = f"{rank}|{' '.join(row)}"
            print(row_str)
        print()

    def show_moves(self) -> list:
        cur = self.head.next
        queue = []
        i = 0
        j = 1

        while cur != self.tail:
            queue.append((cur.move[i], cur.move[j]))
            cur = cur.next
            i += 2
            j += 2
        
        return queue
    
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
        if not self.__has_moved("d1"):
            if not self.__has_moved("h1"):
                rights += "K"
            if not self.__has_moved("a1"):
                rights += "Q"

        # Check black
        if not self.__has_moved("d8"):
            if not self.__has_moved("h8"):
                rights += "k"
            if not self.__has_moved("a8"):
                rights += "q"

        return rights if rights else "-"

    def __pawn_promote(self, pawn, r2, c2) -> bool:
        valid_promotion = ["q", "r", "n", "b"]

        if not self.__is_pawn_promote(pawn, r2):
            return False

        promotion_piece = input("Promotion Piece (q, r, n, b): ").lower()
        if promotion_piece in valid_promotion:
            self.board[r2][c2] = promotion_piece.upper() if pawn.isupper() else promotion_piece.lower()
            return True
        else:
            print(f"'{promotion_piece}' is invalid. Please enter one of: {', '.join(valid_promotion)}")

    
    def __is_pawn_promote(self, pawn, r2):
        if (pawn.isupper() and r2 == 0) or (pawn.islower() and r2 == 7):
            return True
        return False


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

