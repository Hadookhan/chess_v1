import { useEffect, useState } from "react";
import ChessBoard from "./ChessBoard";
import Return from "./Return"
import Moves from "./Moves"
import { io } from "socket.io-client";
import './Game.css';

function App() {
  const [board, setBoard] = useState([]);
  const [from, setFrom] = useState(null);
  const [selectedSquare, setSelectedSquare] = useState(null);
  const [moves, setMoves] = useState(null);

  useEffect(() => {
    const socket = io("https://chess-v1.onrender.com", {
    transports: ["websocket"],
    withCredentials: true,
    });

    socket.on("connect", () => {
      socket.emit("join", { room: "main" });
    })

    socket.on("move", (data) => {
      console.log("Received move:", data);
      setBoard(data.board);
    });

    return () => socket.disconnect();
  }, []);


  useEffect(() => {
    fetch("https://chess-v1.onrender.com/api/board")
      .then(res => res.json())
      .then(data => setBoard(data.board));
  }, []);

  const handleSquareClick = (row, col) => {
    if (!from) {
      setFrom({ row, col });
    } else {
      const to = { row, col };

      const fromStr = String.fromCharCode(97 + from.col) + (8 - from.row); // string conv from ASCII code for from pos
      const toStr = String.fromCharCode(97 + to.col) + (8 - to.row); // string conv from ASCII code for to pos

      fetch("https://chess-v1.onrender.com/api/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ from: fromStr, to: toStr }),
      })
        .then(res => res.json())
        .then(data => {
          setBoard(data.board);
          setFrom(null);
        });
    }
  };

  const handleButtonClick = () => {
    fetch("https://chess-v1.onrender.com/api/undo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    })
    .then(response => response.json()) // Parse JSON first
    .then(data => {
      setBoard(data.board);
    })
    .catch((error) => {
      console.error("Error during undo:", error);
    });
};

  const getMoves = () => {
    fetch("https://chess-v1.onrender.com/api/get-moves", {
      method: "GET",
    })
      .then(res => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json()
      })
      .then(data => {
        console.log("Fetched moves:", data.moves);
        setMoves(data.moves);
      })
      .catch(err => {
        console.error("Fetch failed:", err);
        return [];
      });
    }

  return (
    <div>
      <h1>Chess Game</h1>
      <div className="game">
        <Return onButtonClick={handleButtonClick} />
        <ChessBoard board={board} onSquareClick={handleSquareClick} selectedSquare={selectedSquare} />
      </div>
    </div>
  );
}

export default App;
