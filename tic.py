# tic-tac-toe

# Define a class Grid
# Defines a turn
# Sets players notation 'x' or 'o'

# Winner
# Player who scored 3 in any of the following 8 sequence is the winner

# Draw
# When the grid is completed

# Grid [
#   [0,0],      [0,1],      [0,2],
#   [1,0],      [1,1],      [1,2],
#   [2,0],      [2,1],      [2,2]
# ]
import argparse


class Grid:

    def __init__(self):
        self.n = 3
        self.x = -1
        self.o = 1

        self.grid = [[0 for i in range(self.n)] for j in range(self.n)]

        # [[0,0], [0,1], [0,2],     [1,0], [1,1], [1,2],    [2,0], [2,1], [2,2]]
        self.seq_row = [0]*3

        # [[0,0], [[1,0], [2,0],    [0,1], [1,1], [2,1],    [0,2], [1,2], [2,2]]
        self.seq_col = [0]*3

        # [[0,0], [1,1], [2,2],     [2,0], [1,1], [0,2]]
        self.seq_dia = [0]*2
#   [2,1]

    def turn(self, player, row, col):
        self.grid[row][col] = player
        for r in self.grid:
            print( " ".join(str(e) for e in r).replace("0", "-"))
        print("\n")

        player_score = self.x if player == 'x' else self.o

        # row check
        self.seq_row[row] += player_score

        # col check
        self.seq_col[col] += player_score

        # dia check
        if row == col:
            self.seq_dia[row] += player_score
            if row == 1:
                self.seq_dia[0] += player_score
        elif abs(row-col) == 2:
            self.seq_dia[1] += player_score

        flat_list = [abs(item) for sublist in [self.seq_row, self.seq_col, self.seq_dia] for item in sublist]
        print(flat_list)
        if self.n in flat_list:
            return True
        else:
            return False


if __name__ == '__main__':

    count = 0
    player_1 = input(f"Player 1, select your symbol (X/O): ")
    player_2 = "X" if player_1 == "O" else "O"

    # Check for valid symbols

    my_g = Grid()
    while True:
        player = [player_1, player_2][count % 2]
        print(f"Player '{player}' Turn:")

        try:
            input_int_array = [int(x) for x in input("Enter the slot ('row col'):  ").split()]
            if len(input_int_array) != 2:
                raise Exception("Please enter only two integers.")
            else:

        except (IndexError, ValueError, TypeError):
            print("Enter the row and column of your choice separated by space.\n Example: 1 1")
            print("Try again\n")
            #
            # print("Try again\n")

            continue
        else:
            is_winner = my_g.turn(player, )
            if is_winner or count == 8:
                print(f"Player {player} WON!!")
                break
            count += 1
