from Logic import Chess

def main():
    def run_game():
        game = Chess()
        
        while True:
            game.show_board()
            pos1 = input(print("pos1: "))
            if pos1 == "0":
                break
            elif pos1 == "-1":
                game.undo()
            else:
                pos2 = input(print("pos2: "))
                game.move(pos1, pos2)
        return game.board
    
    return run_game()
    

if __name__ == "__main__":
    save = main()

    print("Final Board:")
    for row in save:
        print(" ".join(row))