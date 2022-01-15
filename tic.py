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
    grid = []

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

    def __str__(self):
        buff = ""
        for r in self.grid:
            buff += " ".join([str(e) for e in r]) + "\n"
        return buff.replace("0", "-")

    def turn(self, player, row, col):
        self.grid[row][col] = player

        player_score = self.x if player == 'X' else self.o

        # row check
        self.seq_row[row] += player_score

        # col check
        self.seq_col[col] += player_score

        # dia check
        if row == col:
            self.seq_dia[0] += player_score
            if row == 1:
                self.seq_dia[1] += player_score
        elif abs(row-col) == 2:
            self.seq_dia[1] += player_score

        # print([item for sublist in [self.seq_row, self.seq_col, self.seq_dia] for item in sublist])
        flat_list = [abs(item) for sublist in [self.seq_row, self.seq_col, self.seq_dia] for item in sublist]
        # print(flat_list)
        return self.n in flat_list


if __name__ == '__main__':

    count = 0
    player_1 = input(f"Player 1, select your symbol (X/O): ")
    player_2 = "X" if player_1 == "O" else "O"

    if {"X", "O"} != {player_1, player_2}:
        sys.stderr.write("Please choose between uppercase X and O only.")
        sys.exit(0)

    play_grid = Grid()
    while True:
        player = [player_1, player_2][count % 2]
        print(f"Player '{player}' Turn: \n ('q' to exit)")

        try:
            row = input("Enter the row:")
            if row.lower() == "q":
                raise KeyboardInterrupt

            col = input("Enter the col:")
            if col.lower() == "q":
                raise KeyboardInterrupt

            row, col = int(row), int(col)
            if not (0 <= row <= 2 and 0 <= col <= 2):
                print(f"{bcolors.FAIL}Error: The values can be between 0 and 2 only.{bcolors.ENDC}")
                raise Exception("Invalid Input")

            # TODO: handle this as classmethod
            if play_grid.grid[row][col] != 0:
                print(f"{bcolors.WARNING}Warning: The slot ({row},{col}) is already taken.{bcolors.ENDC}")
                raise Exception("Invalid Input")

        except KeyboardInterrupt:
            sys.exit(0)

        except:
            # TODO: Extend Exception to raise invalid input.
            print(f"Enter the integer for row and column of your choice.")
            print(f"Player '{player}', play again.\n")
            continue

        else:
            is_winner = play_grid.turn(player, int(row), int(col))
            if is_winner:
                print(f"{bcolors.OKGREEN}Player {player} WON!!{bcolors.ENDC}")
                break
            if count == 7:
                if 2 not in [abs(item) for sublist in [play_grid.seq_row, play_grid.seq_col, play_grid.seq_dia] for item in sublist]:
                    print("Draw!! Exiting.")
                    break
            elif count == 8:
                print("Its a draw!")
                break
            count += 1
            print(play_grid)
