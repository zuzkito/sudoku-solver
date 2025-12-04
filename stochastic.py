import random
import math
from copy import deepcopy
from board import SudokuBoard

def count_conflicts(board: SudokuBoard):
    """Return total number of row + column conflicts."""
    conflicts = 0

    # Row conflicts
    for r in range(9):
        row = [x for x in board.board[r] if x != 0]
        conflicts += len(row) - len(set(row))

    # Column conflicts
    for c in range(9):
        col = [board.board[r][c] for r in range(9) if board.board[r][c] != 0]
        conflicts += len(col) - len(set(col))

    return conflicts


def fill_random(board: SudokuBoard, fixed):
    """
    Fills each 3×3 box with the missing digits randomly,
    respecting the original fixed positions.
    """
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):

            # Collect digits already fixed in this block
            used = set()
            for r in range(br, br+3):
                for c in range(bc, bc+3):
                    if fixed[r][c]:
                        used.add(board.board[r][c])

            # Determine missing digits
            missing = [d for d in range(1, 10) if d not in used]
            random.shuffle(missing)

            # Fill non-fixed cells with random missing digits
            idx = 0
            for r in range(br, br+3):
                for c in range(bc, bc+3):
                    if not fixed[r][c]:
                        board.board[r][c] = missing[idx]
                        idx += 1


def stochastic_solve(initial_board: SudokuBoard, max_iterations=200000000):
    """
    Stochastic sudoku solver using simulated annealing-like optimization.
    Returns solved SudokuBoard or None if not solved.
    """

    # Fixed cells mask
    fixed = [[initial_board.board[r][c] != 0 for c in range(9)] for r in range(9)]

    # Make working copy
    board = SudokuBoard(deepcopy(initial_board.board))

    # Initial random fill
    fill_random(board, fixed)

    current_conf = count_conflicts(board)

    if current_conf == 0:
        return board   # Already solved (!)

    temperature = 1.0  # annealing temperature
    cooling = 0.99995  # slow gradual cooling

    for step in range(max_iterations):

        # Pick random block
        br = 3 * random.randint(0, 2)
        bc = 3 * random.randint(0, 2)

        # Pick two random non-fixed cells *in the same block*
        free_cells = [(r, c) for r in range(br, br+3)
                              for c in range(bc, bc+3)
                              if not fixed[r][c]]

        if len(free_cells) < 2:
            continue

        (r1, c1), (r2, c2) = random.sample(free_cells, 2)

        # Swap them
        board.board[r1][c1], board.board[r2][c2] = board.board[r2][c2], board.board[r1][c1]

        new_conf = count_conflicts(board)

        # Accept if better OR with annealing probability
        if new_conf < current_conf:
            current_conf = new_conf
        else:
            # Probability based on temperature
            if random.random() < math.exp((current_conf - new_conf) / temperature):
                current_conf = new_conf
            else:
                # Revert swap
                board.board[r1][c1], board.board[r2][c2] = board.board[r2][c2], board.board[r1][c1]

        temperature *= cooling

        # If no conflicts → solved!
        if current_conf == 0:
            return board

    return None   # Failed to solve

dadsboard =  SudokuBoard([
        [0, 0, 0, 0, 0, 0, 8, 0, 2],
        [0, 0, 0, 6, 0, 0, 1, 0, 0],
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 6, 0, 0, 0],
        [0, 0, 0, 7, 0, 0, 0, 9, 0],
        [0, 0, 0, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 3, 8, 5, 0, 0],
        [0, 0, 9, 0, 0, 0, 0, 3, 0],
        [4, 0, 0, 0, 9, 0, 0, 0, 0]
    ])

print(stochastic_solve(dadsboard))