import chess.engine
from backend.engine.Logic import board, Chess
import chess
from backend.engine.get_platform import get_stockfish_binary


def run_game(board=board):
    game = Chess(board)
    engine_on = input("Play with engine? Y/N: ")

    def run_engine(game=game):
        board_fen = game.custom_board_to_fen(board)
        chess_board = chess.Board(board_fen)

        engine = chess.engine.SimpleEngine.popen_uci(get_stockfish_binary())


        info = engine.analyse(chess_board, chess.engine.Limit(time=0.1))

        score = info["score"].white().score(mate_score=10000)
        print(f"Evaluation ({'white' if game.white_to_move else 'black'}):", score)

        result = engine.play(chess_board, chess.engine.Limit(time=0.1))
        print("Best move:", result.move)

        engine.quit()

        return list(str(result.move))

    while True:
        game.show_board()
        if engine_on.upper() == "Y":
            move = run_engine()
        pos1 = input(f"pos1: ")
        if pos1 == "0":
            break
        elif pos1 == "-1":
            game.undo()
        else:
            pos2 = input("pos2: ")
            game.move(pos1, pos2)
            game.show_moves()
    return game