import './ChessBoard.css';
import * as blackFolder from './assets/blackPieces';
import * as whiteFolder from './assets/whitePieces';

const ChessBoard = ({ board, onSquareClick, selectedSquare }) => {
  return (
    <div className="chess-board">
      {board.map((row, rowIndex) =>
        row.map((cell, colIndex) => {
          const isSelected =
            selectedSquare &&
            selectedSquare[0] === rowIndex &&
            selectedSquare[1] === colIndex;

          const defaultColor = (rowIndex + colIndex) % 2 === 0 ? "darkgrey" : "#668";
          const backgroundColor = isSelected ? "black" : defaultColor;

          return (
            <div
              key={`${rowIndex}-${colIndex}`}
              onClick={() => onSquareClick(rowIndex, colIndex)}
              style={{
                width: 60,
                height: 60,
                backgroundColor,
                display: flex,
                justifyContent: "center",
                alignItems: "center",
                cursor: "pointer",
                
              }}
            >
              {cell !== "." && (
                <img
                  src={getPieceImage(cell)}
                  alt={cell}
                  style={{ width: "80%", height: "80%" }}
                />
              )}
            </div>
            );
          })
        )}
      </div>
  );
};

export default ChessBoard;
