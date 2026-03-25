"""
Backtracking bruteforce, simple constraint propagation and combined sudoku solving functions.
"""
from board import SudokuBoard


def solve_backtracking(sudoku: SudokuBoard):
    """
    Checks if valid and tries to solve the sudoku.
    :param sudoku: A sudoku playing field (SudokuBoard object) to be solved.
    :return: True in case it is solved, False if not valid, edits the SudokuBoard object.
    """

    if sudoku.initial_validation() is False:
        print("The entered sudoku board is not valid.")
        return False

    empty = sudoku.find_empty()  # make sure it is not solved yet
    if empty is None:
        return sudoku  # sudoku solved fully

    row, col = empty
    for i in range(1, 10):
        if sudoku.is_move_valid(row, col, i):
            sudoku.set_value(row, col, i)

            solved = solve_backtracking(sudoku)
            if solved:  # all that's not fase is kind of true
                return solved  # this needed for the sudoku to get returned all the way up

            sudoku.set_value(row, col, 0)  # if not, we're setting back to 0 and backtracking


def tryout(sudoku: SudokuBoard):
    """
    Finds all possibilities for all empty fields and stores them in a copy of the board.
    :return: SudokuBoard with all possibilities as strings.
    """
    grid = SudokuBoard([row.copy() for row in sudoku.board])  # safe copy

    for row in range(0, 9):
        for col in range(0, 9):
            if sudoku.get_value(row, col) == 0:  # only empty cells
                possibilities = ''
                for i in range(1, 10):
                    if sudoku.is_move_valid(row, col, i):
                        possibilities += str(i)
                grid.set_value(row, col, possibilities)

    return grid


def evaluate_possibilities(grid):
    """
    Evaluates the possibilites and finds 'hidden singles', fills them.
    :param grid: SudokuBoard including the possibilities strings.
    :return: The number of fields filled in this run.
    """

    to_fill_in = []  # list of tuples, position and candidate number (row, col, num_str)

    def scanner(coords):
        """
        Helps find the 'hidden singles'. Finds the positions and counts of possibilities.
        :param coords: Iterative of (row, column) tuples defining the unit (row, col 3x3) to scan.
        :return: None, but results are accumulated in the outer to_fill_in list.
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
                to_fill_in.append((row, col, digit))  # we'll fill it in
        return

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
    for (row, col, num_str) in to_fill_in:
        grid.set_value(row, col, num_str)
        applied += 1

    return applied


def set_possibilities(grid, sudoku: SudokuBoard):
    """
    In all cases where there's just one possibility, it saves it into the board being solved.
    :param grid: SudokuBoard object where the possibilities are stored.
    :param sudoku: SudokuBoard object of the original sudoku that is solved.
    :return: Boolean informing whether at least one new box was filled
    """
    solution_check = False  # will check that there is at least one new box solved, so we can start bruteforce
    for row in range(0, 9):
        for col in range(0, 9):
            field = grid.get_value(row, col)
            if type(field) == str and len(field) == 1:  # if only one possibility, save it into sudoku
                sudoku.set_value(row, col, int(field))
                solution_check = True

    return solution_check


def solve_constraint(sudoku: SudokuBoard):
    """
    Simple constraint propagation only solver, solves as long as progress is made.
    :param sudoku: SudokuBoard object of the board to be solved.
    :return: SudokuBoard of the solved (or at least as much as possible) sudoku.
    """
    solution_flag = True

    while solution_flag is True:  # while progress is still being made through constraints
        grid = tryout(sudoku)  # find possible solutions
        evaluate_possibilities(grid)  # evaluate 'hidden singles'
        solution_flag = set_possibilities(grid, sudoku)  # check that progress is still made
    return sudoku


def solve_combined(sudoku: SudokuBoard):
    """
    Combined constraint and bruteforce solver, once no progress is made through constraint propagation, starts
    bruteforce backtracking the partially solved sudoku.
    :param sudoku: SudokuBoard instance of the puzzle to be solved.
    :return: SudokuBoard of the solution.
    """
    solution_flag = True

    while solution_flag is True:  # while progress is still being made through constraints
        grid = tryout(sudoku)
        evaluate_possibilities(grid)
        solution_flag = set_possibilities(grid, sudoku)

    solve_backtracking(sudoku)  # then bruteforce backtrack through the sudoku
    return sudoku
