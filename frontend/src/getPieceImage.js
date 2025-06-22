import * as black from './assets/blackPieces';
import * as white from './assets/whitePieces';

const getPieceImage = (cell) => {
  if (cell === ".") return null;
  const piece = cell.toLowerCase();

  return cell === cell.toUpperCase()
    ? white[piece] // white piece
    : black[piece]; // black piece
};

export default getPieceImage;