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
from __future__ import print_function
import sys
import argparse


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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

        player_score = self.x if player == 'X' else self.o

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

    if {"X", "O"} != {player_1, player_2}:
        sys.stderr.write("Please choose between uppercase X and O only.")

    my_g = Grid()
    while True:
        player = [player_1, player_2][count % 2]
        print(f"Player '{player}' Turn: \n ('q' to exit)")

        try:
            row = input("Enter the row:")
            if row.lower() == "q":
                break
            col = input("Enter the col:")
            if col.lower() == "q":
                break

            elif not (0 <= int(row) <= 2 and 0 <= int(col) <= 2):
                # print("The values can be between 0 and 2 only.")
                print(f"{bcolors.FAIL}Error: The values can be between 0 and 2 only.?{bcolors.ENDC}")
                raise Exception("Invalid Input")

        except:
            print("Enter the integer for row and column of your choice.\n")
            continue

        else:
            is_winner = my_g.turn(player, int(row), int(col))
            if is_winner or count == 8:
                print(f"Player {player} WON!!")
                break
            count += 1
