from board import SudokuBoard
import copy

# Original board
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


def tryout(sudoku: SudokuBoard):
    """
    Finds all possibilities for all empty fields and stores them in a copy of the board.
    :param sudoku: Original SudokuBoard
    :return: SudokuBoard copy with possibilities as strings
    """
    grid = SudokuBoard([row.copy() for row in sudoku.board])  # safe copy

    for row in range(9):
        for col in range(9):
            if sudoku.get_value(row, col) == 0:  # empty cell
                possibilities = ''
                for i in range(1, 10):
                    if sudoku.is_move_valid(row, col, i):
                        possibilities += str(i)
                grid.set_value(row, col, possibilities)

    return grid


def set_possibilities(grid: SudokuBoard, sudoku: SudokuBoard):
    """
    For all cells with a single possibility, fill it in the original board.
    :param grid: SudokuBoard with possibilities
    :param sudoku: Original SudokuBoard to update
    :return: True if at least one new cell was filled
    """
    solution_check = False

    for row in range(9):
        for col in range(9):
            field = grid.get_value(row, col)
            if isinstance(field, str) and len(field) == 1:  # only one possibility
                sudoku.set_value(row, col, int(field))
                solution_check = True

    return solution_check


def constraint_solver(sudoku: SudokuBoard):
    """
    Constraint propagation solver:
    Repeatedly fills cells with only one possibility.
    """
    solution_flag = True

    while solution_flag:
        grid = tryout(sudoku)                     # compute possibilities safely
        solution_flag = set_possibilities(grid, sudoku)  # fill single-digit possibilities

    print(f"Done! Solved board (partial/full):\n{sudoku}")


# Run solver
# constraint_solver(board1)
tryout(board1)