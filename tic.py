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


class GridError(Exception):

    def __init__(self, row, col, message):
        self.slot = [str(row), str(col)]
        self.message = message

        super().__init__(self.message)

    def __str__(self):
        return f"Invalid Input ({', '.join(self.slot)}). -> {self.message}"


class GridInputError(GridError):

    def __init__(self, row, col):

        self.message = f"Given slot is not in range (0, 2). " \
                       f"Please choose values for row and col between 0 and 2."
        super().__init__(row, col, self.message)


class GridSlotError(GridError):

    def __init__(self, row, col):
        self.message = f"Given slot is already occupied. Please choose another slot."
        super().__init__(row, col, self.message)


class UserSymbolError(Exception):
    def __init__(self):
        self.message = "User symbol has to be either of uppercase 'X' or 'O' only. Please restart."

    def __str__(self):
        return f"{bcolors.FAIL}{self.message}{bcolors.ENDC}"


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

        self.available_slots_map = {
            "seq_0": [[0, 0], [0, 1], [0, 2]],
            "seq_1": [[1, 0], [1, 1], [1, 2]],
            "seq_2": [[2, 0], [2, 1], [2, 2]],
            "seq_3": [[0, 0], [1, 0], [2, 0]],
            "seq_4": [[0, 1], [1, 1], [2, 1]],
            "seq_5": [[0, 2], [1, 2], [2, 2]],
            "seq_6": [[0, 0], [1, 1], [2, 2]],
            "seq_7": [[2, 0], [1, 1], [0, 2]]
        }
        self.seq_row = [0]*3
        self.seq_col = [0]*3
        self.seq_dia = [0]*2

    def __str__(self):
        buff = ""
        for r in self.grid:
            buff += " ".join([str(e) for e in r]) + "\n"
        return buff.replace("0", "-")

    def mark_slot(self, row, col, score):
        if self.is_slot_available(row, col):
            self.grid[row][col] = score
        else:
            raise GridSlotError(row, col)

    def is_slot_available(self, row, col):
        return self.grid[row][col] == 0

    def get_flat_list(self, is_abs=False):
        if is_abs:
            return [abs(item) for sublist in [self.seq_row, self.seq_col, self.seq_dia] for item in sublist]
        else:
            return [item for sublist in [self.seq_row, self.seq_col, self.seq_dia] for item in sublist]

    def get_next_turn(self, comp_player):
        flat_list = self.get_flat_list()
        for i in [2, -2, -1, 1, 0]:
            if i in flat_list:
                seq_idx = flat_list.index(i)
                if len(self.available_slots_map[f"seq_{seq_idx}"]) > 0:
                    return self.available_slots_map[f"seq_{seq_idx}"][0]

    def turn(self, player, row, col):
        self.mark_slot(row, col, player)
        player_score = self.x if player == 'X' else self.o

        # row check
        self.seq_row[row] += player_score
        self.available_slots_map[f"seq_{row}"].remove([row, col])
        # col check
        self.seq_col[col] += player_score
        self.available_slots_map[f"seq_{col+3}"].remove([row, col])
        # dia check
        if row == col:
            self.seq_dia[0] += player_score
            self.available_slots_map[f"seq_6"].remove([row, col])
        if row == self.n - 1 - col:
            self.seq_dia[1] += player_score
            self.available_slots_map[f"seq_7"].remove([row, col])

        is_winner = self.n in self.get_flat_list(is_abs=True)
        return is_winner

    def play_next_turn(self, player):
        row, col = self.get_next_turn(player)
        return self.turn(player, row, col)


if __name__ == '__main__':

    def declare_winner(is_winner):
        if is_winner:
            print(f"{bcolors.OKGREEN}Player {player} WON!!{bcolors.ENDC}")
            sys.exit()


    def get_slot_input():
        _row = input("Enter the row:")
        _col = input("Enter the col:")
        if _row.isnumeric() and _col.isnumeric():
            raise GridInputError(_row, _col)
        return int(_row), int(_col)


    count = 0
    # Prompt for choosing computer or human
    is_player_comp = input(f"Do you want to play against a computer? (y/N)")
    is_player_comp = True if "y" == is_player_comp.lower() else False

    # Prompt for choosing symbols
    player_1 = input(f"Player 1, select your symbol (X/O): ")
    if player_1 not in ("X", "O"):
        raise UserSymbolError
    player_2 = "X" if player_1 == "O" else "O"

    play_grid = Grid()
    while True:
        player = [player_1, player_2][count % 2]
        print(f"Player '{player}' Turn:")

        try:
            row, col = get_slot_input()
            if not (0 <= row <= 2 and 0 <= col <= 2):
                raise GridInputError(row, col)

            if not play_grid.is_slot_available(row, col):
                raise GridSlotError(row, col)

        except KeyboardInterrupt:
            sys.exit(0)

        except Exception as e:
            print(f"{bcolors.FAIL}{e}{bcolors.ENDC}\n")
            print(f"Player '{player}', try again.")
            continue

        else:
            is_winner = play_grid.turn(player, int(row), int(col))
            # print(play_grid)
            declare_winner(is_winner)
            if count >= 8:
                print("Its a draw!")
                break

            count += 1

            if is_player_comp:
                is_winner = play_grid.play_next_turn(player_2)
                # print(play_grid)
                declare_winner(is_winner)
                count += 1
