from board import *
from solver_babyversion import solve_backtracking


def tryout(sudoku: SudokuBoard):
    """
    Finds all possibilities for all empty fields and stores them in a copy of the board.
    """
    grid = SudokuBoard([row.copy() for row in sudoku.board])  # safe copy

    for row in range(9):
        for col in range(9):
            if sudoku.get_value(row, col) == 0:  # only empty cells
                possibilities = ''
                for i in range(1, 10):
                    if sudoku.is_move_valid(row, col, i):
                        possibilities += str(i)
                grid.set_value(row, col, possibilities)

    return grid


def evaluate_possibilities(grid):
    """
    Evaluates the possibilites and finds 'hidden singles'.
    :param grid:
    :return:
    """

    to_fillin = []  # list of tuples, position and candidate number (row, col, num_str)


    def scanner(coords):
        """
        Helps find the 'hidden singles'. Finds the positions and counts of possibilities.
        :param coords:
        :return:
        """
        counts = {str(d): 0 for d in range(1, 10)}  # initiate counting dictionary
        positions = {str(d): [] for d in range(1, 10)}  # initiate dictionary for saving positions

        for (row, col) in coords:
            field = grid.get_value(row, col)
            if type(field) == str and len(field) > 0:  # in case of more possibilities
                for char in field:  # counts numbers that occur
                    counts[char] += 1
                    positions[char].append((row, col))  # saves their positions

        for digit in "123456789":
            if counts[digit] == 1:  # if the digit occurs only once
                row, col = positions[digit][0]
                to_fillin.append((row, col, digit))  # we'll fill it in

    # now scan rows
    for row in range(0, 9):
        coords = [(row, col) for col in range(0, 9)]
        scanner(coords)

    # columns
    for col in range(0, 9):
        coords = [(row, col) for row in range(0, 9)]
        scanner(coords)

    # 3x3 boxes
    for start_row in range(0, 9, 3):
        for start_col in range(0, 9, 3):
            coords = [(row, col) for row in range(start_row, start_row + 3) for col in range(start_col, start_col + 3)]
            scanner(coords)

    applied = 0  # just a counter
    for (row, col, num_str) in to_fillin:
        grid.set_value(row, col, num_str)
        applied += 1

    return applied



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
        # print(sudoku)
        return solution_check

def solve_constraint(sudoku:SudokuBoard):
        solution_flag = True
        i = 0
        while solution_flag == True:
                grid = tryout(sudoku)
                evaluate_possibilities(grid)
                solution_flag = set_possibilities(grid, sudoku)
                i += 1
                # print(i)
        # print(f"hehe constraints done:\n  {sudoku}")
        return sudoku


def solve_combined(sudoku: SudokuBoard):
    solution_flag = True
    i = 0
    while solution_flag == True:
        grid = tryout(sudoku)
        evaluate_possibilities(grid)
        solution_flag = set_possibilities(grid, sudoku)
        i += 1

    solve_backtracking(sudoku)
    # print(f"hehe bruteforced: \n {sudoku}")
    return sudoku

# sampleboard = SudokuBoard([ [7, 2, 3, 0, 0, 0, 0, 4, 0],
#                                    [0, 0, 9, 1, 0, 0, 0, 0, 0],
#                                    [1, 0, 0, 9, 4, 0, 0, 0, 0],
#                                    [0, 3, 0, 0, 0, 4, 7, 0, 0],
#                                    [6, 1, 0, 0, 3, 0, 0, 9, 4],
#                                    [0, 0, 7, 8, 0, 0, 0, 2, 0],
#                                    [0, 0, 0, 0, 7, 9, 0, 0, 5],
#                                    [0, 0, 0, 0, 0, 1, 9, 0, 0],
#                                    [0, 5, 0, 0, 0, 0, 6, 7, 1]])
#
# xtremeboard = SudokuBoard([
#         [0, 0, 9, 0, 0, 0, 2, 0, 0],
#         [0, 8, 0, 5, 0, 0, 0, 1, 0],
#         [7, 0, 0, 0, 0, 0, 0, 0, 6],
#         [0, 0, 6, 0, 9, 0, 0, 0, 0],
#         [0, 5, 0, 8, 0, 0, 3, 0, 0],
#         [4, 0, 0, 0, 0, 7, 0, 0, 0],
#         [0, 0, 0, 0, 0, 4, 0, 0, 9],
#         [0, 3, 0, 0, 1, 0, 0, 8, 0],
#         [0, 0, 0, 2, 0, 0, 5, 0, 0]
#     ])
#
# # constraint_solver(sampleboard)
# print(f"{xtremeboard} \n")
# solve_combined(xtremeboard)
# print(xtremeboard)
