from board import *

board1 = SudokuBoard([
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ])

grid = SudokuBoard([row.copy() for row in board1.board])


def tryout(sudoku):
        """
        Finds all possibilities for all empty fields and stores them.
        :param sudoku:
        :return:
        """
        while sudoku.find_empty() is not None:  # while there are still spots to fill
                empty = sudoku.find_empty()   # in an empty box
                row, col = empty
                possibilities = ''

                for i in range(1,10):  # try all possibilities
                        if sudoku.is_move_valid(row, col, i):
                                possibilities += str(i)  # note which are possible
                grid.set_value(row, col, possibilities)  # store that information

def set_possibilities(grid, sudoku:SudokuBoard):
        """
        In all cases where theres's just one possibility, it saves it into the board being solved.
        :param grid: SudokuBoard object where the possibilities are stored.
        :param sudoku: SudokuBoard object of the original sudoku that is solved.
        :return:
        """
        solution_check = False  # will check that there is at least one new box solved
        for row in range(0,9):
                for col in range(0,9):  # dat dovnitr nejakej counter kterej kdyz bude 0, tak to pusti bruteforce
                        field = grid.get_value(row, col)
                        if type(field) == str and len(field) == 1:  # if only one possibility, save it into the normal sudoku
                                sudoku.set_value(row, col, int(field))
                                solution_check = True
        return solution_check


print(f"old board: \n {board1} \n")
tryout(grid)
set_possibilities(grid, board1)
print(set_possibilities(grid, board1))
print(f"new board: \n {board1}")
grid = SudokuBoard([row.copy() for row in board1.board])
tryout(grid)
set_possibilities(grid, board1)
print(f"newer board: \n {board1}")
grid = SudokuBoard([row.copy() for row in board1.board])
tryout(grid)
set_possibilities(grid, board1)
print(f"newer board2: \n {board1}")
grid = SudokuBoard([row.copy() for row in board1.board])
tryout(grid)
