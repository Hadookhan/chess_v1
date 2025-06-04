from Logic import Chess
from Engine import run_game

def main():
    return run_game()
    

if __name__ == "__main__":
    save = main()

    print("Final Board:")
    for row in save.board:
        print(" ".join(row))

    save.show_moves()