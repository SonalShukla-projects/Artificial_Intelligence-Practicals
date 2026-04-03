# Sonal Shukla CS23176

board = [" "] * 9
def show():
    print()
    print(board[0], "|", board[1], "|", board[2])
    print("--+---+--")
    print(board[3], "|", board[4], "|", board[5])
    print("--+---+--")
    print(board[6], "|", board[7], "|", board[8])
def win(p):
    return (
        board[0] == board[1] == board[2] == p or
        board[3] == board[4] == board[5] == p or
        board[6] == board[7] == board[8] == p or
        board[0] == board[3] == board[6] == p or
        board[1] == board[4] == board[7] == p or
        board[2] == board[5] == board[8] == p or
        board[0] == board[4] == board[8] == p or
        board[2] == board[4] == board[6] == p
    )
player = "X"
for i in range(9):
    show()
    pos = int(input("Player " + player + " (1-9): ")) - 1
    if board[pos] == " ":
        board[pos] = player
    else:
        print("Invalid move")
        continue
    if win(player):
        show()
        print(player, "wins")
        break
    if player == "X":
        player = "O"
    else:
        player = "X"
else:
    show()
    print("Draw")
