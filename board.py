"""
The class of the main object of the sudoku playing field (SudokuBoard) and its methods are defined here in this module.
"""


class SudokuBoard:

    def __init__(self, initial_grid):  # constructor to get a board in
        self.board = initial_grid

    def __str__(self):  # make the board printable, for practical and testing reasons
        printable = [" ".join(str(x) for x in row) for row in self.board]
        return "\n".join(printable)

    def get_value(self, row: int, col: int):
        """
        Simple getter of board values in each cell.
        :param row: Row index.
        :param col: Column index.
        :return: Value stored in the cell with these indexes/coordinates.
        """
        return self.board[row][col]

    def set_value(self, row: int, col: int, num: int):
        """
        Simple setter of board values for each cell. Puts a number into a specific place on board.
        :param row: Row index.
        :param col: Column index.
        :param num: Number to enter into the cell.
        :return: None
        """
        self.board[row][col] = num
        return

    def is_move_valid(self, row, col, num):
        """
        Checks whether adding a certain number to a box would be ok with numbers already present.
        :param row: index of a row to add to
        :param col: index of a column to add to
        :param num: what number is to be added
        :return: False, if this addition isn't valid. True, if it's possible.
        """
        # check rows
        if num in self.board[row]:  # if number in row already, move invalid
            return False

        # check columns
        for i in range(0, 9):
            if num == self.board[i][col]:  # if number in column already, move invalid
                return False

        # check 3x3 box
        start_row = row // 3 * 3  # finds the index of uppermost row in 3x3
        start_col = col // 3 * 3  # finds the index of leftmost col in 3x3

        for i in range(start_row, start_row+3):
            for j in range(start_col, start_col+3):
                if num == self.board[i][j]:
                    return False

        return True

    def initial_validation(self):
        """
        Checks whether the board on input is a valid sudoku problem.
        :return: True if valid, False if not.
        """
        for row in range(0, 9):
            for col in range(0, 9):

                if self.board[row][col] != 0:  # if box not empty
                    num = self.get_value(row, col)  # remember the number in it and empty box temporarily
                    self.set_value(row, col, 0)

                    if not self.is_move_valid(row, col, num):  # if it wouldn't be valid to put it there
                        self.set_value(row, col, num)  # reset original number
                        return False  # the sudoku is invalid

                    self.set_value(row, col, num)  # reset original number
        return True  # if all filled boxes are valid, the sudoku board itself is

    def find_empty(self):
        """
        Finds the next empty box on the board.
        :return: row index, column index (of empty box), None if all occupied.
        """
        for row in range(0, 9):
            for col in range(0, 9):
                if self.board[row][col] == 0:  # if box empty
                    return row, col
        return None
