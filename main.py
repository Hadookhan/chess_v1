from Logic import Chess

def main():
    def run_game():
        game = Chess()
        
        while True:
            game.show_board()
            pos1 = input("pos1: ")
            if pos1 == "0":
                break
            elif pos1 == "-1":
                game.undo()
            else:
                pos2 = input("pos2: ")
                game.move(pos1, pos2)
        return game
    
    return run_game()
    

if __name__ == "__main__":
    save = main()

    print("Final Board:")
    for row in save.board:
        print(" ".join(row))

    save.show_moves()

    