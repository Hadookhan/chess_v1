from Logic import Chess

def main():
    game = Chess()
    
    while True:
        game.show_board()
        pos1, pos2 = input(print("pos1: ")), input(print("pos2: "))
        if pos1 == 0:
            break
        game.move(pos1, pos2)

main()