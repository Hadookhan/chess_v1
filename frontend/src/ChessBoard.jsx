import './ChessBoard.css';

const ChessBoard = ({ board, onSquareClick, selectedSquare }) => {
  return (
    <div className='board-wrapper'>
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
                  color: cell === cell.toUpperCase() ? "white" : "black",
                  fontSize: 36,
                  textAlign: "center",
                  lineHeight: "60px",
                  cursor: "pointer",
                }}
              >
                {cell !== "." ? cell : ""}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};

export default ChessBoard;
