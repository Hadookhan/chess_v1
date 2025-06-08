# backend/GameWrapper.py
import chess
import chess.engine
from backend.engine.Logic import Chess, board
from backend.engine.get_platform import get_stockfish_binary

class GameWrapper:
    def __init__(self):
        self.game = Chess(board)
    
    def get_board(self):
        return self.game.board
    
    def make_move(self, pos1, pos2):
        self.game.move(pos1, pos2)
        return self.get_board()
    
    def undo(self):
        self.game.undo()
        return self.get_board()

    def get_fen(self):
        return self.game.custom_board_to_fen(self.game.board)

    def get_stockfish_move(self):
        board_fen = self.get_fen()
        chess_board = chess.Board(board_fen)

        engine = chess.engine.SimpleEngine.popen_uci(get_stockfish_binary())
        result = engine.play(chess_board, chess.engine.Limit(time=0.1))
        engine.quit()

        move_str = str(result.move)
        return {"from": move_str[:2], "to": move_str[2:]}
