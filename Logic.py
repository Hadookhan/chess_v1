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

    def __init__(self, board=board):
        self.board = board

    def __conv_move(self, pos):
        col = self.pos_convert[pos[0].lower()]
        row = 8 - int(pos[1])
        return row, col



    def move(self, pos1, pos2):
        r1, c1 = self.__conv_move(pos1)
        r2, c2 = self.__conv_move(pos2)

        piece = self.board[r1][c1]
        if self.__is_valid(pos1, pos2):
            self.board[r1][c1] = "."
            self.board[r2][c2] = piece
        else:
            print("\nINVALID MOVE\n")


    def __is_valid(self, pos1, pos2) -> bool:
        r1, c1 = self.__conv_move(pos1)
        r2, c2 = self.__conv_move(pos2)
        piece = self.board[r1][c1]
        target = self.board[r2][c2]

        if piece.lower() == "p":
            direction = -1 if self.board[r1][c1].isupper() else 1
            if (c1 == c2 and target == "."):
                if r2 == r1 + direction:
                    print(f"{pos1}{piece}{pos2}")
                    return True
            elif c1 == c2 + 1 or c1 == c2 - 1 and target.islower() != piece.islower():
                if r2 == r1 + direction:
                    print(f"{pos1}{piece}x{pos2}{target}")
                    return True
    
        elif piece.lower() == "n":
            knight_moves = [
                (2, 1), (1, 2), (-1, 2), (-2, 1),
                (-2, -1), (-1, -2), (1, -2), (2, -1)
            ]
            for dr, dc in knight_moves:
                if (r1 + dr == r2 and c1 + dc == c2) and self.__is_blocked(piece, target) == False:
                    return self.__move_or_capture(pos1, pos2, piece, target)
            return False
        
        elif piece.lower() == "r":
            if self.__is_blocked(piece, target) and self.__path_is_clear(piece, pos1, pos2) == False:
                return False
            
            return self.__move_or_capture(pos1, pos2, piece, target)
                    
        elif piece.lower() == "b":
            if self.__is_blocked(piece, target) and self.__path_is_clear(piece, pos1, pos2) == False:
                return False
            
            if abs(r1 - r2) != abs(c1 - c2):
                return False
            
            return self.__move_or_capture(pos1, pos2, piece, target)
        
        elif piece.lower() == "q":
            if self.__is_blocked(piece, target) and self.__path_is_clear(piece, pos1, pos2) == False:
                return False
            
            if abs(r1 - r2) != abs(c1 - c2):
                return False
            
            return self.__move_or_capture(pos1, pos2, piece, target)
                
        else:
            return False
        
    def __is_blocked(self, piece, target) -> bool:
        if (piece.isupper() and target.isupper()) or (piece.islower() and target.islower()):
            return True

        return False
    
    def __path_is_clear(self, piece, pos1, pos2) -> bool:
        r1, c1 = self.__conv_move(pos1)
        r2, c2 = self.__conv_move(pos2)

        if piece.lower() == "r" or piece.lower() == "q":
            # Horizontal movement
            if r1 == r2:
                step = 1 if c2 > c1 else -1
                for col in range(c1 + step, c2, step):
                    if self.board[r1][col] != ".":
                        return False

            # Vertical movement
            elif c1 == c2:
                step = 1 if r2 > r1 else -1
                for row in range(r1 + step, r2, step):
                    if self.board[row][c1] != ".":
                        return False
        
        if piece.lower() == "b" or piece.lower() == "q":
            row_step = 1 if r2 > r1 else -1
            col_step = 1 if c2 > c1 else -1

            row, col = r1 + row_step, c1 + col_step
            while row != r2 and col != c2:
                if self.board[row][col] != ".":
                    return False
                row += row_step
                col += col_step

        return True
    
    def __move_or_capture(self, pos1, pos2, piece, target):
        if target == ".":
            print(f"{pos1}{piece}{pos2}")
        elif (target.islower() != piece.islower()):
            print(f"{pos1}{piece}x{pos2}{target}")
        return True



    def show_board(self):
        print("  a b c d e f g h")
        print(" +----------------")
        for i, row in enumerate(self.board):
            rank = 8 - i  # Chess ranks go from 8 to 1
            row_str = f"{rank}|{' '.join(row)}"
            print(row_str)
        print()
