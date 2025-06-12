from engine.GameWrapper import GameWrapper
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://www.hadi-khan-chess.com"])

game = GameWrapper()

@app.route("/api/board", methods=["GET"])
def get_board():
    return jsonify({"board": game.get_board()})

@app.route("/api/move", methods=["POST"])
def make_move():
    data = request.json
    pos1 = data["from"]
    pos2 = data["to"]
    
    move_result = game.make_move(pos1, pos2)
    return jsonify({
        "board": game.get_board(),
        "valid": move_result
    })

@app.route("/api/undo", methods=["POST"])
def undo():
    return jsonify({"board": game.undo()})

@app.route("/api/get-moves", methods=["GET"])
def get_moves():
    return jsonify({"moves": game.get_moves()})

@app.route("/api/stockfish", methods=["GET"])
def stockfish_move():
    return jsonify(game.get_stockfish_move())
    

if __name__ == "__main__":
    app.run(debug=True)