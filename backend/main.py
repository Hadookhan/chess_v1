import eventlet
eventlet.monkey_patch()

from engine.GameWrapper import GameWrapper
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, emit
from werkzeug.security import generate_password_hash
from engine.Client import User, SessionLocal
import os

app = Flask(__name__)
CORS(app, origins="http://localhost:5000")
socketio = SocketIO(app, cors_allowed_origins=[
    "http://localhost:5000"
], async_mode="eventlet")

game = GameWrapper()

@app.route("/")
def home():
    return "Chess backend is running"

@app.route("/api/register", methods=["POST"])
def register():
    session = SessionLocal()
    data = request.json

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "All fields required"}), 400

    if session.query(User).filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409

    if session.query(User).filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    new_user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password)
    )

    session.add(new_user)
    session.commit()
    session.close()

    return jsonify({"message": "User registered successfully"}), 201


@app.route("/api/board", methods=["GET"])
def get_board():
    return jsonify({"board": game.get_board()})

@app.route("/api/move", methods=["POST"])
def make_move():
    data = request.json
    pos1 = data["from"]
    pos2 = data["to"]

    move_result = game.make_move(pos1, pos2)

    socketio.emit("move", {"from": pos1, "to": pos2, "board": game.get_board()})
    
    return jsonify({
        "board": game.get_board(),
        "valid": move_result
    })

@app.route("/api/undo", methods=["POST"])
def undo():

    board = game.undo()

    socketio.emit("move", {
    "from": None,
    "to": None,
    "board": game.get_board()
})

    return jsonify({"board": board})

@app.route("/api/get-moves", methods=["GET"])
def get_moves():
    return jsonify({"moves": game.get_moves()})

@app.route("/api/stockfish", methods=["GET"])
def stockfish_move():
    return jsonify(game.get_stockfish_move())

@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    emit('status', {'msg': f'User joined room {room}'}, room=room)

    

if __name__ == "__main__":
    socketio.run(app, debug=True)