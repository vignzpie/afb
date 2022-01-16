"""
    Problem Statement: A program that allows 2 players (human vs human) or 1 player (human vs computer) to play Tic Tac Toe.

    Assumptions:
        - The grid is of the size 3 * 3
        - The user symbol has to be one of 'X' or 'O', strictly upper case. On choosing any other symbol the program quits.
        - The user input for the slot is captured by two parameters row and col (column).
        - The values for row and col has to be one of 0, 1 or 2 denoting first, second and third row/column respectively.
        - The computer move is not deploying any greedy algorithm, which allows the human user to win the game.
        - The game is completed when a player wins or the grid ends in draw.
        - Win is defined by marking the entire sequence (3) by player symbol. 3 rows, 3 columns, 2 diagonals form the 8 sequences.
        - The game is considered draw when all the 9 slots are occupied without formingn any win sequence.
    
    Author:
        Vignesh D Pai (vigneshpai1993@gmail.com)
    
    Repo:
        https://github.com/vignzpie/afb/blob/main/tic.py
"""

import sys


class GridError(Exception):
    """
        Base class for Grid related exceptions inherited from Exception class.
        The error message is defined in the child classes.

    Args:
        row ([int]): row integer
        col ([int]): col integer
    """

    def __init__(self, row, col, message):
        self.slot = [str(row), str(col)]
        self.message = message

        super().__init__(self.message)

    def __str__(self):
        return f"Invalid Input ({', '.join(self.slot)}). -> {self.message}"


class GridInputError(GridError):
    """
        Exception class to handle grid input inherited from Grid class.
        Defines a custom message for the error.

    Args:
        row ([int]): user input row
        col ([int]): user input column
    """

    def __init__(self, row, col):

        self.message = f"Given slot is not in range (0, 2). " \
                       f"Please choose values for row and col between 0 and 2."
        super().__init__(row, col, self.message)


class GridSlotError(GridError):
    """
        Exception class to handle grid slot availability, inherited from Grid class.
        Defines a custom message for the error.

    Args:
        row ([int]): row component of the slot
        col ([int]): column  component of the slot
    """
    def __init__(self, row, col):
        self.message = f"Given slot is already occupied. Please choose another slot."
        super().__init__(row, col, self.message)


class UserSymbolError(Exception):
    """
        Exception class to handle user symbol input. Defines a custom message for the error.

    """
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
    """
        Implements a number of methods for making a turn, marking a slot, predict next turn along with other utilities.

    Raises:
        GridSlotError: Exception if slot is already occupied while assigning symbol to the slot.
    """
    # grid = []

    def __init__(self):
        # Size of the grid
        self.n = 3
        # Score for player, rewarded for making a turn
        self.x = -1
        self.o = 1
        # Empty for grid of n*n matrix where all elements is set to 0.
        self.grid = [[0 for i in range(self.n)] for j in range(self.n)]
        # A dictionary to keep track of availability of slots across the 9 interested sequences.
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
        # Set of sequences, which is set to 0 by default, +1 or -1 is added to it when the player makes a move.
        self.seq_row = [0]*3
        self.seq_col = [0]*3
        self.seq_dia = [0]*2

    def __str__(self):
        """
            Generates a string that represents the current state of the grid.

        Returns:
            [str]: String representing the state of greid
        """

        buff = ""
        for r in self.grid:
            buff += " ".join([str(e) for e in r]) + "\n"
        return buff.replace("0", "-")

    def mark_slot(self, row, col, score):
        """
            Marks a slot by assigning the given slot to the grid, slot is determined by given row and col value.

        Args:
            row ([int]): row value that determined the slot
            col ([int]): column value that determined the slot
            score ([int]): player value either +1 or -1

        Raises:
            GridSlotError: Exception if grid slot is already occupied.
        """

        if self.is_slot_available(row, col):
            self.grid[row][col] = score
        else:
            raise GridSlotError(row, col)

    def is_slot_available(self, row, col):
        """
            Checks if the slot determined by row, col is occupied or not.

        Args:
            row ([int]): [description]
            col ([int]): [description]

        Returns:
            [bool]: True if the slot is empty/available
        """

        return self.grid[row][col] == 0

    def get_flat_list(self, is_abs=False):
        """
            Returns a flat 1D list containing the value from all the 8 sequences, covering 3 rows and coluns and 2 diagonals.

        Args:
            is_abs (bool, optional): Flag to determine whether to return absolute values of all the elements.
             Defaults to False.

        Returns:
            [list]: List of values determining the sequence.
        """

        if is_abs:
            return [abs(item) for sublist in [self.seq_row, self.seq_col, self.seq_dia] for item in sublist]
        else:
            return [item for sublist in [self.seq_row, self.seq_col, self.seq_dia] for item in sublist]

    def get_next_turn(self, comp_player):
        """
            This method determines the next move with basic set of rules. Without implementing any fancy greedy algorithms.
            Next best move is determined in the following priority:
                - Move if it's a winner move. (i == 2)
                - Move if it prevents opponent from winning. (i == -2)
                - Move to any sequence that doesn't let opponent score -2. (i == -1)
                - Move to any sequence that lets the computer player to score 2. (i == 1)
                - Move to any available slot. (i == 0)
            Determines the next best move prioritizing winning move over preventing opponent winner move.
            Followed by choosing sequences that are already filled.

        Args:
            comp_player ([int]): Score of the computer player.

        Returns:
            [int, int]: row, col denoting the slot which is the calculated next best move.
        """
        flat_list = self.get_flat_list()
        seq_priority = [2, -2, -1, 1, 0]
        if comp_player != 1:
            seq_priority = [e * comp_player for e in seq_priority]

        for i in seq_priority:
            if i in flat_list:
                seq_idx = flat_list.index(i)
                if len(self.available_slots_map[f"seq_{seq_idx}"]) > 0:
                    return self.available_slots_map[f"seq_{seq_idx}"][0]

    def turn(self, player, row, col):
        """
            This method marks the slot in the grid as occupied by assigning the player score.
            Manipulates the value of 8 sequences of interest, by adding player score.
            Manipulates the available_slot_map by removing the slots that are occupied.
            If any sequences is complete (by checking if 3 is present in the sequence),
            the current player who just made a turn is flagged as winner.

        Args:
            player ([str]): A character 'X' or 'O' based on which player score is assigned.
            row ([int]): row component of the slot
            col ([int]): column  component of the slot


        Returns:
            [bool]: boolean flag to determine is if the current player is a winner.
        """
        player_score = self.x if player == 'X' else self.o
        self.mark_slot(row, col, player)


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

        """
            Get the next best slot by calling get_next_turn() method.
            The resultant slot is fed to turn method to make the next turn.

        Args:
            player ([int]): Score of the player.

        Returns:
            [bool]: A function call to turn method that returns bool declaring a winner or not.
        """
        player_score = self.x if player == 'X' else self.o
        row, col = self.get_next_turn(player_score)
        return self.turn(player, row, col)


if __name__ == '__main__':

    def declare_winner(is_winner, player):
        """
            Checks if there is a winner, print a message to declare the winner.
        Args:
            is_winner (bool): flag that decides if the player is a winner
            player ([str]): player symbol X/O
        """
        if is_winner:
            print(f"{bcolors.OKGREEN}Player {player} WON!!{bcolors.ENDC}")
            sys.exit()


    def get_slot_input():
        """
            Accept separate input from the user, for row and a column.

        Raises:
            GridInputError: Error if the given input cannot be casted to integer.

        Returns:
            row ([int]): row integer
            col ([int]): column integer
        """
        # Capture input row and col form the playing user.
        _row = input("Enter the row:")
        _col = input("Enter the col:")
        # Verify input is an integer.
        if not (_row.isnumeric() and _col.isnumeric()):
            raise GridInputError(_row, _col)
        return int(_row), int(_col)

    # Counter to stop the game when all turns are exhausted.
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
        # print(play_grid)
        # Player 1 plays the even turns.
        player = [player_1, player_2][count % 2]
        print(f"Player '{player}' Turn:")

        try:
            row, col = get_slot_input()
            # Out of grid xception
            if not (0 <= row <= 2 and 0 <= col <= 2):
                raise GridInputError(row, col)

            # Slot unavailable exception
            if not play_grid.is_slot_available(row, col):
                raise GridSlotError(row, col)

        # ctrl+c to quit game
        except KeyboardInterrupt:
            sys.exit(0)

        except Exception as e:
            print(f"{bcolors.FAIL}{e}{bcolors.ENDC}\n")
            print(f"Player '{player}', try again.")
            continue

        else:
            is_winner = play_grid.turn(player, int(row), int(col))
            print(play_grid)

            declare_winner(is_winner, player)
            # All turns are exhausted when count = 8
            if count >= 8:
                print("Its a draw!")
                break

            count += 1

            if is_player_comp:
                is_winner = play_grid.play_next_turn(player_2)
                print(play_grid)
                declare_winner(is_winner, player)
                count += 1
