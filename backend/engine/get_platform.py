import platform
from pathlib import Path

def get_stockfish_binary():
    base_path = Path(__file__).resolve().parent.parent
    binary_dir = base_path / "stockfish"

    system = platform.system()
    if system == "Windows":
        binary = "stockfish-windows-x86-64-avx2.exe"
    elif system == "Darwin":
        binary = "stockfish-macos-m1-apple-silicon"
    elif system == "Linux":
        binary = "stockfish-ubuntu-x86-64-avx2"
    else:
        raise RuntimeError("Unsupported platform")
    
    full_path = binary_dir / binary

    if not full_path.exists():
        raise FileNotFoundError(f"Stockfish binary not found: {full_path}")
    
    return str(full_path)
