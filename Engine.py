import chess.engine
from Logic import board, Chess
import chess


def run_game(board=board):
    game = Chess(board)
    engine_on = input("Play with engine? Y/N: ")

    def run_engine(game=game):
        board_fen = game.custom_board_to_fen(board)
        chess_board = chess.Board(board_fen)

        engine = chess.engine.SimpleEngine.popen_uci("./stockfish/stockfish-ubuntu-x86-64-avx2")

        info = engine.analyse(chess_board, chess.engine.Limit(time=0.1))

        score = info["score"].white().score(mate_score=10000)
        print(f"Evaluation ({'white' if game.white_to_move == True else 'black'}):", score)

        result = engine.play(chess_board, chess.engine.Limit(time=0.1))
        print("Best move:", result.move)

        engine.quit()

    while True:
        game.show_board()
        if engine_on.upper() == "Y":
            run_engine()
        pos1 = input("pos1: ")
        if pos1 == "0":
            break
        elif pos1 == "-1":
            game.undo()
        else:
            pos2 = input("pos2: ")
            game.move(pos1, pos2)
            game.show_moves()
    return game