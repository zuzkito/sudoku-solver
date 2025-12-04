"""
The main object of the sudoku playing field and its methods are defined here in this module.
"""


class SudokuBoard:

    # constructor to get a board in
    def __init__(self, initial_grid):
        self.board = initial_grid

    def __str__(self):  # make the board printable, for practical and testing reasons
        printable = [" ".join(str(x) for x in row) for row in self.board]
        return "\n".join(printable)

    def get_value(self, row, col):  # simple getter of box values
        return self.board[row][col]

    def set_value(self, row, col, num):  # simple setter for box values
        self.board[row][col] = num

    # def get_board(self):
    #     return [row.copy() for row in self.board]

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
        for i in range(0,9):
            if num == self.board[i][col]:  # if number in column already, move invalid
                return False

        # check 3x3 box
        start_row = row // 3 * 3  # finds the index of uppermost row in 3x3
        start_col = col // 3 * 3  # finds the index of leftmost col in 3x3

        for i in range(start_row,start_row+3):
            for j in range(start_col, start_col+3):
                if num == self.board[i][j]:
                    return False

        return True

    def initial_validation(self):
        """
        Checks whether the board on input is a valid sudoku problem.
        :return: True if valid, False if not.
        """
        for row in range(0,9):
            for col in range(0,9):

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
        for row in range(0,9):
            for col in range(0,9):
                if self.board[row][col] == 0:  # if box empty
                    return row, col
        return None

#
# board1 = SudokuBoard([[5, 3, 3, 0, 7, 0, 0, 0, 0],[6, 0, 0, 1, 9, 5, 0, 0, 0],[0, 9, 8, 0, 0, 0, 0, 6, 0],[8, 0, 0, 0, 6, 0, 0, 0, 3],[4, 0, 0, 8, 0, 3, 0, 0, 1],[7, 0, 0, 0, 2, 0, 0, 0, 6],[0, 6, 0, 0, 0, 0, 2, 8, 0],[0, 0, 0, 4, 1, 9, 0, 0, 5],[0, 0, 0, 0, 8, 0, 0, 7, 9]])
#
# board2 = SudokuBoard([
#         [5, 3, 0, 0, 7, 0, 0, 0, 0],
#         [6, 0, 0, 1, 9, 5, 0, 0, 0],
#         [0, 9, 8, 0, 0, 0, 0, 6, 0],
#         [8, 0, 0, 0, 6, 0, 0, 0, 3],
#         [4, 0, 0, 8, 0, 3, 0, 0, 1],
#         [7, 0, 0, 0, 2, 0, 0, 0, 6],
#         [0, 6, 0, 0, 0, 0, 2, 8, 0],
#         [0, 0, 0, 4, 1, 9, 0, 0, 5],
#         [0, 0, 0, 0, 8, 0, 0, 7, 9]
#     ])
# print(board2.board)
#
# print(board2.initial_validation())

